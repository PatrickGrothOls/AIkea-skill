"""Scope: Verify hinge recipe geometry, paired machining and exact owned purchases."""

from dataclasses import asdict, replace
import importlib
from math import pi
from pathlib import Path

import pytest
import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from assembly_taxonomy_writer import AssemblyTaxonomyConflict
from cabinet_assembly_spec_loader import CabinetAssemblySpecLoader
from cabinet_door_feature_generator import CabinetDoorFeatureGenerator
from concealed_hinge_machining import ConcealedHingeMachining
from construction_result_validator import ConstructionResultValidator
from door_hinge_plan import DoorHingePlanner
from door_hinge_side import DoorHingeSide
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from generated_project_module_runtime import GeneratedProjectModuleRuntime
from panel_machining_feature import PanelMachiningFeature
from physical_item_counter import PhysicalItemCounter
from riex_nc70_hinge_profile import RIEX_NC70_FULL_OVERLAY
from riex_nc70_machining_recipe import RiexNc70MachiningRecipe


class TestDoorConstructionMachining:
    @pytest.fixture
    def project(self, tmp_path):
        project = yaml.safe_load((Path(__file__).parent/'fixtures/four-unit-review-aikea.yaml').read_text())
        (tmp_path/'aikea.yaml').write_text(yaml.safe_dump(project))
        AssemblyTaxonomyGenerator().generate(project, tmp_path)
        return tmp_path, CabinetAssemblySpecLoader().load(tmp_path, "tall_storage_01")

    @pytest.mark.parametrize("hand", (DoorHingeSide.LEFT, DoorHingeSide.RIGHT))
    def test_official_build_matches_cup_geometry_reuses_grid_and_counts_purchases(self, project, hand):
        root, spec = project
        loader = GeneratedAssemblyBuilderLoader()
        before = loader.load_assembly(root, spec.assembly_id)
        plan = self._plan(spec, hand)
        expected = ConcealedHingeMachining().apply(before, plan, RIEX_NC70_FULL_OVERLAY)
        plan.write(root/f'assemblies/{spec.assembly_id}/door_hinges/installation.json')
        generator = CabinetDoorFeatureGenerator()
        generator.generate(root, spec, plan, RIEX_NC70_FULL_OVERLAY)
        generator.generate(root, spec, plan, RIEX_NC70_FULL_OVERLAY)
        built = loader.load_assembly(root, spec.assembly_id)
        parts = {part.spec.part_id: part for part in built.parts}
        for name, expected_part in (("door_panel", expected.door), (hand.side_part_id, expected.cabinet_side)):
            shape, previous = parts[name].solid.val(), expected_part.val()
            assert shape.cut(previous).Volume()+previous.cut(shape).Volume() < 1e-5
        restored = loader.load_assembly(root, spec.assembly_id, exclude_features=("door_hinges.feature",))
        assert len(restored.cuts) == len(before.cuts)
        # Generated modules reload their dataclass types; compare saved values.
        assert tuple(asdict(item.spec) for item in restored.purchased_hardware) == tuple(
            asdict(item.spec) for item in before.purchased_hardware)
        for actual, original in zip(restored.purchased_hardware, before.purchased_hardware):
            assert actual.has_geometry == original.has_geometry
            if actual.has_geometry:
                left, right = actual.solid.val(), original.solid.val()
                assert left.cut(right).Volume()+right.cut(left).Volume() < 1e-5
        fresh_plan = self._plan(restored.spec, hand)
        generator.generate(root, restored.spec, fresh_plan, RIEX_NC70_FULL_OVERLAY)
        built = loader.load_assembly(root, spec.assembly_id)
        parts = {part.spec.part_id: part for part in built.parts}
        requests = built.spec.machining[-2:]
        door_before = next(part.solid.val() for part in before.parts if part.spec.part_id == 'door_panel')
        removed_volume = door_before.Volume()-parts['door_panel'].solid.val().Volume()
        assert removed_volume == pytest.approx(pi*17.5**2*12+2*pi*1.25**2*10)
        assert len(requests[0].holes) == 3 and len(requests[1].holes) == 2
        assert requests[1].reuse_machining_ids
        assert len(built.cuts) == len(before.cuts)+2
        assert len(built.parts) == len(before.parts) and built.child_assemblies == before.child_assemblies
        assert {item.spec.product_code for item in built.purchased_hardware} == (
            {"F000001", "F000049"} | {item.spec.product_code for item in before.purchased_hardware})
        report = PhysicalItemCounter().count(loader.walk(root, built))
        assert len(report["manufactured_parts"]) == len(before.parts)
        assert {item.requirement_id for item in built.spec.requirements} >= {"door_hinge_installation", "door_fixing_pilots"}

    def test_missing_plate_holes_are_cut_and_out_of_bounds_cup_is_rejected(self, project):
        root, spec = project
        module = GeneratedProjectModuleRuntime().execute(root, lambda: importlib.import_module('assemblies.panel_assembly'))
        spec = replace(spec, joints=(), machining=(), requirements=())
        before = module.PanelAssemblyBuilder(spec).build()
        plan = self._plan(spec, DoorHingeSide.LEFT)
        requests = RiexNc70MachiningRecipe().build(spec, plan, RIEX_NC70_FULL_OVERLAY)
        assert not requests[1].reuse_machining_ids
        built = PanelMachiningFeature().apply(before, requests)
        left = next(part.solid.val() for part in before.parts if part.spec.part_id == 'left_side')
        changed = next(part.solid.val() for part in built.parts if part.spec.part_id == 'left_side')
        assert left.Volume()-changed.Volume() == pytest.approx(2*pi*2.5**2*13)
        ConstructionResultValidator().validate(built)
        original = plan.placements[0]
        delta = 5-original.door_height_mm
        shifted = replace(plan, placements=(replace(original, door_height_mm=5,
            cabinet_height_mm=original.cabinet_height_mm+delta,
            cabinet_fixing_rows_mm=tuple(row+delta for row in original.cabinet_fixing_rows_mm)),))
        requests = RiexNc70MachiningRecipe().build(spec, shifted, RIEX_NC70_FULL_OVERLAY)
        with pytest.raises(ValueError):
            PanelMachiningFeature().apply(before, requests)

    def test_local_machining_edits_are_preserved_on_regeneration(self, project):
        root, spec = project
        plan = self._plan(spec, DoorHingeSide.LEFT)
        generator = CabinetDoorFeatureGenerator()
        generator.generate(root, spec, plan, RIEX_NC70_FULL_OVERLAY)
        path = root/f'assemblies/{spec.assembly_id}/door_hinges/machining.py'
        authored = path.read_text()+'# Authored change retained.\n'
        path.write_text(authored)
        with pytest.raises(AssemblyTaxonomyConflict):
            generator.generate(root, spec, plan, RIEX_NC70_FULL_OVERLAY)
        assert path.read_text() == authored

    def _plan(self, spec, hand):
        plan = DoorHingePlanner().plan(spec, RIEX_NC70_FULL_OVERLAY, hand)
        return replace(plan, placements=plan.placements[:1])
