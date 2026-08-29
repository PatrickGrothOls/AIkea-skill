"""Scope: Describe one complete wardrobe review with repeated drawer children."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class DrawerCollectionWardrobeReviewResult:
    """Report the exported wardrobe and every local/global position record."""

    glb_path: Path
    cabinet_report_paths: tuple[Path, ...]
    full_position_report_path: Path


__all__ = ["DrawerCollectionWardrobeReviewResult"]
