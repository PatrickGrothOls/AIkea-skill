"""Scope: Prove explicit door hosts use paired cuts, source axes and generic opening review."""

from dataclasses import replace
from math import pi
from types import SimpleNamespace

import cadquery as cq
import pytest

from assembly_feature_review import AssemblyFeatureReviewContext
from cabinet_door_feature_generator import CabinetDoorFeatureGenerator
from door_hinge_plan import DoorHingePlanner, DoorHingePlan
from door_hinge_side import DoorHingeSide
from door_host import DoorHost
from door_host_test_support import DoorHostTestSupport
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from physical_item_counter import PhysicalItemCounter
from riex_nc70_door_review_feature import RiexNc70DoorReviewFeature
from riex_nc70_hardware_placement import RiexNc70HardwarePlacement
from riex_nc70_hardware_loader import RiexNc70HardwareSet
from riex_nc70_hardware_reservations import RiexNc70HardwareReservations
from riex_nc70_hinge_profile import RIEX_NC70_FULL_OVERLAY as PROFILE


class TestDoorHostInterface:
    @pytest.mark.parametrize("hand", (DoorHingeSide.LEFT, DoorHingeSide.RIGHT))
    @pytest.mark.parametrize("face", ("<Z", ">Z"))
    def test_saved_custom_front_cuts_and_source_axes_match_inset_translated_hosts(self, tmp_path, hand, face):
        host = DoorHostTestSupport().create(tmp_path, hand, face)
        plan = DoorHingePlanner().plan(host, PROFILE, hand)
        assert plan.overlay_mm == 17 and not plan.compatibility_issues
        path = tmp_path/'assemblies/niche_01/door_hinges/installation.json'
        plan.write(path)
        assert DoorHingePlan.read(path) == plan
        CabinetDoorFeatureGenerator().generate(tmp_path, host.assembly, plan, PROFILE)
        loader = GeneratedAssemblyBuilderLoader()
        built = loader.load_assembly(tmp_path, 'niche_01')
        parts = {part.spec.part_id: part.solid.val() for part in built.parts}
        n = len(plan.placements)
        assert 500*1000*18-parts['slab'].Volume() == pytest.approx(n*(pi*17.5**2*12+2*pi*1.25**2*10))
        assert 582*1000*18-parts['post'].Volume() == pytest.approx(n*2*pi*2.5**2*13)
        assert {cut.part_id for cut in built.cuts} == {'slab', 'post'}
        assert len(built.purchased_hardware) == n*2
        assert len(PhysicalItemCounter().count(loader.walk(tmp_path, built))['manufactured_parts']) == 2
        placement = RiexNc70HardwarePlacement()
        for item in plan.placements:
            hinge = placement.hinge_location(host, PROFILE, host.door_bottom_mm+item.door_height_mm, hand)
            point = self._point(hinge, (PROFILE.native_door_surface_x_mm, PROFILE.native_cup_center_y_mm, 0))
            cup_x = 23.5 if hand is DoorHingeSide.LEFT else 500-23.5
            assert point == pytest.approx((101+cup_x, 70, 32+item.door_height_mm))
            plate = placement.plate_location(host, PROFILE, host.support_bottom_mm+item.cabinet_height_mm, hand)
            points = sorted(self._point(plate, (x, PROFILE.plate_native_panel_face_y_mm, PROFILE.plate_native_fixing_axis_z_mm))
                            for x in (8.693877, 40.693877))
            assert points[0] == pytest.approx((118 if hand is DoorHingeSide.LEFT else 584, 107, 32+item.cabinet_fixing_rows_mm[0]))
            assert points[1] == pytest.approx((118 if hand is DoorHingeSide.LEFT else 584, 107, 32+item.cabinet_fixing_rows_mm[1]))
        reservations = RiexNc70HardwareReservations().from_plan(plan, PROFILE, host)
        assert reservations[0].side_part_id == 'post'
        assert reservations[0].depth_interval_mm == pytest.approx((39.576999, 83.576999))

    def test_generic_review_opens_only_named_front_and_hides_its_own_hardware(self, tmp_path, monkeypatch):
        host = DoorHostTestSupport().create(tmp_path)
        plan = DoorHingePlanner().plan(host, PROFILE)
        plan.write(tmp_path/'assemblies/niche_01/door_hinges/installation.json')
        CabinetDoorFeatureGenerator().generate(tmp_path, host.assembly, plan, PROFILE)
        built = GeneratedAssemblyBuilderLoader().load_assembly(tmp_path, 'niche_01')
        feature = RiexNc70DoorReviewFeature(plan)
        shape = cq.Workplane('XY').box(1, 2, 3).val()
        monkeypatch.setattr(feature.hardware, 'load', lambda root: RiexNc70HardwareSet(shape, shape, shape))
        other = replace(built.purchased_hardware[0], spec=replace(built.purchased_hardware[0].spec, hardware_id='unrelated_hinge'))
        built = replace(built, purchased_hardware=built.purchased_hardware+(other,),
                        spec=replace(built.spec, purchased_hardware=built.spec.purchased_hardware+(other.spec,)))
        context = AssemblyFeatureReviewContext(tmp_path, ('assembly:niche_01',), built)
        opened = feature.plan(context, 'open')
        assert ('assembly:niche_01', 'part:slab') in opened.hidden_paths
        assert ('assembly:niche_01', 'part:post') not in opened.hidden_paths
        assert ('assembly:niche_01', 'hardware:unrelated_hinge') not in opened.hidden_paths
        door = next(part for part in opened.overlays[0].parts if part.name == 'slab')
        original = next(part.solid.val() for part in built.parts if part.spec.part_id == 'slab')
        assert door.solid.val().Volume() == pytest.approx(original.Volume())
        assert door.solid.val().BoundingBox().ymin < -100
        assert feature.plan(context, 'removed').hidden_paths == opened.hidden_paths

    def test_missing_support_and_wrong_hand_fail_before_generation(self, tmp_path):
        host = DoorHostTestSupport().create(tmp_path)
        with pytest.raises(ValueError, match='distinct parts'):
            DoorHost(host.assembly, replace(host.spec, support_part_id='absent'), DoorHingeSide.LEFT)
        with pytest.raises(ValueError, match='selected opposing support'):
            DoorHost(host.assembly, host.spec, DoorHingeSide.RIGHT)

    def test_old_plan_fails_when_door_moves_independently_of_support(self, tmp_path):
        host = DoorHostTestSupport().create(tmp_path)
        plan = DoorHingePlanner().plan(host, PROFILE)
        door = host.door
        frame = door.local_to_parent
        moved = replace(door, local_to_parent=replace(frame, origin_in_parent=replace(frame.origin_in_parent, z_mm=33)))
        changed = replace(host.assembly, parts=(host.support, moved))
        with pytest.raises(ValueError, match='replan'):
            CabinetDoorFeatureGenerator().generate(tmp_path, changed, plan, PROFILE)
        assert not (tmp_path/'assemblies/niche_01/door_hinges/machining.py').exists()

    @pytest.mark.parametrize("inset", (0, 20, 200))
    def test_inset_plates_reserve_real_space_without_claiming_front_grid_nodes(self, tmp_path, inset):
        host = DoorHostTestSupport().create(tmp_path, inset=inset)
        plan = DoorHingePlanner().plan(host, PROFILE)
        actual = RiexNc70HardwareReservations().from_plan(plan, PROFILE, host)[0]
        front = replace(RiexNc70HardwareReservations().for_position(
            'front_fitting', DoorHingeSide.LEFT, (100, 132), 116, PROFILE), side_part_id='post')
        assert bool(actual.system_32_node_rows_mm) == (inset == 0)
        assert actual.conflicts_with(front) == (inset < 200)
        blocked = DoorHingePlanner().plan(host, PROFILE, blocked_reservations=(front,))
        assert (blocked.placements[0].cabinet_fixing_rows_mm == plan.placements[0].cabinet_fixing_rows_mm) == (inset == 200)

    @pytest.mark.parametrize("hand,height,count", ((DoorHingeSide.LEFT, 1000, 3), (DoorHingeSide.RIGHT, 700, 2)))
    def test_sloped_front_uses_height_at_selected_hinge_edge(self, tmp_path, hand, height, count):
        host = DoorHostTestSupport().create(tmp_path, hand)
        outline = tuple(SimpleNamespace(x_mm=x, height_mm=y) for x, y in ((0, 0), (500, 0), (500, 700), (0, 1000)))
        door = replace(host.door, outline_mm=outline)
        changed = DoorHost(replace(host.assembly, parts=(host.support, door)), host.spec, hand)
        plan = DoorHingePlanner().plan(changed, PROFILE, hand)
        assert plan.door_height_mm == height and len(plan.placements) == count
        assert all(100 <= item.door_height_mm <= height-100 for item in plan.placements)

    def _point(self, location, point):
        return cq.Vector(*point).transform(cq.Matrix(location.wrapped.Transformation())).toTuple()
