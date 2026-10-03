"""Scope: Coordinate physical files and saved fabrication evidence."""

from __future__ import annotations

from pathlib import Path

from fabrication_closed_assembly_approval_checker import (
    FabricationClosedAssemblyApprovalChecker,
)
from fabrication_feature_evidence_checker import FabricationFeatureEvidenceChecker
from fabrication_pack_record_checker import FabricationPackRecordChecker
from fabrication_part_artifact_checker import FabricationPartArtifactChecker
from fabrication_readiness_report import FabricationReadinessCheck
from fabrication_position_evidence_checker import FabricationPositionEvidenceChecker
from fabrication_tree_evidence import FabricationTreeEvidence
from construction_position_evidence import ConstructionPositionEvidence


class FabricationArtifactChecker:
    """Require every exported, recorded, validated, and approved artifact."""

    def __init__(self) -> None:
        self.part_artifacts = FabricationPartArtifactChecker()
        self.pack_records = FabricationPackRecordChecker()
        self.feature_evidence = FabricationFeatureEvidenceChecker()
        self.position_evidence = FabricationPositionEvidenceChecker()
        self.approval = FabricationClosedAssemblyApprovalChecker()
        self.construction_position = ConstructionPositionEvidence()

    def check(
        self,
        project_root: Path,
        evidence: FabricationTreeEvidence,
        visits,
    ) -> tuple[FabricationReadinessCheck, ...]:
        # Keep the old wardrobe-specific relationship record as a migration adapter.
        legacy = (self.position_evidence.check(project_root, evidence, visits),) if visits[0].path == ("wardrobe_01",) else ()
        return (
            self.part_artifacts.check(project_root, evidence.parts),
            *self.pack_records.check(project_root, evidence),
            self.feature_evidence.check(project_root, evidence, visits),
            self.construction_position.check(project_root, evidence, visits),
            *legacy,
            self.approval.check(project_root, visits),
        )


__all__ = ["FabricationArtifactChecker"]
