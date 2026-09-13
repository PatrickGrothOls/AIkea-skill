"""Scope: Apply sourced MOVENTO fixing axes and declared pilot choices to flat panels."""
from dataclasses import dataclass
from surface_drilling_spec import SurfaceDrillingSpec
from surface_hole_pattern import SurfaceHole
from movento_mounting_profile import MOVENTO_760H5000S_MOUNTING
from local_to_parent_location import LocalToParentLocation
import cadquery as cq


@dataclass(frozen=True)
class MoventoPilotChoice:
    """A selected screw/material preparation; qualification is recorded separately."""

    host_diameter_mm: float
    host_depth_mm: float
    clip_diameter_mm: float
    clip_depth_mm: float
    basis: str


class MoventoPanelMachining:
    """Use TD-132/1 pages 5, 13, 19 and the registered T51.7601 source axes.

    Host fixing option B: five 661.1450.HG system screws per 500 mm runner.
    Clip coordinates differ by hand; they are not mirrored from one download.
    Rear hook bores retain nominal axes/diameter but extend through for one setup.
    Source-CAD fit needs requalification; the right-hand download has a mismatch.
    """

    HOST_DEPTHS_MM = tuple(MOVENTO_760H5000S_MOUNTING.drawer_front_to_manufacturer_origin_mm - z
                          for z in MOVENTO_760H5000S_MOUNTING.runner_screw_native_z_mm)
    HOST_ROW_ABOVE_SIDE_BOTTOM_MM = MOVENTO_760H5000S_MOUNTING.drawer_bottom_to_manufacturer_origin_mm

    def drawer(self, dimensions, pilots, frame):
        width = dimensions.clear_width_mm
        inside = dimensions.inside_width_mm
        identity = frame((0, 0, 0))
        return (
            # Keep the sourced axes/diameter; extend through from the groove face
            # to avoid a flip. This extension still needs installation qualification.
            SurfaceDrillingSpec("rear_hooks", "back", frame((0,0,16),
                ((1,0,0),(0,-1,0),(0,0,-1))), (
                SurfaceHole("left", 7, -10.5, 6, 16),
                SurfaceHole("right", inside-7, -10.5, 6, 16))),
            SurfaceDrillingSpec("locking_clips", "rail", identity, tuple(
                SurfaceHole(str(i), x-21, 6.8, pilots.clip_diameter_mm, pilots.clip_depth_mm)
                for i, x in enumerate((37.5, 60.5, width-37, width-60)))),
            # The source runner rises 0.2 mm into this support. Local underside
            # reliefs clear it without shifting the clip's flush mounting plane.
            SurfaceDrillingSpec("runner_relief", "rail", identity, (
                SurfaceHole("left", 14.37, 33, 12, .5),
                SurfaceHole("right", inside-14.37, 33, 12, .5))),
        )

    def host(self, machining_id, part, drawer_frame, wall_x, pilots, frame):
        """Transform product axes into the host's actual chosen broad face."""
        placement = LocalToParentLocation()
        transform = placement.build(part.local_to_parent).inverse * placement.build(drawer_frame)
        if part.inside_face not in {"<Z", ">Z"}:
            raise ValueError("runner host needs a chosen broad face")
        upper = part.inside_face == ">Z"
        z, sign = (part.local_size_mm[2], -1) if upper else (0, 1)
        start = cq.Vertex.makeVertex(wall_x,0,0).located(transform).Center()
        end = cq.Vertex.makeVertex(wall_x + (-1 if wall_x == 0 else 1),0,0).located(transform).Center()
        axis = end-start
        if max(abs(axis.x),abs(axis.y),abs(axis.z-sign)) > 1e-6:
            raise ValueError("runner screw axes must enter perpendicular to the selected host face")
        surface = frame((0,0,z), ((1,0,0),(0,sign,0),(0,0,sign)))
        holes = []
        for i, depth in enumerate(self.HOST_DEPTHS_MM):
            point = cq.Vertex.makeVertex(wall_x, depth, self.HOST_ROW_ABOVE_SIDE_BOTTOM_MM).located(transform).Center()
            if abs(point.z-z) > 1e-6:
                raise ValueError("runner fixing datum does not lie on the selected host face")
            holes.append(SurfaceHole(str(i),point.x,sign*point.y,pilots.host_diameter_mm,pilots.host_depth_mm))
        return SurfaceDrillingSpec(machining_id, part.part_id, surface, tuple(holes))


__all__ = ["MoventoPanelMachining", "MoventoPilotChoice"]
