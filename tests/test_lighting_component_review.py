"""Scope: Verify common lighting review states, nested placement and current-body checks."""
from dataclasses import replace
import json

import cadquery as cq
import pytest

from assembly_feature_review import AssemblyFeatureReviewContext
from cabinet_feature_manifest import CabinetFeatureManifest
from cabinet_lighting_generator import CabinetLightingGenerator
from cabinet_lighting_review_generator import CabinetLightingReviewGenerator
from complete_assembly_review_generator import CompleteAssemblyReviewGenerator
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from lighting_component_review import LightingComponentReview
from lighting_run import LightingRun
from lighting_test_project import LightingTestProject
from part_lighting_plan_loader import PartLightingPlanLoader
from physical_item_counter import PhysicalItemCounter
from recessed_luminaire_profile import DOMUS_APEX_84_HI


class TestLightingComponentReview:
    def test_nested_states_follow_parent_and_keep_physical_inventory(self, tmp_path):
        self._project(tmp_path)
        self._parent(tmp_path)
        generator = CompleteAssemblyReviewGenerator()
        flat = generator.generate(tmp_path, 'custom_01', tmp_path/'flat.glb')
        nested = generator.generate(tmp_path, 'room_01', tmp_path/'on.glb', {'room_01/custom_01/lighting': 'on'})
        off = generator.generate(tmp_path, 'room_01', tmp_path/'off.glb', {'room_01/custom_01/lighting': 'off'})
        assert (flat.part_count, nested.part_count, off.part_count) == (3, 3, 2)
        transform = cq.Location(cq.Vector(700, 80, 120), cq.Vector(0, 0, 1), 90)
        for first, second in zip(flat.rendered_parts, nested.rendered_parts):
            expected = first.solid.val().located(transform*first.location)
            actual = second.solid.val().located(second.location)
            assert actual.cut(expected).Volume()+expected.cut(actual).Volume() == pytest.approx(0, abs=1e-5)
        assert any(part.name.startswith('custom_01__light_source__') for part in nested.rendered_parts)
        for part in nested.rendered_parts:
            if part.review_kind == 'hardware':
                assert part.inspection_path[:-1] == ('custom_01', 'host', 'shelf_light_01')
        assert sum(part.review_kind == 'hardware' for part in nested.rendered_parts) == 2
        assert {part.inspection_path[-1] for part in nested.rendered_parts
                if part.review_kind == 'hardware'} == {'body', 'emitter'}
        assert all(part.inspection_path[:-1] == ('host', 'shelf_light_01')
                   for part in flat.rendered_parts if part.review_kind == 'hardware')
        assert not any('light_source__' in part.name for part in off.rendered_parts)
        assert len(self._inventory(tmp_path)['purchased_summary']) == 1
        CabinetFeatureManifest().unregister(tmp_path, 'custom_01', 'lighting.feature')
        removed = generator.generate(tmp_path, 'room_01', tmp_path/'removed.glb')
        assert removed.part_count == 1 and not removed.feature_selectors
        assert not self._inventory(tmp_path)['purchased_summary']

    def test_compatibility_command_needs_no_drawer_cad(self, tmp_path):
        self._project(tmp_path)
        result = CabinetLightingReviewGenerator().generate(tmp_path, 'custom_01', 'host')
        report = json.loads(result.fit_report_path.read_text())
        assert result.glb_path.stat().st_size > 100
        assert report['status'] == 'geometry_preview' and report['manufacturing_authority'] is False
        assert (tmp_path/report['review_report']).is_file()

    def test_current_body_and_host_clearance_are_checked(self, tmp_path):
        self._project(tmp_path)
        loader = GeneratedAssemblyBuilderLoader()
        built = loader.load_assembly(tmp_path, 'custom_01')
        plan = PartLightingPlanLoader().load(tmp_path/'assemblies/custom_01/parts/host/lighting.yaml')
        review = LightingComponentReview(plan)
        context = AssemblyFeatureReviewContext(tmp_path, ('custom_01',), built)
        changed_plan = replace(plan, run=replace(plan.run, color_temperature_k=4300))
        with pytest.raises(ValueError, match='purchased variant'):
            LightingComponentReview(changed_plan).plan(context, 'on')
        hardware = built.purchased_hardware[0]
        changed = replace(hardware, solid=hardware.solid.translate((1, 0, 0)))
        with pytest.raises(ValueError, match='current owned hardware'):
            review.plan(replace(context, assembly=replace(built, purchased_hardware=(changed,))), 'on')
        blank = cq.Workplane().box(800, 400, 16, centered=(False, False, False))
        with pytest.raises(ValueError, match='interferes with manufactured part'):
            review.plan(replace(context, assembly=replace(built, parts=(replace(built.parts[0], solid=blank),))), 'on')
        with pytest.raises(ValueError, match='supports on/off'):
            review.plan(context, 'removed')

    def test_rejects_retained_plan_after_feature_moves_to_another_host(self, tmp_path):
        self._project(tmp_path)
        path = tmp_path/'assemblies/custom_01/spec.py'
        source = path.read_text().replace('from assemblies.specification', 'from dataclasses import replace\nfrom assemblies.specification')
        source = source.replace("SPEC = PanelAssemblySpec", "OTHER = replace(PART, part_id='other', local_to_parent=replace(PART.local_to_parent, origin_in_parent=Point3D(1100, 200, 50)))\nSPEC = PanelAssemblySpec")
        path.write_text(source.replace('(PART,), ()', '(PART, OTHER), ()'))
        run = LightingRun('shelf_light_01', (50, 200), (650, 200), 3200, DOMUS_APEX_84_HI)
        CabinetLightingGenerator().generate(tmp_path, 'custom_01', 'other', run, base_builder_module='complete_builder')
        with pytest.raises(ValueError, match='inactive'):
            CabinetLightingReviewGenerator().generate(tmp_path, 'custom_01', 'host')
        result = CabinetLightingReviewGenerator().generate(tmp_path, 'custom_01', 'other')
        assert result.glb_path.is_file()

    def test_hidden_ancestor_suppresses_its_lighting_overlays(self, tmp_path):
        self._project(tmp_path)
        self._parent(tmp_path)
        owner = tmp_path/'assemblies/room_01'
        builder = owner/'builder.py'
        builder.write_text(builder.read_text()+"""
from dataclasses import replace
from assemblies.specification import PartSpec, IDENTITY_LOCAL_TO_PARENT
ANCHOR = PartSpec('anchor', 'parent panel', (), IDENTITY_LOCAL_TO_PARENT, local_size_mm=(50,50,16), material_id='mdf')
SPEC = replace(SPEC, parts=(ANCHOR,))
BUILDER = PanelAssemblyBuilder(SPEC, children=(BuiltChildAssembly(PLACEMENT, CHILD),))
""")
        (owner/'features.json').write_text(json.dumps({'schema_version': 1, 'features': [
            {'module': 'preview.feature', 'order': 1, 'review_module': 'review'}]}))
        (owner/'review.py').write_text("""# Scope: Exercise the shared removed-child review contract.
from assembly_tree_review_plan import AssemblyTreeReviewPlan
class RemovedChildReview:
    def plan(self, context, state):
        return AssemblyTreeReviewPlan(hidden_subtrees=(context.owner_path+('custom_01',),))
REVIEW = RemovedChildReview()
""")
        result = CompleteAssemblyReviewGenerator().generate(tmp_path, 'room_01', tmp_path/'hidden.glb')
        assert result.part_count == 1
        assert [part.name for part in result.rendered_parts] == ['anchor']

    def _project(self, root):
        LightingTestProject().create(root)
        run = LightingRun('shelf_light_01', (50, 200), (650, 200), 3200, DOMUS_APEX_84_HI)
        CabinetLightingGenerator().generate(root, 'custom_01', 'host', run, base_builder_module='complete_builder')

    def _inventory(self, root):
        loader = GeneratedAssemblyBuilderLoader()
        return PhysicalItemCounter().count(loader.walk(root, loader.load_assembly(root, 'room_01')))

    def _parent(self, root):
        owner = root/'assemblies/room_01'
        owner.mkdir()
        (owner/'__init__.py').write_text('"""Scope: Own the rotated parent."""\n')
        (owner/'spec.py').write_text('"""Scope: Declare a parent frame."""\n')
        (owner/'builder.py').write_text("""# Scope: Compose an existing component through shared construction.
from assemblies.panel_assembly import PanelAssemblySpec, PanelAssemblyBuilder
from assemblies.specification import ChildAssemblySpec, BuiltChildAssembly, LocalToParentPlacement, Point3D, AxisBasis, AxisDirection
from ..custom_01.complete_builder import BUILDER as CHILD_BUILDER
CHILD = CHILD_BUILDER.build()
FRAME = LocalToParentPlacement(Point3D(700, 80, 120), AxisBasis(AxisDirection(0,1,0), AxisDirection(-1,0,0), AxisDirection(0,0,1)))
PLACEMENT = ChildAssemblySpec('custom_01', CHILD.spec.purpose, FRAME)
SPEC = PanelAssemblySpec('room_01', 'parent', child_assemblies=(PLACEMENT,), requirements=())
BUILDER = PanelAssemblyBuilder(SPEC, children=(BuiltChildAssembly(PLACEMENT, CHILD),))
""")
