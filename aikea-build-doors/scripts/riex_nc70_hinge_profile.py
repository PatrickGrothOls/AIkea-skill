"""Scope: Hold the verified construction facts for one Riex NC70 hinge set."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RiexNc70HingeProfile:
    """Describe F000001 with the grid-mounted F000049 H0 plate."""

    profile_id: str = "riex-nc70-f000001-f000049"
    relationship: str = "full_overlay"
    cup_diameter_mm: float = 35.0
    cup_depth_mm: float = 12.0
    cup_edge_distance_mm: float = 6.0
    cup_center_from_edge_mm: float = 23.5
    cup_fixing_spacing_mm: float = 45.0
    plate_mounting_interface: str = "system_32_euroscrew_pair"
    plate_line_from_front_mm: float = 37.0
    plate_fixing_spacing_mm: float = 32.0
    plate_required_hole_diameter_mm: float = 5.0
    plate_required_hole_depth_mm: float = 12.0
    plate_height_mm: float = 52.0
    plate_height_interval_from_center_mm: tuple[float, float] = (-26.0, 26.0)
    plate_depth_interval_from_front_mm: tuple[float, float] = (
        19.576999,
        63.576999,
    )
    supported_overlay_mm: float = 17.0
    minimum_door_thickness_mm: float = 15.0
    maximum_door_thickness_mm: float = 24.0
    maximum_door_width_mm: float = 600.0
    maximum_door_height_mm: float = 2500.0
    native_door_surface_x_mm: float = -68.6
    native_cup_center_y_mm: float = 13.82363363031955
    native_fixing_center_y_mm: float = 4.32363363031955
    plate_native_vertical_center_x_mm: float = 24.693877
    plate_native_panel_face_y_mm: float = 32.688391
    plate_native_fixing_axis_z_mm: float = 6.103110
    native_pivot_x_mm: float = -78.957778
    native_pivot_y_mm: float = 25.138277
    open_angle_degrees: float = -112.601389

    @property
    def cup_fixing_line_from_edge_mm(self) -> float:
        """Derive the screw line from the exact source-CAD cup relationship."""
        return self.cup_center_from_edge_mm + (
            self.native_cup_center_y_mm - self.native_fixing_center_y_mm
        )

    @property
    def source_origin_from_door_edge_mm(self) -> float:
        """Locate the source origin from the resolved door edge."""
        return self.cup_center_from_edge_mm + self.native_cup_center_y_mm

    def hinge_count(self, door_height_mm: float) -> int:
        """Return the published height-band quantity for this first proof."""
        for maximum_height_mm, count in (
            (750.0, 2),
            (1500.0, 3),
            (2000.0, 4),
            (2500.0, 5),
        ):
            if door_height_mm <= maximum_height_mm:
                return count
        return 5


RIEX_NC70_FULL_OVERLAY = RiexNc70HingeProfile()


__all__ = ["RIEX_NC70_FULL_OVERLAY", "RiexNc70HingeProfile"]
