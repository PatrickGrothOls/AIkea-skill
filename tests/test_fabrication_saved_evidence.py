"""Scope: Verify saved position and feature evidence proves real scoped checks."""

from fabrication_readiness_gate import FabricationReadinessGate
from fabrication_readiness_test_project import FabricationReadinessTestProject


class TestFabricationSavedEvidence:
    """Reject bare status claims and discover feature evidence at any depth."""

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

    def test_finds_nested_feature_evidence_requirements(self, tmp_path) -> None:
        project = FabricationReadinessTestProject()
        project.write_complete_pack(tmp_path)
        project.write_json(
            tmp_path / "assemblies/cabinet_01/children/drawer_01/features.json",
            {
                "schema_version": 1,
                "features": [{"module": "drawer.feature", "order": 10}],
            },
        )

        report = FabricationReadinessGate().evaluate(tmp_path, project.visits())

        check = next(
            item
            for item in report.checks
            if item.code == "pack.feature_manufacturing_evidence"
        )
        assert not check.passed
        assert "drawer-feature.json" in check.problems[0]


__all__ = ["TestFabricationSavedEvidence"]
