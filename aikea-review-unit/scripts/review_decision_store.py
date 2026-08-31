"""Scope: Read and persist one bounded client decision from the local viewer."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path


class ReviewDecisionStore:
    """Own the project-local review record exposed by one loopback server."""

    _DECISIONS = {
        "approved": "approved",
        "change_requested": "change_requested",
    }
    _REVIEW_TYPES = {"door_openings", "fabrication_assembly"}

    def __init__(self, path: Path) -> None:
        self.path = path.resolve()

    def decide(self, decision: str) -> dict:
        status = self._DECISIONS.get(decision)
        if status is None:
            raise ValueError("unsupported review decision")
        record = json.loads(self.path.read_text(encoding="utf-8"))
        if (
            not isinstance(record, dict)
            or record.get("review_type") not in self._REVIEW_TYPES
        ):
            raise ValueError("review record type is unsupported")
        record["status"] = status
        record["decided_at"] = datetime.now(timezone.utc).isoformat()
        self.path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        return record


__all__ = ["ReviewDecisionStore"]
