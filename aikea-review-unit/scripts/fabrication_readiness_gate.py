"""Scope: Combine recursive physical checks with the required fabrication pack."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from assembly_fabrication_checker import AssemblyFabricationChecker
from fabrication_artifact_checker import FabricationArtifactChecker
from fabrication_readiness_report import FabricationReadinessReport


class FabricationReadinessGate:
    """Produce one authoritative readiness result without feature-specific branches."""

    def __init__(self) -> None:
        self.assembly = AssemblyFabricationChecker()
        self.artifacts = FabricationArtifactChecker()

    def evaluate(
        self,
        project_root: Path,
        visits: tuple[Any, ...],
    ) -> FabricationReadinessReport:
        checks = self.assembly.check(visits) + self.artifacts.check(
            project_root,
            self.assembly.part_paths(visits),
            self.assembly.hardware_paths(visits),
        )
        return FabricationReadinessReport(checks)


__all__ = ["FabricationReadinessGate"]
