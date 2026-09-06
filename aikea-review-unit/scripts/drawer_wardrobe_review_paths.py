"""Scope: Name every artifact path from one drawer-in-wardrobe review."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from drawer_review_state import DrawerReviewState


@dataclass(frozen=True, slots=True)
class DrawerWardrobeReviewPaths:
    """Keep review outputs together beneath their owning project and cabinet."""

    drawer_position_report: Path
    hardware_position_report: Path
    runner_movement_report: Path
    closeup_glb: Path
    full_wardrobe_filename: str

    @classmethod
    def build(
        cls,
        project_root: Path,
        assembly_id: str,
        drawer_state: DrawerReviewState,
    ) -> "DrawerWardrobeReviewPaths":
        assembly_root = project_root / "assemblies" / assembly_id
        state = drawer_state.value
        return cls(
            drawer_position_report=assembly_root / "drawer-position-check.json",
            hardware_position_report=(
                assembly_root / "drawer-hardware-position-check.json"
            ),
            runner_movement_report=(
                assembly_root / "drawer-runner-movement-check.json"
            ),
            closeup_glb=(
                assembly_root / f"{assembly_id}_drawer_{state}_review.glb"
            ),
            full_wardrobe_filename=(
                f"full_wardrobe_{assembly_id}_drawer_{state}_review.glb"
            ),
        )


__all__ = ["DrawerWardrobeReviewPaths"]
