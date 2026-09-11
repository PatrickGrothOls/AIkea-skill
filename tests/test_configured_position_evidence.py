"""Scope: Check configured site measurements and custom position proof through the same geometry engine."""

import json
from pathlib import Path

import pytest
import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from configured_review_envelope import ConfiguredReviewEnvelope
from construction_position_evidence import ConstructionPositionEvidence
from fabrication_tree_evidence import FabricationTreeEvidenceBuilder
from full_wardrobe_review_generator import FullWardrobeReviewGenerator


class TestConfiguredPositionEvidence:
    def test_site_envelope_uses_the_existing_root_datum(self):
        fixture = Path(__file__).parent / "fixtures/review-unit-aikea.yaml"
        envelope = ConfiguredReviewEnvelope().build(yaml.safe_load(fixture.read_text()))
        box = envelope.val().BoundingBox()
        assert (box.xmin, box.ymin, box.zmin) == pytest.approx((-10, -18, 0))
        assert (box.xmax, box.ymax, box.zmax) == pytest.approx((2988, 582, 2396))

    def test_sloped_configurator_produces_reproducible_shared_position_evidence(self, tmp_path):
        fixture = Path(__file__).parent / "fixtures/four-unit-review-aikea.yaml"
        project = yaml.safe_load(fixture.read_text())
        (tmp_path / "aikea.yaml").write_text(fixture.read_text())
        AssemblyTaxonomyGenerator().generate(project, tmp_path)
        generator = FullWardrobeReviewGenerator()
        generator.generate(tmp_path, project)
        data = json.loads((tmp_path / ConstructionPositionEvidence.REPORT).read_text())
        assert data["status"] == "valid", data["geometry"]
        assert data["envelope_source"] == "configured_measurements"
        built = generator.loader.load_assembly(tmp_path, "wardrobe_01")
        visits = generator.loader.walk(tmp_path, built)
        tree = FabricationTreeEvidenceBuilder().build(visits)
        check = ConstructionPositionEvidence().check(tmp_path, tree, visits)
        assert check.passed, check.problems
