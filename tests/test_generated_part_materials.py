"""Scope: Prove selected stock survives standard generation into inventory and checks."""

from dataclasses import replace
import importlib
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from assembly_taxonomy_writer import AssemblyTaxonomyConflict
from construction_requirement_checker import ConstructionRequirementChecker
from generated_project_module_runtime import GeneratedProjectModuleRuntime
from generated_file_record import GeneratedFileRecord
from physical_item_counter import PhysicalItemCounter
from part_material_resolver import PartMaterialResolver
from overall_wardrobe_inputs import OverallWardrobeInputError
from design_decisions import DesignDecisionReader


class TestGeneratedPartMaterials:
    def setup_method(self):
        self.project = yaml.safe_load((Path(__file__).parent /
            "fixtures/four-unit-review-aikea.yaml").read_text())
        self.choices = {
            "cabinet_carcass_material": "Selected birch plywood, clear finish",
            "door_front_material": "Selected MDF, white paint",
            "back_panel_material": "Selected HDF",
        }
        for decision in self.project["design_decisions"]:
            decision["decision"] = self.choices[decision["subject"]]
        self.generator = AssemblyTaxonomyGenerator()

    def _specs(self, root, taxonomy):
        # Callback executes in the generated project's isolated import namespace.
        def read_specs():
            return [importlib.import_module(f"assemblies.{a.assembly_id}.spec").SPEC
                    for a in taxonomy.assemblies]
        return GeneratedProjectModuleRuntime().execute(root, read_specs)

    def test_selected_stock_reaches_all_parts_inventory_and_identity_gate(self, tmp_path):
        taxonomy = self.generator.generate(self.project, tmp_path)
        visits = []
        for spec in self._specs(tmp_path, taxonomy):
            for part in spec.parts:
                expected = {"door_panel": self.choices["door_front_material"],
                            "back_panel": self.choices["back_panel_material"]}.get(
                                part.role, self.choices["cabinet_carcass_material"])
                assert part.material_id == expected
                visits.append(SimpleNamespace(path=("wardrobe_01", spec.assembly_id,
                    "part:" + part.part_id), part=SimpleNamespace(spec=part)))
        assert {v.part.spec.role for v in visits} >= {
            "side_panel", "shelf_panel", "top_panel", "base_deck", "base_kickboard",
            "door_panel", "back_panel"}
        identity = ConstructionRequirementChecker().check(visits)[1]
        assert identity.passed
        inventory = PhysicalItemCounter().count(visits)
        assert not any(row["code"] == "part.material_missing" for row in inventory["unresolved"])
        assert {row["material_id"] for row in inventory["manufactured_parts"]} == set(self.choices.values())
        # Stock identity alone must not claim complete construction or fabrication.
        assert not ConstructionRequirementChecker().check(visits)[0].passed
        assert inventory["status"] == "draft"

    def test_material_revision_changes_saved_stock_without_changing_geometry(self, tmp_path):
        first = self.generator.generate(self.project, tmp_path)
        for choice in self.project["design_decisions"]:
            if choice["subject"] == "cabinet_carcass_material":
                choice["decision"] = "Replacement moisture-resistant MDF"
        second = self.generator.generate(self.project, tmp_path)
        for before, after in zip(first.assemblies, second.assemblies):
            assert before.joints == after.joints
            for old, new in zip(before.parts, after.parts):
                assert replace(new, material_id=old.material_id) == old
        specs = self._specs(tmp_path, second)
        assert specs[-1].parts[0].material_id == "Replacement moisture-resistant MDF"
        assert specs[0].part("door_panel").material_id == self.choices["door_front_material"]

    def test_explicit_part_override_is_preserved(self, tmp_path):
        taxonomy = self.generator.resolver.resolve(self.project)
        assembly = taxonomy.assemblies[0]
        panel = replace(assembly.parts[0], material_id="Explicit exceptional stock")
        taxonomy = replace(taxonomy, assemblies=(replace(assembly,
            parts=(panel, *assembly.parts[1:])), *taxonomy.assemblies[1:]))
        decisions = DesignDecisionReader().read(self.project, [])
        resolved = PartMaterialResolver().resolve(taxonomy, decisions)
        assert resolved.assemblies[0].parts[0] == panel

    def test_local_material_edit_is_not_overwritten(self, tmp_path):
        self.generator.generate(self.project, tmp_path)
        path = tmp_path / "assemblies/tall_storage_01/spec.py"
        edited = path.read_text().replace(self.choices["cabinet_carcass_material"], "Local stock override")
        path.write_text(edited)
        with pytest.raises(AssemblyTaxonomyConflict):
            self.generator.generate(self.project, tmp_path)
        assert path.read_text() == edited

    def test_untouched_previous_specs_gain_materials_from_generation_record(self, tmp_path):
        taxonomy = self.generator.resolver.resolve(self.project)
        files = self.generator.renderer.render(taxonomy)
        # The previous generator emitted exactly these specs without material_id.
        previous = {path: "".join(line for line in text.splitlines(keepends=True)
                    if not line.startswith("            material_id="))
                    for path, text in files.items()}
        self.generator.writer.write(tmp_path, previous)
        GeneratedFileRecord.from_rendered(previous).save(tmp_path)
        old_specs = self._specs(tmp_path, taxonomy)
        assert all(not p.material_id for spec in old_specs for p in spec.parts)
        self.generator.generate(self.project, tmp_path)
        assert all(p.material_id for spec in self._specs(tmp_path, taxonomy) for p in spec.parts)

    def test_missing_choice_is_not_invented(self, tmp_path):
        self.project["design_decisions"].pop()
        with pytest.raises(OverallWardrobeInputError, match="confirmed material decision"):
            self.generator.generate(self.project, tmp_path)
        assert not (tmp_path / "assemblies").exists()
