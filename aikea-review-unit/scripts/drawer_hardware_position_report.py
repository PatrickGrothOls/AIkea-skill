"""Scope: Serialize the checked positions and overlaps of one drawer hardware set."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class DrawerHardwarePositionReport:
    """Keep exact hardware evidence without treating preparation as failure."""

    frames: dict[str, Any]
    fixing_depths_from_drawer_front_mm: tuple[float, ...]
    cabinet_side_contacts: tuple[dict[str, Any], ...]
    locking_device_mounting_relations: tuple[dict[str, Any], ...]
    wood_overlaps: tuple[dict[str, Any], ...]
    manufacturer_engagement_overlaps: tuple[dict[str, Any], ...]
    checks: tuple[dict[str, Any], ...]

    @property
    def is_valid(self) -> bool:
        return all(check["passed"] for check in self.checks)

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": "valid" if self.is_valid else "invalid",
            "cabinet_coordinates": {
                "positive_x": "right",
                "positive_y": "back",
                "positive_z": "up",
            },
            "hardware_frames": self.frames,
            "runner_fixing_depths_from_drawer_front_mm": list(
                self.fixing_depths_from_drawer_front_mm
            ),
            "cabinet_side_contacts": list(self.cabinet_side_contacts),
            "locking_device_mounting_relations": list(
                self.locking_device_mounting_relations
            ),
            "wood_overlaps": list(self.wood_overlaps),
            "manufacturer_engagement_overlaps": list(
                self.manufacturer_engagement_overlaps
            ),
            "checks": list(self.checks),
        }

    def write(self, path: Path) -> None:
        path.write_text(json.dumps(self.as_dict(), indent=2) + "\n", encoding="utf-8")

    def failed_check_names(self) -> list[str]:
        return [check["name"] for check in self.checks if not check["passed"]]


__all__ = ["DrawerHardwarePositionReport"]
