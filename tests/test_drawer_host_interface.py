"""Scope: Exercise existing drawer recipes in authored bays using real support frames."""

from dataclasses import replace
from pathlib import Path

import pytest
import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from cabinet_assembly_spec_loader import CabinetAssemblySpecLoader
from cabinet_drawer_plan import CabinetDrawerPlanner, DrawerLayout
from drawer_host import DrawerHost, DrawerHostSpec
from drawer_host_loader import DrawerHostLoader
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from hettich_ka_4532_spacer_cabinet_drawer_planner import HettichKa4532SpacerCabinetDrawerPlanner
from hettich_ka_4532_spacer_mounting_test_support import HettichKa4532SpacerMountingTestSupport
from hettich_ka_5332_cabinet_drawer_generator import HettichKa5332CabinetDrawerGenerator
from hettich_ka_5332_cabinet_drawer_plan import HettichKa5332CabinetDrawerPlanner
from hettich_ka_5332_host_drilling_recipe import HettichKa5332HostDrillingRecipe
from hettich_ka_5332_test_support import HettichKa5332StepAssemblyLoaderTestDouble, TEST_HETTICH_HARDWARE_DIRECTORY
from physical_item_counter import PhysicalItemCounter


class TestDrawerHostInterface:
    @pytest.fixture
    def host(self, tmp_path):
        project = yaml.safe_load((Path(__file__).parent / "fixtures/four-unit-review-aikea.yaml").read_text())
        (tmp_path / "aikea.yaml").write_text(yaml.safe_dump(project))
        AssemblyTaxonomyGenerator().generate(project, tmp_path)
        original = CabinetAssemblySpecLoader().load(tmp_path, "tall_storage_01")
        names = {"left_side": "support_a", "right_side": "support_b"}
        parts = []
        for name, renamed in names.items():
            part = original.part(name)
            point = part.local_to_parent.origin_in_parent
            location = replace(part.local_to_parent, origin_in_parent=replace(point, x_mm=point.x_mm+100, y_mm=point.y_mm+50, z_mm=point.z_mm+32))
            parts.append(replace(part, part_id=renamed, role="support", local_to_parent=location, material_id="mdf"))
        requests = tuple(replace(item, part_id=names[item.part_id]) for item in original.machining if item.part_id in names)
        declaration = DrawerHostSpec("support_a", "support_b", 50, original.inside_depth_mm,
                                    original.base_height_mm+32, original.base_height_mm+800+32)
        root = tmp_path / "assemblies/niche_01"
        root.mkdir()
        (root / "__init__.py").write_text('"""Scope: Own one custom drawer bay."""\n')
        (root / "spec.py").write_text('"""Scope: Declare custom supports and their drawer opening."""\n'
            "from assemblies.specification import *\nfrom assemblies.panel_assembly import PanelAssemblySpec\n"
            "from drawer_host import DrawerHostSpec\n"
            f"SPEC = PanelAssemblySpec('niche_01', 'custom bay', {tuple(parts)!r}, machining={requests!r}, requirements=())\n"
            f"DRAWER_HOST = {declaration!r}\n")
        (root / "builder.py").write_text('"""Scope: Build the declared custom panels."""\n'
            "from assemblies.panel_assembly import PanelAssemblyBuilder\nfrom .spec import SPEC\nBUILDER = PanelAssemblyBuilder(SPEC)\n")
        return tmp_path, original, DrawerHostLoader().load(tmp_path, "niche_01")

    @pytest.mark.parametrize("runner", ["movento", "ka5332", "ka4532"])
    def test_existing_recipes_use_translated_custom_faces_and_keep_dimensions(self, host, runner):
        _, original, custom = host
        layout = DrawerLayout("drawer_01", 100)
        before, after = self._plan(original, layout, runner), self._plan(custom, layout, runner)
        assert after.parent_assembly_id == "niche_01"
        assert after.drawer.box.outside_width_mm == pytest.approx(before.drawer.box.outside_width_mm)
        assert after.drawer.box.outside_depth_mm == before.drawer.box.outside_depth_mm
        assert after.origin_in_parent_mm == pytest.approx(tuple(value+delta for value, delta in zip(before.origin_in_parent_mm, (100, 50, 32))))
        if runner != "movento":
            assert {item.side_part_id for item in after.hardware_reservations} == {"support_a", "support_b"}

    def test_saved_custom_parent_builds_one_drawer_and_reconciles_purchases(self, host):
        root, _, _ = host
        HettichKa5332CabinetDrawerGenerator(HettichKa5332StepAssemblyLoaderTestDouble()).generate(
            root, "niche_01", DrawerLayout("drawer_01", 100), hardware_directory=TEST_HETTICH_HARDWARE_DIRECTORY)
        loader = GeneratedAssemblyBuilderLoader()
        built = loader.load_assembly(root, "niche_01")
        assert len(built.child_assemblies) == 1 and len(built.purchased_hardware) == 2
        assert {request.part_id for request in built.spec.machining} == {"support_a", "support_b"}
        report = PhysicalItemCounter().count(loader.walk(root, built))
        assert len(report["manufactured_parts"]) == 7
        assert not any(item["code"] == "cut.unknown_joint" for item in report["unresolved"])

    def test_differing_panel_bottoms_still_share_one_real_mounting_height(self, host):
        _, _, custom = host
        right = custom.part("right")
        frame = right.local_to_parent
        changed = replace(right, local_to_parent=replace(frame, origin_in_parent=replace(frame.origin_in_parent, z_mm=frame.origin_in_parent.z_mm+32)))
        owner = replace(custom.assembly, parts=(custom.part("left"), changed))
        moved = DrawerHost(owner, custom.spec)
        plan = self._plan(moved, DrawerLayout("drawer_01", 100), "ka5332")
        requests = HettichKa5332HostDrillingRecipe().build(moved, (plan,))
        left, right = plan.hardware_reservations
        assert left.system_32_node_rows_mm[0] - right.system_32_node_rows_mm[0] == 32
        world = []
        for side, request in zip(("left", "right"), requests):
            hole = request.holes[0]
            world.append(moved.frame(side).to_owner((hole.x_mm, moved.part(side).local_size_mm[1]-hole.y_mm, moved.part(side).local_size_mm[2]))[2])
        assert world[0] == pytest.approx(world[1])

    def test_missing_or_inverted_supports_and_shallow_space_fail(self, host):
        _, _, custom = host
        with pytest.raises(ValueError, match="must be owned"):
            DrawerHost(custom.assembly, replace(custom.spec, left_part_id="missing"))
        with pytest.raises(ValueError, match="opposing"):
            DrawerHost(custom.assembly, replace(custom.spec, left_part_id="support_b", right_part_id="support_a"))
        shallow = DrawerHost(custom.assembly, replace(custom.spec, inside_depth_mm=400))
        with pytest.raises(ValueError):
            self._plan(shallow, DrawerLayout("drawer_01", 100, box_depth_mm=500), "ka5332")

    def _plan(self, host, layout, runner):
        if runner == "movento":
            return CabinetDrawerPlanner().plan(host, layout)
        if runner == "ka5332":
            return HettichKa5332CabinetDrawerPlanner().plan(host, layout,
                HettichKa5332StepAssemblyLoaderTestDouble().load(TEST_HETTICH_HARDWARE_DIRECTORY))
        resolved = DrawerHost.resolve(host)
        return HettichKa4532SpacerCabinetDrawerPlanner().plan(host, layout,
            HettichKa4532SpacerMountingTestSupport().step_set(),
            cabinet_front_mm=resolved.spec.front_mm, drawer_front_mm=resolved.spec.front_mm+18)
