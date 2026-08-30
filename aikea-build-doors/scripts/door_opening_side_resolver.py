"""Scope: Choose a single door's hinge side from proven 90-degree clearance."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any

from door_hinge_side import DoorHingeSide
from door_opening_clearance import (
    DoorOpeningClearanceChecker,
    DoorOpeningClearanceResult,
)
from riex_nc70_hinge_profile import RiexNc70HingeProfile


@dataclass(frozen=True, slots=True)
class DoorOpeningSidePlan:
    """Carry the default, proposed side, and every clearance result used."""

    assembly_id: str
    default_side: DoorHingeSide
    proposed_side: DoorHingeSide | None
    reason: str
    checks: tuple[DoorOpeningClearanceResult, ...]
    selection_source: str = "automatic"

    @property
    def passes(self) -> bool:
        return self.proposed_side is not None

    @property
    def changes_default(self) -> bool:
        return self.proposed_side not in (None, self.default_side)

    def write(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        values = asdict(self)
        values["passes"] = self.passes
        values["changes_default"] = self.changes_default
        path.write_text(json.dumps(values, indent=2) + "\n", encoding="utf-8")


class DoorOpeningSideResolver:
    """Keep the ordinary left hinge unless measured geometry disproves it."""

    def __init__(self) -> None:
        self.clearance = DoorOpeningClearanceChecker()

    def resolve(
        self,
        inputs: Any,
        assembly: Any,
        profile: RiexNc70HingeProfile,
        preferred_side: DoorHingeSide | None = None,
    ) -> DoorOpeningSidePlan:
        default = DoorHingeSide.LEFT
        if preferred_side is not None:
            requested = self.clearance.check(inputs, assembly, preferred_side, profile)
            return DoorOpeningSidePlan(
                assembly.assembly_id,
                default,
                preferred_side if requested.passes else None,
                (
                    "the requested opening clears every measured boundary"
                    if requested.passes
                    else "the requested opening cannot reach 90 degrees in the measured space"
                ),
                (requested,),
                "client_choice",
            )
        left = self.clearance.check(inputs, assembly, default, profile)
        if left.passes:
            return DoorOpeningSidePlan(
                assembly.assembly_id,
                default,
                default,
                "the ordinary left-hinged opening clears every measured boundary",
                (left,),
            )
        right = self.clearance.check(inputs, assembly, DoorHingeSide.RIGHT, profile)
        if right.passes:
            return DoorOpeningSidePlan(
                assembly.assembly_id,
                default,
                DoorHingeSide.RIGHT,
                "the measured space prevents the ordinary opening but clears a right-hinged door",
                (left, right),
                "room_clearance",
            )
        return DoorOpeningSidePlan(
            assembly.assembly_id,
            default,
            None,
            "neither hinge side can open 90 degrees inside the measured space",
            (left, right),
        )


__all__ = ["DoorOpeningSidePlan", "DoorOpeningSideResolver"]
