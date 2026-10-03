"""Scope: Define the written result of one lit-cabinet visual review."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class CabinetLightingReviewResult:
    """Expose the GLB and deterministic position evidence together."""

    assembly_id: str
    glb_path: Path
    fit_report_path: Path


__all__ = ["CabinetLightingReviewResult"]
