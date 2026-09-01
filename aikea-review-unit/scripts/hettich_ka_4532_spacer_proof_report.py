"""Scope: Serialize one exact KA 4532 spacer movement and collision proof."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class HettichKa4532SpacerProofReport:
    """Keep review evidence explicit without granting fabrication authority."""

    assembly_id: str
    drawer_id: str
    source_cad: dict[str, Any]
    artifacts: dict[str, Any]
    machining_blocker: dict[str, Any]
    hardware_reservations: tuple[dict[str, Any], ...]
    movement: dict[str, Any]
    collisions: dict[str, Any]
    checks: tuple[dict[str, Any], ...]

    @property
    def is_valid(self) -> bool:
        return all(check["passed"] for check in self.checks)

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "status": (
                "movement-and-collision-valid-machining-blocked"
                if self.is_valid
                else "invalid"
            ),
            "review_type": "hettich_ka_4532_spacer_movement_collision_proof",
            "manufacturing_authority": False,
            "assembly_id": self.assembly_id,
            "drawer_id": self.drawer_id,
            "source_cad": self.source_cad,
            "artifacts": self.artifacts,
            "machining_blocker": self.machining_blocker,
            "hardware_reservations": list(self.hardware_reservations),
            "movement": self.movement,
            "collisions": self.collisions,
            "checks": list(self.checks),
        }

    def write(self, path: Path) -> None:
        self._replace(path, self.as_dict())

    @classmethod
    def invalidate(cls, path: Path, problem: str | None = None) -> None:
        payload = {
            "schema_version": 1,
            "status": "invalidated-before-run",
            "manufacturing_authority": False,
            "problems": [problem] if problem else [],
        }
        cls._replace(path, payload)

    def failed_check_names(self) -> tuple[str, ...]:
        return tuple(check["name"] for check in self.checks if not check["passed"])

    @staticmethod
    def _replace(path: Path, payload: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(f"{path.name}.tmp")
        temporary.write_text(
            json.dumps(payload, indent=2) + "\n",
            encoding="utf-8",
        )
        temporary.replace(path)


__all__ = ["HettichKa4532SpacerProofReport"]
