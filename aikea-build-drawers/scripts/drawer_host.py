"""Scope: Resolve an explicit drawer bay from owned support panels and clear-space limits."""

from dataclasses import dataclass
from math import isfinite

from drawer_hardware_mounting_plan import HardwarePlacement


@dataclass(frozen=True)
class DrawerHostSpec:
    left_part_id: str
    right_part_id: str
    front_mm: float
    inside_depth_mm: float
    bottom_mm: float
    top_mm: float


class DrawerHost:
    """Support upright opposing sheet faces in this owner's X/Y/Z frame."""

    def __init__(self, assembly, spec):
        self.assembly = assembly
        self.spec = spec
        self.assembly_id = assembly.assembly_id
        values = (spec.front_mm, spec.inside_depth_mm, spec.bottom_mm, spec.top_mm)
        if not all(isfinite(value) for value in values) or spec.inside_depth_mm <= 0 or spec.top_mm <= spec.bottom_mm:
            raise ValueError("drawer host requires finite positive clear space")
        if spec.left_part_id == spec.right_part_id:
            raise ValueError("drawer host requires two distinct owned support panels")
        if not {spec.left_part_id, spec.right_part_id} <= {part.part_id for part in assembly.parts}:
            raise ValueError("drawer host supports must be owned by the selected assembly")
        for side, expected in (("left", (1, 0, 0)), ("right", (-1, 0, 0))):
            part, frame = self.part(side), self.frame(side)
            if part.inside_face not in ("<Z", ">Z"):
                raise ValueError("drawer support must declare its inside face")
            sign = 1 if part.inside_face == ">Z" else -1
            normal = tuple(sign * value for value in frame.local_z_in_owner)
            axes = ((normal, expected), (frame.local_y_in_owner, (0, 0, 1)))
            if any(abs(actual-target) > 1e-9 for first, second in axes for actual, target in zip(first, second)):
                raise ValueError("drawer host requires opposing X faces and upright panel Y axes")
        if self.clear_width_mm <= 0:
            raise ValueError("drawer host inside faces must enclose positive width")

    def part(self, side):
        return self.assembly.part(getattr(self.spec, f"{side}_part_id"))

    def frame(self, side):
        placement = self.part(side).local_to_parent
        origin, basis = placement.origin_in_parent, placement.axis_basis
        axes = tuple((axis.x, axis.y, axis.z) for axis in
                     (basis.local_x_in_parent, basis.local_y_in_parent, basis.local_z_in_parent))
        return HardwarePlacement((origin.x_mm, origin.y_mm, origin.z_mm), *axes)

    def inside_x(self, side):
        part = self.part(side)
        z = part.local_size_mm[2] if part.inside_face == ">Z" else 0
        return self.frame(side).to_owner((0, 0, z))[0]

    @property
    def clear_width_mm(self):
        return self.inside_x("right") - self.inside_x("left")

    def row_in_part(self, side, owner_height_mm):
        return self.frame(side).to_local((self.inside_x(side), self.spec.front_mm, owner_height_mm))[1]

    @classmethod
    def resolve(cls, assembly):
        """Retain standard-cabinet callers through a confined recipe adapter."""
        if isinstance(assembly, cls):
            return assembly
        from standard_drawer_host import StandardDrawerHost
        return StandardDrawerHost().resolve(assembly)
