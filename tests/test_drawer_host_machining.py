"""Scope: Verify declared runner mounting preserves old geometry and composes on authored panels."""

from dataclasses import replace
import importlib
from pathlib import Path

import pytest
import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from cabinet_drawer_plan import DrawerLayout
from construction_requirement_checker import ConstructionRequirementChecker
from construction_result_validator import ConstructionResultValidator
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from generated_project_module_runtime import GeneratedProjectModuleRuntime
from hettich_ka_5332_cabinet_drawer_generator import HettichKa5332CabinetDrawerGenerator
from hettich_ka_5332_host_drilling_recipe import HettichKa5332HostDrillingRecipe
from hettich_ka_5332_panel_machining import HettichKa5332PanelMachining
from hettich_ka_5332_test_support import HettichKa5332StepAssemblyLoaderTestDouble, TEST_HETTICH_HARDWARE_DIRECTORY
from panel_machining_feature import PanelMachiningFeature
from surface_drilling_spec import SurfaceDrillingSpec
from surface_hole_pattern import SurfaceHole


class TestDrawerHostMachining:
    @pytest.fixture(scope="class")
    def generated(self, tmp_path_factory):
        tmp_path = tmp_path_factory.mktemp("drawer-host")
        project = yaml.safe_load((Path(__file__).parent / "fixtures/four-unit-review-aikea.yaml").read_text())
        (tmp_path / "aikea.yaml").write_text(yaml.safe_dump(project))
        AssemblyTaxonomyGenerator().generate(project, tmp_path)
        result = HettichKa5332CabinetDrawerGenerator(HettichKa5332StepAssemblyLoaderTestDouble()).generate(
            tmp_path, "tall_storage_01", DrawerLayout("drawer_01", 356),
            hardware_directory=TEST_HETTICH_HARDWARE_DIRECTORY)
        return tmp_path, result.plan, GeneratedProjectModuleRuntime().execute(tmp_path, self._load)

    def _load(self):
        package = "assemblies.tall_storage_01"
        base = importlib.import_module(package + ".builder").BUILDER.build()
        installation = importlib.import_module(package + ".drawer_installation")
        composed = importlib.import_module(package + ".drawers.feature").FEATURE.apply(base)
        return base, composed, installation, importlib.import_module("assemblies.panel_assembly")

    def test_saved_host_cutters_match_previous_geometry_and_are_independently_checked(self, generated):
        _, plan, (base, composed, installation, _) = generated
        previous = HettichKa5332PanelMachining(plan.runner).cabinet_parts(base.parts, (plan.hardware_mounting.system_32_row_height_mm,))
        self._same_parts(composed.parts, previous)
        assert len(composed.cuts) == len(base.cuts) + 2
        assert all(request.reuse_machining_ids for request in installation.HOST_MACHINING)
        assert ConstructionResultValidator().validate(composed) == ()
        assert len(composed.child_assemblies) == 1
        prior = tuple(item.spec for item in base.purchased_hardware)
        assert tuple(item.spec for item in composed.purchased_hardware[:len(prior)]) == prior
        runners = composed.purchased_hardware[len(prior):]
        assert len(runners) == 2
        assert {item.spec.product_code for item in runners} == {"9057405"}

    def test_missing_host_operations_leave_saved_requirements_unresolved(self, generated):
        root, _, (base, _, installation, _) = generated
        changed = PanelMachiningFeature().apply(base, (), installation.HOST_REQUIREMENTS)
        visits = GeneratedAssemblyBuilderLoader().walk(root, changed)
        problems = ConstructionRequirementChecker().check(visits)[0].problems
        assert any("drawer_01_left_side_fixings" in problem and "required operation is missing" in problem for problem in problems)

    def test_same_feature_works_on_renamed_authored_panels_and_removal_preserves_prior_work(self, generated):
        _, _, (base, _, installation, panels) = generated
        names = {"left_side": "bay_wall_a", "right_side": "bay_wall_b"}
        parts = tuple(replace(part.spec, part_id=names[part.spec.part_id], role="authored support")
                      for part in base.parts if part.spec.part_id in names)
        grid = tuple(replace(request, part_id=names[request.part_id]) for request in base.spec.machining if request.part_id in names)
        spec = panels.PanelAssemblySpec("bench_01", "authored bay", parts, machining=grid, requirements=())
        blank = panels.PanelAssemblyBuilder(spec).build()
        requests = tuple(replace(request, part_id=names[request.part_id]) for request in installation.HOST_MACHINING)
        first = requests[0]
        other = replace(first, machining_id="independent_hole", holes=(SurfaceHole("access", 450, 40, 4, 8),), reuse_machining_ids=())
        retained = PanelMachiningFeature().apply(blank, (other,))
        installed = PanelMachiningFeature().apply(retained, requests)
        direct = panels.PanelAssemblyBuilder(replace(spec, machining=grid+(other,)+requests)).build()
        self._same_parts(installed.parts, direct.parts)
        self._same_parts(retained.parts, PanelMachiningFeature().apply(blank, (other,)).parts)
        assert [cut.joint_id for cut in installed.cuts] == [cut.joint_id for cut in direct.cuts]
        assert len(retained.spec.machining) + 2 == len(installed.spec.machining)
        assert ConstructionResultValidator().validate(installed) == ()

    def test_recipe_uses_selected_profile_and_unassessed_parent_stays_unassessed(self, generated):
        _, plan, (base, _, installation, _) = generated
        profile = replace(plan.runner, cabinet_fixing_positions_from_front_mm=(37, 150, 250))
        requests = HettichKa5332HostDrillingRecipe().build(base.spec, (replace(plan, runner=profile),))
        assert tuple(hole.x_mm for hole in requests[0].holes) == (37, 150, 250)
        assert tuple(hole.x_mm for hole in requests[1].holes) == tuple(base.spec.part("right_side").local_size_mm[0]-x for x in (37, 150, 250))
        unknown = replace(base, spec=replace(base.spec, requirements=None))
        assert PanelMachiningFeature().apply(unknown, requests, installation.HOST_REQUIREMENTS).spec.requirements is None

    def _same_parts(self, left, right):
        assert [part.spec.part_id for part in left] == [part.spec.part_id for part in right]
        for a, b in zip(left, right):
            first, second = a.solid.val(), b.solid.val()
            assert first.cut(second).Volume() + second.cut(first).Volume() == pytest.approx(0, abs=1e-5)
