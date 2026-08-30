"""Scope: Choose a single door's hinge side from the standard or client choice."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any

from door_hinge_side import DoorHingeSide


@dataclass(frozen=True, slots=True)
class DoorOpeningSidePlan:
    """Carry the standard hand and the resolved client-visible proposal."""

    assembly_id: str
    default_side: DoorHingeSide
    proposed_side: DoorHingeSide
    reason: str
    selection_source: str = "standard"

    @property
    def changes_default(self) -> bool:
        return self.proposed_side is not self.default_side

    def write(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        values = asdict(self)
        values["changes_default"] = self.changes_default
        path.write_text(json.dumps(values, indent=2) + "\n", encoding="utf-8")


class DoorOpeningSideResolver:
    """Keep the ordinary left hinge unless the client chooses otherwise."""

    def resolve(
        self,
        assembly: Any,
        preferred_side: DoorHingeSide | None = None,
    ) -> DoorOpeningSidePlan:
        default = DoorHingeSide.LEFT
        if preferred_side is not None:
            return DoorOpeningSidePlan(
                assembly.assembly_id,
                default,
                preferred_side,
                "the client selected this opening hand",
                "client_choice",
            )
        return DoorOpeningSidePlan(
            assembly.assembly_id,
            default,
            default,
            "the ordinary single-door arrangement hinges on the left",
        )


__all__ = ["DoorOpeningSidePlan", "DoorOpeningSideResolver"]
