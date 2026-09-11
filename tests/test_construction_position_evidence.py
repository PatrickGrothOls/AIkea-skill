"""Scope: Recompute saved position proof against current solids and the declared boundary."""

from hashlib import sha256
import json

import cadquery as cq
import pytest

from construction_envelope_authority import ConstructionEnvelopeAuthority
from construction_position_evidence import ConstructionPositionEvidence
from fabrication_readiness_test_project import FabricationReadinessTestProject
from fabrication_tree_evidence import FabricationTreeEvidenceBuilder


class TestConstructionPositionEvidence:
    def test_valid_record_reproduces_current_closed_geometry(self, tmp_path):
        project = FabricationReadinessTestProject()
        project.write_complete_pack(tmp_path)
        assert self._check(tmp_path, project.visits()).passed

    def test_saved_success_does_not_hide_moved_material(self, tmp_path):
        project = FabricationReadinessTestProject()
        project.write_complete_pack(tmp_path)
        visits = project.visits()
        visits[-1].part.solid = visits[-1].part.solid.translate((1, 0, 0))
        assert not self._check(tmp_path, visits).passed

    def test_edited_bounds_or_missing_physical_item_are_not_accepted(self, tmp_path):
        project = FabricationReadinessTestProject()
        project.write_complete_pack(tmp_path)
        record = tmp_path / ConstructionPositionEvidence.REPORT
        data = json.loads(record.read_text())
        data["physical_items"] = []
        record.write_text(json.dumps(data))
        assert not self._check(tmp_path, project.visits()).passed

    def test_replaced_envelope_with_updated_checksum_cannot_enlarge_declared_space(self, tmp_path):
        project = FabricationReadinessTestProject()
        project.write_complete_pack(tmp_path)
        envelope = tmp_path / ConstructionPositionEvidence.ENVELOPE
        cq.exporters.export(cq.Workplane("XY").box(1000, 2000, 18, centered=False), str(envelope))
        record = tmp_path / ConstructionPositionEvidence.REPORT
        data = json.loads(record.read_text())
        data["envelope_sha256"] = sha256(envelope.read_bytes()).hexdigest()
        record.write_text(json.dumps(data))
        check = self._check(tmp_path, project.visits())
        assert not check.passed
        assert "current declared inputs" in check.problems[0]

    def test_unbound_contact_declaration_cannot_suppress_collisions(self, tmp_path):
        project = FabricationReadinessTestProject()
        project.write_complete_pack(tmp_path)
        record = tmp_path / ConstructionPositionEvidence.REPORT
        data = json.loads(record.read_text())
        data["contact_allowances"] = [{"allowance_id": "ignore_everything"}]
        record.write_text(json.dumps(data))
        assert not self._check(tmp_path, project.visits()).passed

    def test_record_cannot_choose_configured_measurements_over_authored_envelope(self, tmp_path):
        project = FabricationReadinessTestProject()
        project.write_complete_pack(tmp_path)
        builder = tmp_path / "assemblies/wardrobe_01/builder.py"
        builder.write_text(builder.read_text().replace("box(500,", "box(450,"))
        # The report is freshly bound to the same inputs but uses a larger boundary.
        ConstructionPositionEvidence().write(tmp_path, project.visits(),
            cq.Workplane("XY").box(500, 2000, 18, centered=False), envelope_source="configured_measurements")
        check = self._check(tmp_path, project.visits())
        assert not check.passed
        assert "current declared inputs" in check.problems[0]

    def test_missing_root_authority_cannot_fall_back_to_a_wardrobe_recipe(self, tmp_path):
        project = FabricationReadinessTestProject()
        project.write_complete_pack(tmp_path)
        (tmp_path / "assemblies/wardrobe_01/builder.py").write_text('"""No envelope declared."""\n')
        with pytest.raises(ValueError, match="unknown construction envelope authority"):
            ConstructionEnvelopeAuthority().read(tmp_path, "wardrobe_01")

    def _check(self, root, visits):
        tree = FabricationTreeEvidenceBuilder().build(visits)
        return ConstructionPositionEvidence().check(root, tree, visits)
