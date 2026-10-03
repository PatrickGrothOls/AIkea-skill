"""Scope: Verify saved position and approval evidence is current and complete."""

import json

from fabrication_readiness_gate import FabricationReadinessGate
from fabrication_readiness_test_project import FabricationReadinessTestProject


class TestFabricationSavedEvidence:
    """Reject placeholder, stale, or incomplete saved review evidence."""

    def test_rejects_a_bare_valid_position_claim(self, tmp_path) -> None:
        project = FabricationReadinessTestProject()
        project.write_complete_pack(tmp_path)
        project.write_json(
            tmp_path / "assemblies/full-wardrobe-position-check.json",
            {"schema_version": 1, "status": "valid"},
        )

        report = FabricationReadinessGate().evaluate(tmp_path, project.visits())

        failed = {check.code for check in report.checks if not check.passed}
        assert "validation.full_wardrobe_position" in failed

    def test_rejects_position_evidence_for_a_stale_tree_frame(self, tmp_path) -> None:
        project = FabricationReadinessTestProject()
        project.write_complete_pack(tmp_path)
        visits = project.visits()
        visits[-1].local_to_root.origin_in_parent.x_mm = 10.0

        report = FabricationReadinessGate().evaluate(tmp_path, visits)

        failed = {check.code for check in report.checks if not check.passed}
        assert "validation.full_wardrobe_position" in failed

    def test_rejects_arbitrary_position_relationship_claims(self, tmp_path) -> None:
        project = FabricationReadinessTestProject()
        project.write_complete_pack(tmp_path)
        path = tmp_path / "assemblies/full-wardrobe-position-check.json"
        record = json.loads(path.read_text(encoding="utf-8"))
        record["relationships"] = {"cabinet_count": 1}
        project.write_json(path, record)

        report = FabricationReadinessGate().evaluate(tmp_path, project.visits())

        failed = {check.code for check in report.checks if not check.passed}
        assert "validation.full_wardrobe_position" in failed

    def test_rejects_approval_without_the_decided_artifact_hash(self, tmp_path) -> None:
        project = FabricationReadinessTestProject()
        project.write_complete_pack(tmp_path)
        record_path = tmp_path / "reviews/fabrication-assembly.json"
        record = json.loads(record_path.read_text(encoding="utf-8"))
        del record["decision_artifact_sha256"]
        project.write_json(record_path, record)

        report = FabricationReadinessGate().evaluate(tmp_path, project.visits())

        failed = {check.code for check in report.checks if not check.passed}
        assert "approval.current_closed_assembly" in failed


__all__ = ["TestFabricationSavedEvidence"]
