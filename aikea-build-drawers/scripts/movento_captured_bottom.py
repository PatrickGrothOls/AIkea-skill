"""Scope: Resolve a retained MOVENTO floor and its four wall grooves from one datum."""

from surface_groove_spec import SurfaceGrooveSpec
from surface_pocket_spec import SurfacePocketSpec
from cabineo_connector_layout import CabineoConnectorLayout


class MoventoCapturedBottom:
    """Proposed stock-fit allowances; source runner datums remain unchanged.

    14.5 mm is within the registered 12–15 mm bottom-recess range and clears
    the nominal rear-hook bore (top at 14 mm). Validate tolerances on real stock.
    """

    underside_mm = 14.5
    thickness_mm = 16
    groove_depth_mm = 6
    fit_clearance_mm = .2

    @property
    def engagement_mm(self):
        return self.groove_depth_mm - self.fit_clearance_mm

    def floor(self, dimensions):
        engagement = self.engagement_mm
        size = (dimensions.inside_width_mm + 2*engagement, 474 + 2*engagement, self.thickness_mm)
        origin = (21-engagement, -engagement, self.underside_mm)
        return size, origin

    def grooves(self, dimensions, frame):
        width = self.thickness_mm + self.fit_clearance_mm
        center = self.underside_mm + width/2
        inner = ((1,0,0),(0,-1,0),(0,0,-1))
        rows = (("left",490,center), ("right",490,center),
                ("back",dimensions.inside_width_mm,center-.5))
        grooves = tuple(SurfaceGrooveSpec("bottom_groove_"+part, part,
                        frame((0,height,16),inner),length,width,self.groove_depth_mm)
                        for part,length,height in rows)
        # Overrun past the floor's square corners leaves them in the straight
        # section of this stopped R3 pocket; its rounded ends stay inside the front.
        front = SurfacePocketSpec("bottom_groove_front", "front",
            frame((5-dimensions.front_left_mm,center-dimensions.front_bottom_mm,0)),
            dimensions.clear_width_mm-10,width,self.groove_depth_mm,corner_radius_mm=3)
        return grooves + (front,)

    def wall_positions(self, height):
        """Locate above the groove, along the edge; never inset the joining edge."""
        return CabineoConnectorLayout().between(48, height-24)


__all__ = ["MoventoCapturedBottom"]
