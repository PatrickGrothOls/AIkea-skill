"""Scope: Record the deterministic fit evidence for one door-and-hinge proof."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path

from door_hinge_plan import DoorHingePlan
from door_opening_side_resolver import DoorOpeningSidePlan
from riex_nc70_hinge_profile import RiexNc70HingeProfile


@dataclass(frozen=True, slots=True)
class DoorHingeReviewReport:
    """Expose fit checks separately from visual presentation."""

    assembly_id: str
    profile_id: str
    hinge_side: str
    hinge_count: int
    cup_center_from_edge_mm: float
    plate_mounting_interface: str
    plate_line_from_front_mm: float
    plate_fixing_rows_mm: tuple[tuple[float, float], ...]
    overlay_mm: float
    plate_mount_face_mm: float
    open_angle_degrees: float
    opening_side_changed_from_default: bool
    opening_selection_source: str
    shared_placement_drives_both_panels: bool
    mounting_uses_cabinet_grid: bool
    exact_closed_and_open_source_cad: bool
    fabrication_ready: bool
    compatibility_issues: tuple[str, ...]

    @classmethod
    def from_plan(
        cls,
        plan: DoorHingePlan,
        opening_plan: DoorOpeningSidePlan,
        side_thickness_mm: float,
        profile: RiexNc70HingeProfile,
    ) -> "DoorHingeReviewReport":
        return cls(
            assembly_id=plan.assembly_id,
            profile_id=plan.profile_id,
            hinge_side=plan.hinge_side.value,
            hinge_count=len(plan.placements),
            cup_center_from_edge_mm=profile.cup_center_from_edge_mm,
            plate_mounting_interface=profile.plate_mounting_interface,
            plate_line_from_front_mm=profile.plate_line_from_front_mm,
            plate_fixing_rows_mm=tuple(
                placement.cabinet_fixing_rows_mm
                for placement in plan.placements
            ),
            overlay_mm=plan.overlay_mm,
            plate_mount_face_mm=side_thickness_mm,
            open_angle_degrees=abs(profile.open_angle_degrees),
            opening_side_changed_from_default=opening_plan.changes_default,
            opening_selection_source=opening_plan.selection_source,
            shared_placement_drives_both_panels=True,
            mounting_uses_cabinet_grid=True,
            exact_closed_and_open_source_cad=True,
            fabrication_ready=plan.fabrication_ready,
            compatibility_issues=plan.compatibility_issues,
        )

    def write(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(asdict(self), indent=2) + "\n", encoding="utf-8")


__all__ = ["DoorHingeReviewReport"]
