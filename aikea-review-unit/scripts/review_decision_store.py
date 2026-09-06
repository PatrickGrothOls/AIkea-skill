"""Scope: Atomically persist one decision bound to one local review artifact."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from uuid import uuid4

from glb_artifact_snapshot import GlbArtifactSnapshot
from review_decision_file_lock import ReviewDecisionFileLock


class ReviewDecisionConflict(ValueError):
    """Report a stale artifact, stale proposal, or already completed decision."""


class ReviewDecisionStore:
    """Own one project review record and its single proposed-to-decided transition."""

    _DECISIONS = {"approved", "change_requested"}
    _REVIEW_TYPES = {"door_openings", "fabrication_assembly"}

    def __init__(self, path: Path) -> None:
        self.path = path.resolve()

    def read(self, artifact: GlbArtifactSnapshot | None = None) -> dict:
        record = self._read_record()
        self._validate_record(record, artifact)
        return record

    def decide(
        self,
        decision: str,
        artifact: GlbArtifactSnapshot | None = None,
    ) -> dict:
        if decision not in self._DECISIONS:
            raise ValueError("unsupported review decision")
        with ReviewDecisionFileLock(self.path):
            record = self.read(artifact)
            if record.get("status") != "proposed":
                raise ReviewDecisionConflict("the review proposal is no longer pending")
            record["status"] = decision
            record["decided_at"] = datetime.now(timezone.utc).isoformat()
            if record["review_type"] == "fabrication_assembly":
                record["decision_artifact_sha256"] = artifact.sha256
            self._write_atomically(record)
            return record

    def _read_record(self) -> dict:
        try:
            record = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise ValueError("review record cannot be read") from error
        if not isinstance(record, dict):
            raise ValueError("review record must contain an object")
        return record

    def _validate_record(
        self,
        record: dict,
        artifact: GlbArtifactSnapshot | None,
    ) -> None:
        review_type = record.get("review_type")
        if review_type not in self._REVIEW_TYPES:
            raise ValueError("review record type is unsupported")
        if review_type == "fabrication_assembly":
            self._validate_artifact(record, artifact)

    def _validate_artifact(
        self,
        record: dict,
        artifact: GlbArtifactSnapshot | None,
    ) -> None:
        relative_path = record.get("artifact")
        if artifact is None or not isinstance(relative_path, str):
            raise ReviewDecisionConflict("fabrication review has no served artifact")
        candidate = Path(relative_path)
        project_root = self.path.parent.parent
        if (
            candidate.is_absolute()
            or (project_root / candidate).resolve() != artifact.path
            or record.get("artifact_sha256") != artifact.sha256
        ):
            raise ReviewDecisionConflict(
                "fabrication review does not match the served GLB"
            )

    def _write_atomically(self, record: dict) -> None:
        temporary = self.path.with_name(f".{self.path.name}.{uuid4().hex}.tmp")
        try:
            temporary.write_text(
                json.dumps(record, indent=2) + "\n",
                encoding="utf-8",
            )
            temporary.replace(self.path)
        except OSError:
            temporary.unlink(missing_ok=True)
            raise


__all__ = ["ReviewDecisionConflict", "ReviewDecisionStore"]
