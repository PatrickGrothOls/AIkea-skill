"""Scope: Check base height and derive conservative Korrekt stations without load qualification."""
from dataclasses import dataclass
from math import ceil
from korrekt_mounting_profile import KorrektMountingProfile
from part_construction_error import PartConstructionError


@dataclass(frozen=True)
class KorrektBaseLayout:
    height_mm: float
    deck_thickness_mm: float
    minimum_plate_edge_margin_mm: float = 15.0
    maximum_station_spacing_mm: float = 600.0
    # Official article 70151, accessed 2026-09-15; physical adjustment range, not CAD articulation.
    adjustment_range_mm: tuple[float, float] = (74.0, 110.0)
    source_foot_floor_z_mm: float = -53.5

    @property
    def support_height_mm(self):
        return self.height_mm - self.deck_thickness_mm

    def check_adjustment_range(self):
        low, high = self.adjustment_range_mm
        if self.deck_thickness_mm <= 0 or not low <= self.support_height_mm <= high:
            raise PartConstructionError(
                f"Korrekt 70151 requires {low:g}–{high:g} mm below the deck; "
                f"{self.height_mm:g} mm base minus {self.deck_thickness_mm:g} mm deck "
                f"leaves {self.support_height_mm:g} mm. Resolve this conflict; no brace-base fallback.")

    def station_axes(self, start_x_mm, end_x_mm, depth_mm, kickboard_rear_mm):
        """Keep the whole plate and foot behind the kickboard and within deck edges."""
        p = KorrektMountingProfile()
        left, right, front, rear = p.plate_bounds_xy_mm
        sx, sy = p.socket_axis_xy_mm
        margin = self.minimum_plate_edge_margin_mm
        first = start_x_mm + max(sx-left+margin, 40.15)
        last = end_x_mm - max(right-sx+margin, 40.15)
        front_axis = max(sy-front+margin, kickboard_rear_mm+40.15+2)
        rear_axis = depth_mm-max(rear-sy+margin,40.15)
        if last <= first or rear_axis <= front_axis:
            raise PartConstructionError("Korrekt plates/feet do not fit this deck and kickboard footprint")
        intervals = max(1, ceil((last-first)/self.maximum_station_spacing_mm))
        return tuple((first+(last-first)*i/intervals, y)
                     for i in range(intervals+1) for y in (front_axis,rear_axis))
