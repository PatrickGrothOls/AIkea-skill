"""Scope: Verify approval belongs to the exact current closed wardrobe GLB."""

from __future__ import annotations

from pathlib import Path

from fabrication_closed_assembly_model import FabricationClosedAssemblyModel
from fabrication_readiness_report import FabricationReadinessCheck
from fabrication_record_validator import FabricationRecordValidator
from glb_artifact_snapshot import GlbArtifactSnapshot
from unit_mockup import UnitMockupInputError


class FabricationClosedAssemblyApprovalChecker:
    """Reject corrupt, stale, differently pathed, or unapproved visual artifacts."""

    def __init__(self) -> None:
        self.records = FabricationRecordValidator()
        self.closed_model = FabricationClosedAssemblyModel()

    def check(self, root, visits) -> FabricationReadinessCheck:
        model_path = root / "assemblies/full_wardrobe_review.glb"
        record_path = root / "reviews/fabrication-assembly.json"
        data = self.records.read_json(record_path)
        try:
            model = GlbArtifactSnapshot.load(model_path)
            expected_sha256 = self.closed_model.expected_sha256(visits)
        except UnitMockupInputError:
            model = None
            expected_sha256 = None
        artifact = data.get("artifact") if data else None
        approved = bool(
            model
            and model.sha256 == expected_sha256
            and isinstance(artifact, str)
            and not Path(artifact).is_absolute()
            and (root / artifact).resolve() == model.path
            and data.get("review_type") == "fabrication_assembly"
            and data.get("status") == "approved"
            and data.get("artifact_sha256") == model.sha256
            and data.get("decision_artifact_sha256") == model.sha256
        )
        problems = () if approved else (str(record_path.relative_to(root)),)
        return FabricationReadinessCheck(
            "approval.current_closed_assembly",
            not problems,
            problems,
        )


__all__ = ["FabricationClosedAssemblyApprovalChecker"]
