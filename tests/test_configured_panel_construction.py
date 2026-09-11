"""Scope: Compare the cabinet recipe with legacy geometry and custom construction."""

from dataclasses import replace
import importlib
from pathlib import Path

import pytest
import yaml

from assembly_joint_machining_builder import AssemblyJointMachiningBuilder
from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from generated_project_module_runtime import GeneratedProjectModuleRuntime
from physical_item_counter import PhysicalItemCounter
from sheet_part_builder import SheetPartBuilder


class TestConfiguredPanelConstruction:
    """Use independent legacy construction as the cabinet migration reference."""

    @pytest.fixture(scope="class")
    def cabinet(self, tmp_path_factory):
        root = tmp_path_factory.mktemp("configured-panels")
        project = yaml.safe_load((Path(__file__).parent / "fixtures/review-unit-aikea.yaml").read_text())
        AssemblyTaxonomyGenerator().generate(project, root)
        return GeneratedProjectModuleRuntime().execute(root, self._build)

    def _build(self):
        values = importlib.import_module("assemblies.specification")
        panels = importlib.import_module("assemblies.panel_assembly")
        tree = importlib.import_module("assemblies.assembly_tree").AssemblyTreeWalker()
        configured = importlib.import_module("assemblies.tall_storage_01.builder").BUILDER.build()
        spec = configured.spec
        legacy_cuts = AssemblyJointMachiningBuilder().build(spec, spec.joints)
        legacy = values.BuiltAssembly(
            replace(spec, machining=()),
            tuple(values.BuiltPart(part, SheetPartBuilder().build(part, legacy_cuts.for_part(part.part_id)))
                  for part in spec.parts),
            spec.joints, legacy_cuts.all,
        )
        direct = panels.PanelAssemblySpec(
            spec.assembly_id, spec.purpose, spec.parts, spec.joints,
            spec.child_assemblies, spec.purchased_hardware, spec.machining,
        )
        custom = panels.PanelAssemblyBuilder(direct, allow_unresolved=True).build()
        return values, panels, tree, configured, legacy, custom

    def test_recipe_and_custom_preserve_legacy_solids(self, cabinet):
        _, _, _, configured, legacy, custom = cabinet
        # Measured 3000 minus 2 fit allowance, 20 wall gaps and two 2 mm unit gaps.
        assert configured.spec.width_mm == pytest.approx((3000 - 2 - 20 - 4) / 3)
        assert configured.spec.base_height_mm == 100
        assert len(configured.parts) == len(legacy.parts) == len(custom.parts) == 8
        for built in (configured, custom):
            for actual, expected in zip(built.parts, legacy.parts):
                assert actual.spec == expected.spec
                left, right = actual.solid.val(), expected.solid.val()
                assert left.cut(right).Volume() == pytest.approx(0, abs=1e-5)
                assert right.cut(left).Volume() == pytest.approx(0, abs=1e-5)
            assert built.joints == legacy.joints
            assert len(built.cuts) == len(legacy.cuts) + 2

    def test_inventory_retains_all_parts_connectors_and_unresolved_attachments(self, cabinet):
        _, _, tree, configured, legacy, custom = cabinet
        reports = [PhysicalItemCounter().count(tree.walk(built)) for built in (configured, legacy, custom)]
        for report in reports[1:]:
            assert report == reports[0]
        assert any(item["code"] == "joint.unresolved" for item in reports[0]["unresolved"])
        assert not any(item["code"] == "cut.unknown_joint" for item in reports[0]["unresolved"])

    def test_recipe_panel_can_be_notched_without_new_role_or_tool(self, cabinet):
        values, panels, _, configured, _, custom = cabinet
        shelf = custom.spec.part("shelf_01")
        width, depth, thickness = shelf.local_size_mm
        points = ((0, 0), (width / 2, 0), (width / 2, 20), (width, 20), (width, depth), (0, depth))
        adapted = replace(shelf, role="custom_niche_shelf", material_id="mdf",
                          outline_mm=tuple(values.BoundaryPoint(*point) for point in points))
        spec = replace(custom.spec, purpose="authored arrangement",
                       parts=tuple(adapted if part.part_id == shelf.part_id else part
                                   for part in custom.spec.parts))
        built = panels.PanelAssemblyBuilder(spec, allow_unresolved=True).build()
        result = next(part for part in built.parts if part.spec.part_id == shelf.part_id)
        assert result.solid.val().Volume() == pytest.approx((width * depth - width / 2 * 20) * thickness)
        assert result.spec.material_id == "mdf"
        assert configured.spec.part("shelf_01") == shelf
        assert built.joints == custom.joints
