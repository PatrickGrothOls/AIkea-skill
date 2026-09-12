"""Scope: Verify shared layer machining, source identity and whole-front motion in a parent."""
from dataclasses import asdict, replace
from math import pi

import cadquery as cq
import pytest

from assembly_door_test_project import AssemblyDoorTestProject
from assembly_feature_review import AssemblyFeatureReviewContext
from assembly_tree_review_geometry import AssemblyTreeReviewGeometry
from assembly_tree_review_plan import AssemblyReviewMotion, AssemblyTreeReviewPlan
from cabinet_feature_manifest import CabinetFeatureManifest
from construction_result_validator import ConstructionResultValidator
from door_hinge_plan import DoorHingePlan
from door_hinge_side import DoorHingeSide
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from local_to_parent_location import LocalToParentLocation
from physical_item_counter import PhysicalItemCounter
from riex_assembly_door_review import RiexAssemblyDoorReview
from riex_nc70_hardware_loader import RiexNc70HardwareSet


class TestAssemblyDoorComponent:
    @pytest.mark.parametrize('hand', (DoorHingeSide.LEFT, DoorHingeSide.RIGHT))
    def test_real_layers_and_parent_support_are_machined_once(self, tmp_path, hand):
        original, plan = AssemblyDoorTestProject().create(tmp_path, hand)
        assert DoorHingePlan.read(tmp_path/'assemblies/niche_01/door_hinges/installation.json') == plan
        loader = GeneratedAssemblyBuilderLoader()
        built = loader.load_assembly(tmp_path, 'niche_01')
        front = built.child_assemblies[0].assembly
        before = original.child_assemblies[0].assembly
        count = len(plan.placements)
        assert ConstructionResultValidator().validate(front) == ()
        assert ConstructionResultValidator().validate(built) == ()
        expected = (count*(pi*17.5**2*9+2*pi*1.25**2*9),
                    count*(pi*17.5**2*3+2*pi*1.25**2*1))
        assert [a.solid.val().Volume()-b.solid.val().Volume() for a,b in zip(before.parts,front.parts)] == pytest.approx(expected)
        assert original.parts[0].solid.val().Volume()-built.parts[0].solid.val().Volume() == pytest.approx(count*2*pi*2.5**2*13)
        inventory = PhysicalItemCounter().count(loader.walk(tmp_path, built))
        assert len(inventory['manufactured_parts']) == 3
        assert len(built.parts) == 1 and len(front.parts) == 2
        assert len(built.purchased_hardware) == count*2
        assert {item.spec.product_code for item in built.purchased_hardware} == {'F000001','F000049'}
        CabinetFeatureManifest().unregister(tmp_path, 'niche_01', 'door_hinges.feature')
        restored = loader.load_assembly(tmp_path, 'niche_01')
        assert not restored.purchased_hardware
        restored_front = restored.child_assemblies[0].assembly
        assert asdict(restored_front.spec) == asdict(before.spec)
        for left, right in zip(restored_front.parts, before.parts):
            a, b = left.solid.val(), right.solid.val()
            assert a.cut(b).Volume()+b.cut(a).Volume() == pytest.approx(0,abs=1e-5)
        assert restored.parts[0].solid.val().Volume() == pytest.approx(original.parts[0].solid.val().Volume())

    @pytest.mark.parametrize('hand', (DoorHingeSide.LEFT, DoorHingeSide.RIGHT))
    def test_both_layers_follow_child_and_parent_motion(self, tmp_path, monkeypatch, hand):
        _, plan = AssemblyDoorTestProject().create(tmp_path, hand)
        loader = GeneratedAssemblyBuilderLoader()
        built = loader.load_assembly(tmp_path, 'niche_01')
        shape = cq.Workplane('XY').box(1,2,3).val()
        hardware = RiexNc70HardwareSet(shape, shape, shape)
        feature = RiexAssemblyDoorReview(plan)
        monkeypatch.setattr(feature.hardware, 'load', lambda _: hardware)
        # Synthetic hardware keeps this test about part motion; sourced CAD is verified separately.
        built = replace(built, purchased_hardware=tuple(replace(item, solid=cq.Workplane(obj=shape)) for item in built.purchased_hardware))
        context = AssemblyFeatureReviewContext(tmp_path, ('niche_01',), built)
        opened = feature.plan(context, 'open')
        assert not opened.hidden_subtrees
        assert opened.motions[0].assembly_path == ('niche_01','front_01')
        parent = cq.Location(cq.Vector(800,200,90), cq.Vector(0,0,1), 37)
        combined = replace(opened, motions=(AssemblyReviewMotion(('niche_01',),parent),)+opened.motions)
        visits = loader.walk(tmp_path, built)
        actual = AssemblyTreeReviewGeometry().build(visits, {}, combined)
        from riex_nc70_hardware_placement import RiexNc70HardwarePlacement
        from door_host import DoorHost
        from riex_nc70_hinge_profile import RIEX_NC70_FULL_OVERLAY as profile
        pivot = RiexNc70HardwarePlacement().pivot(DoorHost.resolve(built,hand,plan.host_spec), profile, hand)
        for item in visits:
            if not hasattr(item,'part'):
                continue
            expected = item.part.solid.val().located(LocalToParentLocation().build(item.local_to_root))
            if 'front_01' in item.path:
                expected = expected.rotate((pivot[0],pivot[1],0),(pivot[0],pivot[1],1), hand.opening_angle_degrees(profile.open_angle_degrees))
            expected = expected.moved(parent)
            name = '__'.join(segment.split(':')[-1] for segment in item.path[1:])
            part = next(part for part in actual if part.name == name)
            received = part.solid.val().located(part.location)
            assert received.cut(expected).Volume()+expected.cut(received).Volume() == pytest.approx(0,abs=1e-5)
        removed = AssemblyTreeReviewGeometry().build(visits, {}, feature.plan(context,'removed'))
        assert [part.name for part in removed] == ['post']

    def test_stale_front_placement_and_missing_purchase_reject(self, tmp_path):
        _, plan = AssemblyDoorTestProject().create(tmp_path)
        built = GeneratedAssemblyBuilderLoader().load_assembly(tmp_path, 'niche_01')
        child = built.child_assemblies[0]
        placement = child.spec.local_to_parent
        moved = replace(child, spec=replace(child.spec, local_to_parent=replace(placement,
            origin_in_parent=replace(placement.origin_in_parent,z_mm=40))))
        changed = replace(built, spec=replace(built.spec, child_assemblies=(moved.spec,)), child_assemblies=(moved,))
        feature = RiexAssemblyDoorReview(plan)
        with pytest.raises(ValueError,match='replan'):
            feature.plan(AssemblyFeatureReviewContext(tmp_path,('niche_01',),changed),'closed')
        with pytest.raises(ValueError,match='exact hinge purchases'):
            feature.plan(AssemblyFeatureReviewContext(tmp_path,('niche_01',),replace(built,spec=replace(built.spec,purchased_hardware=()),purchased_hardware=())),'closed')

    def test_clipped_frame_preflight_does_not_write_or_register_feature(self, tmp_path):
        from cabinet_door_feature_generator import CabinetDoorFeatureGenerator
        from door_host import DoorHost
        from part_construction_error import PartConstructionError
        from riex_nc70_hinge_profile import RIEX_NC70_FULL_OVERLAY as profile
        built, plan = AssemblyDoorTestProject().create(tmp_path, border=10, generate=False)
        host = DoorHost.resolve(built, plan.hinge_side, plan.host_spec)
        before = {p.relative_to(tmp_path): p.read_bytes() for p in tmp_path.rglob('*')
                  if p.suffix in ('.py','.json')}
        with pytest.raises(PartConstructionError, match='clipped'):
            CabinetDoorFeatureGenerator().generate(tmp_path, host, plan, profile)
        after = {p.relative_to(tmp_path): p.read_bytes() for p in tmp_path.rglob('*')
                 if p.suffix in ('.py','.json')}
        assert after == before
        assert not (tmp_path/'assemblies/niche_01/features.json').exists()
        assert not (tmp_path/'assemblies/niche_01/door_hinges/installation.json').exists()
        restored = GeneratedAssemblyBuilderLoader().load_assembly(tmp_path,'niche_01')
        assert not restored.purchased_hardware
