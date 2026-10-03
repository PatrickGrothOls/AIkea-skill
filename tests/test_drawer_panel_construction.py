"""Scope: Compare saved and directly authored drawer construction against existing fixing geometry."""

from dataclasses import asdict, replace
import importlib
from pathlib import Path
from types import SimpleNamespace

import pytest

from construction_requirement_checker import ConstructionRequirementChecker
from construction_result_validator import ConstructionResultValidator
from drawer_assembly_spec import DrawerAssemblySpec
from drawer_box_builder import DrawerBoxBuilder
from drawer_box_planner import DrawerBoxPlanner
from drawer_box_spec import CabinetDrawerOpening
from furniture_design_project import FurnitureDesignProject
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from generated_project_module_runtime import GeneratedProjectModuleRuntime
from hettich_ka_5332_drawer_box_profile import HettichKa5332DrawerBoxProfileAdapter
from hettich_ka_5332_panel_machining import HettichKa5332PanelMachining
from hettich_ka_5332_runner_profile import HETTICH_KA_5332_500
from physical_item_counter import PhysicalItemCounter
from wooden_drawer_child_module_renderer import WoodenDrawerChildModuleRenderer


class TestDrawerPanelConstruction:
    @pytest.fixture
    def drawer(self, tmp_path):
        profile = HETTICH_KA_5332_500
        sizing = HettichKa5332DrawerBoxProfileAdapter().build(profile, side_thickness_mm=16,
            front_back_thickness_mm=16, bottom_thickness_mm=9, bottom_underside_recess_mm=13, box_height_mm=160)
        box = DrawerBoxPlanner().plan(CabinetDrawerOpening(600, 570), sizing)
        box = replace(box, parts=tuple(replace(part, material_id="birch" if part.part_id == "bottom" else "mdf")
                                      for part in box.parts))
        spec = DrawerAssemblySpec("drawer_01", "drawer", profile.product_code, profile.item_number, "test_only", box)
        plan = SimpleNamespace(drawer=spec, runner=profile)
        FurnitureDesignProject().initialize(tmp_path)
        files = WoodenDrawerChildModuleRenderer().render(Path("assemblies/drawer_01"), plan)
        for name, source in files.items():
            target = tmp_path / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(source)
        built = GeneratedAssemblyBuilderLoader().load_assembly(tmp_path, "drawer_01")
        panels, values = GeneratedProjectModuleRuntime().execute(tmp_path, self._contracts)
        direct = panels.PanelAssemblySpec(built.spec.assembly_id, "authored drawer", built.spec.parts,
                                          machining=built.spec.machining, requirements=built.spec.requirements)
        custom = panels.PanelAssemblyBuilder(direct).build()
        reference = HettichKa5332PanelMachining(profile).drawer_box(DrawerBoxBuilder().build(box))
        return tmp_path, built, custom, reference, panels, values

    def _contracts(self):
        return importlib.import_module("assemblies.panel_assembly"), importlib.import_module("assemblies.specification")

    def test_generated_and_direct_drawer_keep_exact_legacy_holes_and_materials(self, drawer):
        _, built, custom, reference, _, _ = drawer
        for assembly in (built, custom):
            assert len(assembly.parts) == 5 and len(assembly.cuts) == 2
            assert len(assembly.spec.machining) == 2
            for actual, expected in zip(assembly.parts, reference.parts):
                assert asdict(actual.spec) == asdict(expected.spec)
                left, right = actual.solid.val(), expected.solid.val()
                assert left.cut(right).Volume() + right.cut(left).Volume() == pytest.approx(0, abs=1e-5)
            assert ConstructionResultValidator().validate(assembly) == ()
        assert built.spec.part("bottom").material_id == "birch"
        assert built.spec.part("left_side").material_id == "mdf"

    def test_requirements_survive_removed_drilling_and_joinery_remains_unresolved(self, drawer):
        root, built, custom, _, panels, _ = drawer
        walker = GeneratedAssemblyBuilderLoader()
        checks = ConstructionRequirementChecker().check(walker.walk(root, built))
        assert any("box_joinery" in problem and "unresolved" in problem for problem in checks[0].problems)
        changed = panels.PanelAssemblyBuilder(replace(custom.spec, machining=custom.spec.machining[1:])).build()
        problems = ConstructionRequirementChecker().check(walker.walk(root, changed))[0].problems
        assert any("runner_fixings" in problem and "required operation is missing" in problem for problem in problems)

    def test_custom_parent_preserves_one_physical_inventory_and_shared_checks(self, drawer):
        root, built, custom, _, _, values = drawer
        placement = values.LocalToParentPlacement(values.Point3D(100, 50, 200), values.IDENTITY_AXIS_BASIS)
        child = values.ChildAssemblySpec(custom.spec.assembly_id, custom.spec.purpose, placement)
        owner = values.CompositeAssemblySpec("niche_01", "custom parent", (child,), requirements=())
        nested = values.BuiltAssembly(owner, (), (), child_assemblies=(values.BuiltChildAssembly(child, custom),))
        visits = GeneratedAssemblyBuilderLoader().walk(root, nested)
        assert asdict(visits[1].local_to_root) == asdict(placement)
        report = PhysicalItemCounter().count(visits)
        assert len(report["manufactured_parts"]) == 5
        assert not any(item["code"] == "cut.unknown_joint" for item in report["unresolved"])
        assert ConstructionResultValidator().validate(custom) == ()
