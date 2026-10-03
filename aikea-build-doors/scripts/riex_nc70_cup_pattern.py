"""Scope: Express the NC70 cup and chosen fixing pilots relative to the cup centre."""

from riex_nc70_hinge_profile import RiexNc70HingeProfile
from surface_hole_pattern import SurfaceHole, SurfaceHolePattern


class RiexNc70CupPattern:
    def __init__(self, profile: RiexNc70HingeProfile,
                 pilot_diameter_mm: float, pilot_depth_mm: float):
        self.profile = profile
        self.pilot_diameter_mm = pilot_diameter_mm
        self.pilot_depth_mm = pilot_depth_mm

    def build(self):
        profile = self.profile
        fixing_offset = profile.cup_fixing_line_from_edge_mm-profile.cup_center_from_edge_mm
        cup = SurfaceHole("cup", 0, 0, profile.cup_diameter_mm, profile.cup_depth_mm)
        pilots = tuple(SurfaceHole(f"fixing_{index}", fixing_offset, y,
                                  self.pilot_diameter_mm, self.pilot_depth_mm)
                       for index, y in enumerate((-profile.cup_fixing_spacing_mm/2,
                                                 profile.cup_fixing_spacing_mm/2), 1))
        return SurfaceHolePattern((cup, *pilots))
