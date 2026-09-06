"""Scope: Generate and load isolated assembly composition test contracts."""

from __future__ import annotations

from dataclasses import dataclass
import importlib
import sys

import pytest

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from overall_wardrobe_test_project import OverallWardrobeTestProject


class AssemblyCompositionTestCase:
    """Provide one generated project contract to each composition test."""

    @pytest.fixture
    def generated_values(self, tmp_path):
        data = OverallWardrobeTestProject().load_flat()
        run = data["design_settings"].pop("cabinet_run")
        data["design_settings"]["assembly_run"] = {
            "left_clearance": run["left_clearance"],
            "right_clearance": run["right_clearance"],
            "gap": run["cabinet_gap"],
            "ceiling_clearance": run["ceiling_clearance"],
            "assemblies": [
                {
                    "id": "tall_storage_01",
                    "purpose": "tall_storage",
                    "width_share": 1,
                }
            ],
        }
        AssemblyTaxonomyGenerator().generate(data, tmp_path)
        sys.path.insert(0, str(tmp_path))
        try:
            yield importlib.import_module("assemblies.specification"), tmp_path
        finally:
            sys.path.remove(str(tmp_path))
            for name in tuple(sys.modules):
                if name == "assemblies" or name.startswith("assemblies."):
                    sys.modules.pop(name)

    def fixture_assembly_spec(
        self,
        assembly_id: str,
        purpose: str,
        child_assemblies: tuple,
        purchased_hardware: tuple,
        parts: tuple = (),
    ):
        @dataclass(frozen=True)
        class FixtureAssemblySpec:
            assembly_id: str
            purpose: str
            child_assemblies: tuple
            purchased_hardware: tuple
            parts: tuple = ()

        return FixtureAssemblySpec(
            assembly_id,
            purpose,
            child_assemblies,
            purchased_hardware,
            parts,
        )
