"""Scope: Build an actual generated wardrobe through the common configured envelope authority."""
import json
from pathlib import Path

import yaml

from panel_review_hydration_fixture import PanelReviewHydrationFixture
from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from build_furniture_design import FurnitureDesignBuild
from construction_position_evidence import ConstructionPositionEvidence
from fabrication_tree_evidence import FabricationTreeEvidenceBuilder


class TestCommonConfiguredBuild:
    def test_common_build_reproduces_current_configured_position_authority(self, tmp_path):
        source = Path(__file__).parent / "fixtures/four-unit-review-aikea.yaml"
        project = yaml.safe_load(source.read_text())
        project["measured_space"].update(
            top_boundary="flat", width_measurements={"bottom": 60, "middle": 60, "top": 60},
            height_measurements=[{"distance_from_left": x, "height_from_floor": 70} for x in (0, 30, 60)],
            depth_measurements={"single": 40})
        project["design_settings"]["assembly_run"]["assemblies"] = [
            {"id": "tall_storage_01", "purpose": "tall_storage", "width_share": 1}]
        (tmp_path / "aikea.yaml").write_text(yaml.safe_dump(project))
        AssemblyTaxonomyGenerator().generate(project, tmp_path)
        builder = FurnitureDesignBuild()
        builder._hydrate = PanelReviewHydrationFixture().hydrate
        result = builder.build(tmp_path, "wardrobe_01", tmp_path / "reviews/wardrobe.glb")
        assert result["status"] == "valid", result
        saved = json.loads((tmp_path / ConstructionPositionEvidence.REPORT).read_text())
        assert saved["envelope_source"] == "configured_measurements"
        built = builder.loader.load_assembly(tmp_path, "wardrobe_01")
        visits = builder.loader.walk(tmp_path, built)
        check = ConstructionPositionEvidence().check(
            tmp_path, FabricationTreeEvidenceBuilder().build(visits), visits)
        assert check.passed, check.problems
