"""Scope: Serialize evidence for one review-only drawer-runner movement."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class RunnerMovementPreviewReport:
    """Record what moves together without granting manufacturing authority."""

    drawer_travel_mm: tuple[float, float, float]
    hand_relationships: tuple[dict[str, Any], ...]
    checks: tuple[dict[str, Any], ...]

    @property
    def is_valid(self) -> bool:
        return all(check["passed"] for check in self.checks)

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": "valid" if self.is_valid else "invalid",
            "representation": "review_only_runner_movement",
            "manufacturing_authority": False,
            "closed_hardware_authority": "verified_source_cad",
            "drawer_travel_mm": list(self.drawer_travel_mm),
            "hand_relationships": list(self.hand_relationships),
            "checks": list(self.checks),
        }

    def write(self, path: Path) -> None:
        path.write_text(json.dumps(self.as_dict(), indent=2) + "\n", encoding="utf-8")

    def failed_check_names(self) -> list[str]:
        return [check["name"] for check in self.checks if not check["passed"]]


__all__ = ["RunnerMovementPreviewReport"]
