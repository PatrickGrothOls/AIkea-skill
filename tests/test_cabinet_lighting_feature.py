"""Scope: Verify saved cabinet lighting registers as a composed feature."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from cabinet_lighting_generator import CabinetLightingGenerator
from lighting_run import LightingRun
from recessed_luminaire_profile import DOMUS_APEX_84_HI


class TestCabinetLightingFeature:
    """Protect lighting ownership without requiring CadQuery geometry."""

    _FIXTURE = Path(__file__).parent / "fixtures/four-unit-review-aikea.yaml"

    def test_registers_reusable_feature_and_compatibility_builder(self, tmp_path) -> None:
        project = yaml.safe_load(self._FIXTURE.read_text(encoding="utf-8"))
        AssemblyTaxonomyGenerator().generate(project, tmp_path)
        run = LightingRun(
            "shelf_light_01",
            (50.0, 200.0),
            (650.0, 200.0),
            3200,
            DOMUS_APEX_84_HI,
        )

        result = CabinetLightingGenerator().generate(
            tmp_path,
            "tall_storage_01",
            "top_panel_01",
            run,
            base_builder_module="builder",
        )

        root = tmp_path / "assemblies/tall_storage_01"
        assert (root / "lighting/feature.py").is_file()
        assert (root / "with_lighting_builder.py").is_file()
        compile(
            (root / "lighting/feature.py").read_text(encoding="utf-8"),
            "lighting/feature.py",
            "exec",
        )
        manifest = json.loads((root / "features.json").read_text(encoding="utf-8"))
        assert manifest["features"] == [
            {
                "module": "lighting.feature",
                "order": 30,
                "affected_manufactured_part_paths": ["top_panel_01"],
            }
        ]
        assert Path("assemblies/tall_storage_01/features.json") in result.written_paths
