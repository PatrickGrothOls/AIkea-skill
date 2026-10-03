"""Scope: Declare and build overlapping pocket regions from one accessible surface."""

from dataclasses import dataclass, field, replace
from math import isfinite
from typing import Any

from local_to_parent_location import LocalToParentLocation
from surface_pocket_builder import SurfacePocketBuilder
from surface_pocket_spec import SurfacePocketSpec


@dataclass(frozen=True)
class RecessRegion:
    start_mm: tuple[float, float]
    length_mm: float
    width_mm: float
    depth_mm: float
    corner_radius_mm: float


@dataclass(frozen=True)
class SteppedSurfaceRecessSpec:
    machining_id: str
    part_id: str
    surface_to_part: Any
    regions: tuple[RecessRegion, ...]
    operation_type: str = field(default="stepped_surface_recess", init=False)

    def __post_init__(self):
        if not self.regions:
            raise ValueError("a stepped recess requires regions")

    @property
    def depth_mm(self):
        """Shallowest region governs whether the whole operation is through-cut."""
        return min(region.depth_mm for region in self.regions)


class SteppedSurfaceRecessBuilder:
    def build(self, part, request):
        cutters = []
        for index, region in enumerate(request.regions):
            if not all(isfinite(value) for value in region.start_mm):
                raise ValueError("recess region positions must be finite")
            frame = request.surface_to_part
            x, y = region.start_mm
            basis, origin = frame.axis_basis, frame.origin_in_parent
            coordinates = {axis+"_mm": getattr(origin, axis+"_mm")
                           + x*getattr(basis.local_x_in_parent, axis)
                           + y*getattr(basis.local_y_in_parent, axis) for axis in ("x", "y", "z")}
            placed = replace(frame, origin_in_parent=replace(origin, **coordinates))
            pocket = SurfacePocketSpec(f"{request.machining_id}_{index}", request.part_id,
                placed, region.length_mm, region.width_mm, region.depth_mm, region.corner_radius_mm)
            cutter, _ = SurfacePocketBuilder().build(part, pocket)
            cutters.append(cutter.translate((x, y, 0)))
        combined = cutters[0]
        for cutter in cutters[1:]:
            combined = combined.fuse(cutter)
        return combined.clean(), LocalToParentLocation().build(request.surface_to_part)
