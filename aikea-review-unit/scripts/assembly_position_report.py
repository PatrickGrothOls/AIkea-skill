"""Scope: Record the checked local and project positions of reviewed assemblies."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from placed_bounds import PlacedBounds


@dataclass(frozen=True)
class AssemblyPositionReport:
    """Keep one serializable result from the cabinet-to-base position check."""

    assemblies: dict[str, Any]
    relationships: dict[str, Any]
    checks: tuple[dict[str, Any], ...]

    @staticmethod
    def assembly_values(
        global_zero_mm: tuple[float, float, float],
        local_bounds: PlacedBounds,
        global_bounds: PlacedBounds,
        part_positions: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "local_zero_mm": [0.0, 0.0, 0.0],
            "global_zero_mm": list(global_zero_mm),
            "local_bounds": local_bounds.as_dict(),
            "global_bounds": global_bounds.as_dict(),
            "part_positions": part_positions,
        }

    @staticmethod
    def check(name: str, passed: bool) -> dict[str, Any]:
        return {"name": name, "passed": passed}

    @property
    def is_valid(self) -> bool:
        return all(check["passed"] for check in self.checks)

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "status": "valid" if self.is_valid else "invalid",
            "global_coordinates": {
                "zero": "front-left floor point of the measured space",
                "positive_x": "right",
                "positive_y": "back",
                "positive_z": "up",
            },
            "assemblies": self.assemblies,
            "relationships": self.relationships,
            "checks": list(self.checks),
        }

    def write(self, path: Path) -> None:
        path.write_text(json.dumps(self.as_dict(), indent=2) + "\n", encoding="utf-8")

    def failed_check_names(self) -> list[str]:
        return [check["name"] for check in self.checks if not check["passed"]]


__all__ = ["AssemblyPositionReport"]
