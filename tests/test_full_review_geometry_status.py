"""Scope: Propagate shared geometry eligibility through the real standard review and CLI."""
import json
from pathlib import Path

import pytest
import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from configured_construction_evidence import ConfiguredConstructionEvidence
from generate_full_wardrobe_review import GenerateFullWardrobeReviewCommand


class TestFullReviewGeometryStatus:
    def project(self, root):
        fixture = Path(__file__).parent / "fixtures/review-unit-aikea.yaml"
        project = yaml.safe_load(fixture.read_text())
        project["measured_space"]["width_measurements"] = dict(bottom=60, middle=60, top=60)
        project["measured_space"]["height_measurements"] = [
            {"distance_from_left": distance, "height_from_floor": 100} for distance in (0, 30, 60)]
        project["design_settings"]["assembly_run"]["assemblies"] = [{"id": "tall_storage_01", "purpose": "tall_storage", "width_share": 1}]
        source = root / "aikea.yaml"
        source.write_text(yaml.safe_dump(project))
        AssemblyTaxonomyGenerator().generate(project, root)
        return source

    def test_shared_invalid_geometry_retains_inspection_but_cli_refuses_proposal(self, tmp_path, monkeypatch, capsys):
        source = self.project(tmp_path)
        original = ConfiguredConstructionEvidence.write
        monkeypatch.setattr(ConfiguredConstructionEvidence, "write", self.invalid_writer(original))
        assert GenerateFullWardrobeReviewCommand().run(source, "closed") == 2
        response = json.loads(capsys.readouterr().out)
        assert response["status"] == response["construction_position_status"] == "invalid"
        assert Path(response["full_wardrobe_glb"]).is_file()
        assert json.loads(Path(response["assembly_position_check"]).read_text())["status"] == "valid"
        assert json.loads(Path(response["construction_position_check"]).read_text())["status"] == "invalid"
        assert response["fabrication_review"] is None
        assert not (tmp_path / "reviews/fabrication-assembly.json").exists()

    def invalid_writer(self, original):
        # A narrow test adapter injects the observed shared-check failure after the real geometry build.
        def write(checker, root, *args):
            result = original(checker, root, *args)
            result["status"] = "invalid"
            (root / "assemblies/construction-position-check.json").write_text(json.dumps(result))
            return result
        return write

    @pytest.mark.parametrize("doors", ("closed", "open"))
    def test_ordinary_and_open_cli_expose_current_status_without_stale_evidence(self, tmp_path, doors, capsys):
        source = self.project(tmp_path)
        assert GenerateFullWardrobeReviewCommand().run(source, doors) == 0
        response = json.loads(capsys.readouterr().out)
        assert response["construction_position_status"] == ("valid" if doors == "closed" else None)
        assert bool(response["fabrication_review"]) == (doors == "closed")
