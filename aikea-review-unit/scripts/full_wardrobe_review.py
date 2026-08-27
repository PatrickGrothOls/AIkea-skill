"""Scope: Define the generated files from one full-wardrobe visual review."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FullWardrobeReviewResult:
    assembly_ids: tuple[str, ...]
    glb_path: Path
    position_report_path: Path


__all__ = ["FullWardrobeReviewResult"]
