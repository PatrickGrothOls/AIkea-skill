"""Scope: Prove base recipes and authored parents share construction and missing-work checks."""

from dataclasses import replace
import importlib
from pathlib import Path

import pytest
import yaml

from assembly_joint_machining_builder import AssemblyJointMachiningBuilder
from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from construction_requirement_checker import ConstructionRequirementChecker
from construction_tree_checker import ConstructionTreeChecker
from generated_project_module_runtime import GeneratedProjectModuleRuntime
from physical_item_counter import PhysicalItemCounter
from sheet_part_builder import SheetPartBuilder


class TestConfiguredBaseConstruction:
    @pytest.fixture(scope="class")
    def base(self, tmp_path_factory):
        root = tmp_path_factory.mktemp("configured-base")
        project = yaml.safe_load((Path(__file__).parent / "fixtures/review-unit-aikea.yaml").read_text())
        AssemblyTaxonomyGenerator().generate(project, root)
        return GeneratedProjectModuleRuntime().execute(root, self._build)

    def _build(self):
        values = importlib.import_module("assemblies.specification")
        panels = importlib.import_module("assemblies.panel_assembly")
        tree = importlib.import_module("assemblies.assembly_tree").AssemblyTreeWalker()
        configured = importlib.import_module("assemblies.base_01.builder").BUILDER.build()
        spec = configured.spec
        cuts = AssemblyJointMachiningBuilder().build(spec, spec.joints)
        legacy = values.BuiltAssembly(spec, tuple(
            values.BuiltPart(part, SheetPartBuilder().build(part, cuts.for_part(part.part_id)))
            for part in spec.parts), spec.joints, cuts.all)
        direct = panels.PanelAssemblySpec(spec.assembly_id, "authored platform", spec.parts, spec.joints,
                                         machining=spec.machining, requirements=spec.requirements)
        custom = panels.PanelAssemblyBuilder(direct, allow_unresolved=True).build()
        part_view = importlib.import_module("assemblies.base_01.parts.brace_01_01.builder").BUILDER.build()
        return values, panels, tree, configured, legacy, custom, part_view

    def test_preserves_existing_geometry_cuts_and_individual_part_access(self, base):
        _, _, _, configured, legacy, custom, part_view = base
        assert configured.spec.width_mm == pytest.approx(2978)
        assert configured.spec.machining == ()
        assert len(configured.parts) == len(custom.parts) == len(legacy.parts) == 19
        for built in (configured, custom):
            assert built.joints == legacy.joints
            assert [(cut.joint_id, cut.part_id, cut.connector_index) for cut in built.cuts] == [
                (cut.joint_id, cut.part_id, cut.connector_index) for cut in legacy.cuts]
            for actual, expected in zip(built.parts, legacy.parts):
                assert actual.spec == expected.spec
                self._same_solid(actual.solid, expected.solid)
        self._same_solid(part_view.solid, next(part.solid for part in configured.parts
                                             if part.spec.part_id == part_view.spec.part_id))

    def test_counts_and_unresolved_work_are_identical(self, base):
        _, _, tree, configured, legacy, custom, _ = base
        reports = [PhysicalItemCounter().count(tree.walk(built)) for built in (configured, legacy, custom)]
        assert reports[0] == reports[1] == reports[2]
        assert any(item["code"] == "joint.unresolved" for item in reports[0]["unresolved"])
        checker = ConstructionRequirementChecker()
        assert checker.check(tree.walk(configured)) == checker.check(tree.walk(custom))
        assert all(check.passed for check in ConstructionTreeChecker().check(tree.walk(custom))
                   if check.code == "construction.applied_operations")

    def test_removing_connection_leaves_its_independent_requirement_unfulfilled(self, base):
        _, panels, tree, _, _, custom, _ = base
        joint = next(joint for joint in custom.joints if joint.joint_type == "cabineo")
        spec = replace(custom.spec, joints=tuple(item for item in custom.joints if item != joint))
        changed = panels.PanelAssemblyBuilder(spec, allow_unresolved=True).build()
        problems = ConstructionRequirementChecker().check(tree.walk(changed))[0].problems
        assert any(f"requirement:{joint.joint_id}: required operation is missing" in item for item in problems)

    def test_custom_parent_and_renamed_panel_need_no_new_recipe_or_machining(self, base):
        values, panels, tree, _, _, custom, _ = base
        deck = custom.spec.part("deck_01")
        spec = replace(custom.spec, parts=tuple(replace(part, role="custom_platform_top") if part == deck else part
                                                for part in custom.spec.parts))
        adapted = panels.PanelAssemblyBuilder(spec, allow_unresolved=True).build()
        placement = values.LocalToParentPlacement(values.Point3D(100, 300, 200), values.AxisBasis(
            values.AxisDirection(0, 1, 0), values.AxisDirection(-1, 0, 0), values.AxisDirection(0, 0, 1)))
        child = values.ChildAssemblySpec(spec.assembly_id, spec.purpose, placement)
        owner = values.CompositeAssemblySpec("custom_01", "independent layout", (child,), requirements=())
        nested = values.BuiltAssembly(owner, (), (), child_assemblies=(values.BuiltChildAssembly(child, adapted),))
        visits = tree.walk(nested)
        assert visits[1].local_to_root == placement
        self._same_solid(adapted.parts[0].solid, custom.parts[0].solid)
        assert len(adapted.cuts) == len(custom.cuts)
        assert not any(item["code"] == "cut.unknown_joint" for item in PhysicalItemCounter().count(visits)["unresolved"])

    def _same_solid(self, actual, expected):
        assert actual.val().cut(expected.val()).Volume() == pytest.approx(0, abs=1e-5)
        assert expected.val().cut(actual.val()).Volume() == pytest.approx(0, abs=1e-5)
