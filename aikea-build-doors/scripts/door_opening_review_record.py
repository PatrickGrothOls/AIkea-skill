"""Scope: Persist one client-facing proposal for door-opening approval."""

from __future__ import annotations

import json
from pathlib import Path

from door_opening_side_resolver import DoorOpeningSidePlan


class DoorOpeningReviewRecord:
    """Keep proposed and approved door hands in one project-owned record."""

    _MESSAGE = "All single doors hinge on the left unless marked otherwise."

    def write_proposal(
        self,
        path: Path,
        plans: tuple[DoorOpeningSidePlan, ...],
    ) -> None:
        if not plans:
            raise ValueError("every door needs a clear opening side before review")
        proposal = {
            "review_type": "door_openings",
            "status": "proposed",
            "message": self._MESSAGE,
            "doors": [
                {
                    "assembly_id": plan.assembly_id,
                    "label": f"Cabinet {index}",
                    "hinge_side": plan.proposed_side.value,
                    "exception": plan.changes_default,
                    "note": self._note(plan),
                    "reason": plan.reason,
                }
                for index, plan in enumerate(plans, start=1)
            ],
        }
        existing = self._read(path)
        if existing.get("status") == "approved" and existing.get("doors") == proposal["doors"]:
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(proposal, indent=2) + "\n", encoding="utf-8")

    def _note(self, plan: DoorOpeningSidePlan) -> str | None:
        if not plan.changes_default:
            return None
        return "your requested opening"

    def _read(self, path: Path) -> dict:
        if not path.is_file():
            return {}
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}


__all__ = ["DoorOpeningReviewRecord"]
