"""Scope: Define the generated files from one drawer-in-wardrobe review."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class DrawerWardrobeReviewResult:
    """Report both views and their physical position evidence."""

    assembly_id: str
    drawer_id: str
    drawer_state: str
    runner_product_code: str
    runner_review_representation: str
    closeup_glb_path: Path
    full_wardrobe_glb_path: Path
    drawer_position_report_path: Path
    hardware_position_report_path: Path
    runner_movement_report_path: Path
    full_position_report_path: Path


__all__ = ["DrawerWardrobeReviewResult"]
