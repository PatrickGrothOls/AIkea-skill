"""Scope: Prove actual floor capture, corner access and runner preparation in shared drawers."""

from dataclasses import replace
from itertools import combinations
from functools import partial

import cadquery as cq
import pytest

from construction_requirement_checker import ConstructionRequirementChecker
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from local_to_parent_location import LocalToParentLocation
from panel_blank_builder import PanelBlankBuilder
from test_movento_panel_drawer import TestMoventoPanelDrawer as DrawerFixture
from generated_project_module_runtime import GeneratedProjectModuleRuntime
from movento_panel_dimensions import MoventoPanelDimensions
from movento_panel_drawer import MoventoPanelDrawer
from movento_panel_machining import MoventoPilotChoice
from panel_setup_checker import PanelSetupChecker


class TestMoventoCapturedBottom:
    drawer = DrawerFixture.drawer
    build = DrawerFixture.build

    def placed_parts(self, built):
        placement = LocalToParentLocation()
        return {part.spec.part_id: part.solid.val().located(placement.build(part.spec.local_to_parent))
                for part in built.parts}

    def test_floor_is_captured_in_every_wall_without_solid_overlap(self, drawer):
        _, built = drawer
        parts = self.placed_parts(built)
        for (left, a), (right, b) in combinations(parts.items(), 2):
            assert a.intersect(b).Volume() == pytest.approx(0, abs=1e-5), (left, right)
        placement = LocalToParentLocation()
        floor = parts["bottom"]
        for wall in (part for part in built.parts if part.spec.part_id in ("left","right","front","back")):
            blank = PanelBlankBuilder().build(wall.spec).val().located(placement.build(wall.spec.local_to_parent))
            # Each edge physically occupies a wall's removed groove volume.
            assert floor.intersect(blank).Volume() > 1000
        # With all walls assembled, the floor cannot be extracted in any axis.
        walls = cq.Compound.makeCompound([parts[key] for key in ("left","right","front","back")])
        for translation in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)):
            assert floor.translate(translation).intersect(walls).Volume() > 1
        assert not any(j.source_part_id=="bottom" or j.target_part_id=="bottom" for j in built.joints)

    def test_wall_connector_pockets_remain_above_floor_and_edge_flush(self, drawer):
        _, built = drawer
        parts = {p.spec.part_id:p for p in built.parts}
        placement = LocalToParentLocation()
        floor = self.placed_parts(built)["bottom"]
        for joint in built.joints:
            if joint.source_part_id=="rail":
                continue
            source = parts[joint.source_part_id]
            blank = PanelBlankBuilder().build(source.spec).val()
            for cut in (c for c in built.cuts if c.joint_id==joint.joint_id and c.part_id==source.spec.part_id):
                pocket = cut.cutter.located(cut.location).intersect(blank)
                local = pocket.BoundingBox()
                edge = local.xmin if joint.source_edge=="<X" else local.xmax-source.spec.local_size_mm[0]
                assert edge == pytest.approx(0, abs=1e-6)
                actual = pocket.located(placement.build(source.spec.local_to_parent))
                assert actual.BoundingBox().zmin-floor.BoundingBox().zmax >= 9.99
                assert actual.intersect(floor).Volume() == pytest.approx(0, abs=1e-6)

    def test_lower_support_touches_floor_and_leaves_clip_pilot_material(self, drawer):
        _, built = drawer
        parts = self.placed_parts(built)
        support = parts["rail"].BoundingBox()
        bottom = parts["bottom"].BoundingBox()
        assert support.zmin==pytest.approx(0)
        assert support.zmax==bottom.zmin==pytest.approx(14.5)
        assert bottom.zmax-bottom.zmin==pytest.approx(16)
        operations = {op.machining_id:op for op in built.spec.machining}
        assert all(support.zlen-hole.depth_mm >= 4.5 for hole in operations["locking_clips"].holes)
        # The hook axes stay at global height 11, diameter 6; groove starts at 14.5.
        rear = operations["rear_hooks"]
        assert [(h.x_mm,h.y_mm,h.diameter_mm,h.depth_mm) for h in rear.holes]==[
            (7,-10.5,6,16),(660,-10.5,6,16)]

    def test_missing_retaining_groove_fails_construction_requirement(self, drawer):
        root, built = drawer
        for wall in ("left","right","front","back"):
            changed = replace(built,spec=replace(built.spec,machining=tuple(
                op for op in built.spec.machining if op.machining_id!="bottom_groove_"+wall)))
            visits = GeneratedAssemblyBuilderLoader().walk(root,changed)
            problems = ConstructionRequirementChecker().check(visits)[0].problems
            assert any("panel_connections" in problem and "required operation is missing" in problem
                       for problem in problems)

    def test_unmachined_floor_has_explicit_qualification_without_fake_cut_coverage(self, drawer):
        root, built = drawer
        checks = ConstructionRequirementChecker().check(GeneratedAssemblyBuilderLoader().walk(root,built))
        problems = checks[0].problems
        assert not any("panel_connections" in problem for problem in problems)
        assert any("captured_floor_fit: unresolved construction requirement" in problem for problem in problems)

    @pytest.mark.parametrize("height", (100,400,1000))
    def test_small_and_tall_boxes_keep_clearance_and_bounded_corner_spacing(self, drawer, height):
        root, _ = drawer
        built = GeneratedProjectModuleRuntime().execute(root,partial(self.build_height,height))
        self.test_wall_connector_pockets_remain_above_floor_and_edge_flush((root,built))
        assert all(part["allowed_faces"] for part in PanelSetupChecker().check(built)["parts"])
        for joint in built.joints:
            positions=joint.connector_positions_mm
            assert all(b-a<=300 for a,b in zip(positions,positions[1:]))

    def build_height(self, height):
        from assemblies.panel_assembly import PanelAssemblyBuilder
        dimensions=MoventoPanelDimensions(709,height,724,height+40,-1,-32,20,"ply16","prepared14.5","front20")
        spec=MoventoPanelDrawer().specification("drawer_01",dimensions,
            MoventoPilotChoice(5,14,2.5,10,"Unqualified test preparation"))
        return PanelAssemblyBuilder(spec).build()
