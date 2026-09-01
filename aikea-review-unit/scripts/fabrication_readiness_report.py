"""Scope: Serialize machine-verifiable fabrication readiness checks."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path


@dataclass(frozen=True, slots=True)
class FabricationReadinessCheck:
    """Record one independently actionable fabrication requirement."""

    code: str
    passed: bool
    problems: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, object]:
        return {
            "code": self.code,
            "passed": self.passed,
            "problems": list(self.problems),
        }


@dataclass(frozen=True, slots=True)
class FabricationReadinessReport:
    """Grant readiness only when every physical and documentary gate passes."""

    checks: tuple[FabricationReadinessCheck, ...]

    @property
    def is_ready(self) -> bool:
        return bool(self.checks) and all(check.passed for check in self.checks)

    def as_dict(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "status": "fabrication-ready" if self.is_ready else "blocked",
            "checks": [check.as_dict() for check in self.checks],
        }

    def write(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.as_dict(), indent=2) + "\n", encoding="utf-8")


__all__ = ["FabricationReadinessCheck", "FabricationReadinessReport"]
