"""Scope: Verify feature evidence is bound to its exact manufactured parts."""

from hashlib import sha256

from fabrication_readiness_gate import FabricationReadinessGate
from fabrication_readiness_test_project import FabricationReadinessTestProject


class TestFabricationFeatureEvidence:
    """Reject evidence for any part outside the registered feature scope."""

    def test_accepts_exact_feature_owned_part_evidence(self, tmp_path) -> None:
        project = FabricationReadinessTestProject()
        self._write_feature(project, tmp_path, "left_side")

        check = self._feature_check(project, tmp_path)

        assert check.passed

    def test_rejects_feature_evidence_for_an_unrelated_part(self, tmp_path) -> None:
        project = FabricationReadinessTestProject()
        self._write_feature(project, tmp_path, "door_panel")

        check = self._feature_check(project, tmp_path)

        assert not check.passed

    def _write_feature(self, project, root, affected_part: str) -> None:
        project.write_complete_pack(root)
        feature_root = root / "assemblies/cabinet_01"
        feature_root.mkdir()
        (feature_root / "spec.py").write_text("SPEC = None\n", encoding="utf-8")
        project.write_json(
            feature_root / "features.json",
            {
                "schema_version": 1,
                "features": [
                    {
                        "module": "door_hinges.feature",
                        "order": 20,
                        "affected_manufactured_part_paths": [affected_part],
                    }
                ],
            },
        )
        step = root / "manufacturing/parts" / (
            project.PART_PATH.replace("/", "__") + ".step"
        )
        project.write_json(
            feature_root / "fabrication-evidence/door_hinges-feature.json",
            {
                "schema_version": 1,
                "feature": "door_hinges.feature",
                "status": "valid",
                "manufacturing_authority": True,
                "checks": [{"name": "hinge machining", "passed": True}],
                "part_artifacts": [
                    {
                        "path": project.PART_PATH,
                        "step_sha256": sha256(step.read_bytes()).hexdigest(),
                    }
                ],
            },
        )

    def _feature_check(self, project, root):
        report = FabricationReadinessGate().evaluate(root, project.visits())
        return next(
            item
            for item in report.checks
            if item.code == "pack.feature_manufacturing_evidence"
        )


__all__ = ["TestFabricationFeatureEvidence"]
