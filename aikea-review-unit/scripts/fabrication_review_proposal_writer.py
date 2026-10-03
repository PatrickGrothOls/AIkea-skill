"""Scope: Issue visual proposals for canonical closed full-wardrobe results."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from fabrication_assembly_review_record import FabricationAssemblyReviewRecord
from construction_review_eligibility import ConstructionReviewEligibility


class FabricationReviewProposalWriter:
    """Keep fabrication approval policy outside the generic wardrobe renderer."""

    _CANONICAL_FILENAME = "full_wardrobe_review.glb"

    def __init__(self, records: Any | None = None) -> None:
        self.records = records or FabricationAssemblyReviewRecord()

    def write_for_result(self, project_root: Path, result: Any) -> Path | None:
        canonical_path = project_root / "assemblies" / self._CANONICAL_FILENAME
        is_closed = bool(result.door_states) and set(result.door_states.values()) == {
            "closed"
        }
        if (result.glb_path.resolve() != canonical_path.resolve() or not is_closed
                or result.construction_position_status != "valid"
                or not ConstructionReviewEligibility().allows(project_root, result.construction_sha256)):
            return None
        return self.records.write_proposal(project_root, result.glb_path, result.construction_sha256)


__all__ = ["FabricationReviewProposalWriter"]
