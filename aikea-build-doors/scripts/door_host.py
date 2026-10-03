"""Scope: Resolve an upright door and its owned mounting support from actual part frames."""

from dataclasses import dataclass
from math import isfinite

from door_hinge_side import DoorHingeSide
from hardware_placement import HardwarePlacement


@dataclass(frozen=True)
class DoorHostSpec:
    door_part_id: str
    support_part_id: str
    door_assembly_id: str | None = None


class DoorHost:
    """Support one front-facing slab and an upright broad-face hinge support."""

    def __init__(self, assembly, declaration, hinge_side, fixed_reservations=()):
        self.assembly, self.spec, self.hinge_side = assembly, declaration, hinge_side
        self.assembly_id = assembly.assembly_id
        self.fixed_reservations = fixed_reservations
        ids = (declaration.door_part_id, declaration.support_part_id)
        if len(set(ids)) != 2 or not set(ids) <= {part.part_id for part in assembly.parts}:
            raise ValueError("door and hinge support must be distinct parts owned by the assembly")
        self.door, self.support = (assembly.part(name) for name in ids)
        self.door_frame, self.support_frame = (self._frame(part) for part in (self.door, self.support))
        expected_door = ((1, 0, 0), (0, 0, 1), (0, -1, 0))
        left = hinge_side is DoorHingeSide.LEFT
        if self.door.inside_face != "<Z" or self.support.inside_face not in ("<Z", ">Z"):
            raise ValueError("door host requires declared door-back and support broad faces")
        sign = 1 if self.support.inside_face == ">Z" else -1
        normal = tuple(sign*value for value in self.support_frame.local_z_in_owner)
        checks = (*zip(self.door_frame.axes, expected_door),
                  (self.support_frame.local_y_in_owner, (0, 0, 1)),
                  (normal, (1 if left else -1, 0, 0)))
        coordinates = (*self.door.local_size_mm, *self.support.local_size_mm,
                       *self.door_frame.origin_mm, *self.support_frame.origin_mm)
        if (not all(isfinite(value) for value in coordinates) or
                any(value <= 0 for part in (self.door, self.support) for value in part.local_size_mm) or
                any(not isfinite(a) or abs(a-b) > 1e-9 for first, second in checks for a, b in zip(first, second))):
            raise ValueError("door host requires finite positive panels, an upright front and the selected opposing support face")

    def _frame(self, part):
        placement = part.local_to_parent
        point, basis = placement.origin_in_parent, placement.axis_basis
        axes = tuple((axis.x, axis.y, axis.z) for axis in
                     (basis.local_x_in_parent, basis.local_y_in_parent, basis.local_z_in_parent))
        return HardwarePlacement((point.x_mm, point.y_mm, point.z_mm), *axes)

    @property
    def dimensions(self):
        width, height, thickness = self.door.local_size_mm
        heights = tuple(max(point.height_mm for point in self.door.outline_mm if abs(point.x_mm-edge) < 1e-6)
                        for edge in (0, width)) if self.door.outline_mm else (height, height)
        return dict(width=width, left_height=heights[0], right_height=heights[1], thickness=thickness)

    @property
    def door_bottom_mm(self):
        return self.door_frame.origin_mm[2]

    @property
    def support_bottom_mm(self):
        return self.support_frame.origin_mm[2]

    @property
    def front_mm(self):
        return self.door_frame.origin_mm[1]

    @property
    def support_front_mm(self):
        return min(self.support_frame.origin_mm[1], self.support_frame.to_owner((self.support.local_size_mm[0], 0, 0))[1])

    @property
    def inside_x_mm(self):
        z = self.support.local_size_mm[2] if self.support.inside_face == ">Z" else 0
        return self.support_frame.to_owner((0, 0, z))[0]

    @property
    def door_edge_x_mm(self):
        return self.door_frame.origin_mm[0] + (0 if self.hinge_side is DoorHingeSide.LEFT else self.door.local_size_mm[0])

    @property
    def overlay_mm(self):
        return (self.inside_x_mm-self.door_edge_x_mm) * (1 if self.hinge_side is DoorHingeSide.LEFT else -1)

    def require_current_plan(self, plan, profile):
        dimensions = self.dimensions
        pairs = ((plan.door_width_mm, dimensions["width"]),
                 (plan.door_height_mm, dimensions[self.hinge_side.door_height_dimension]),
                 (plan.door_thickness_mm, dimensions["thickness"]), (plan.overlay_mm, self.overlay_mm))
        aligned = all(isfinite(item.door_height_mm) and isfinite(item.cabinet_height_mm) and
                      abs(self.door_bottom_mm+item.door_height_mm-self.support_bottom_mm-item.cabinet_height_mm) <= 1e-6
                      for item in plan.placements)
        if ((plan.host_spec is not None and plan.host_spec != self.spec) or
                plan.assembly_id != self.assembly_id or plan.profile_id != profile.profile_id or
                plan.relationship != profile.relationship or not aligned or
                any(not isfinite(actual) or abs(actual-current) > 1e-6 for actual, current in pairs)):
            raise ValueError("hinge plan differs from current door/support geometry; replan before generating")

    @classmethod
    def resolve(cls, assembly, hinge_side, declaration=None):
        if isinstance(assembly, cls):
            if assembly.hinge_side is not hinge_side:
                raise ValueError("door host and requested hinge hand disagree")
            return assembly
        if declaration is not None and declaration.door_assembly_id is not None:
            from assembly_door_host import AssemblyDoorHost
            return AssemblyDoorHost(assembly, declaration, hinge_side)
        assembly = getattr(assembly, "spec", assembly)
        if declaration is not None:
            return cls(assembly, declaration, hinge_side)
        from cabinet_feature_reservations import CabinetFeatureReservations
        declaration = DoorHostSpec("door_panel", hinge_side.side_part_id)
        fixed = CabinetFeatureReservations().for_side(assembly, declaration.support_part_id)
        return cls(assembly, declaration, hinge_side, fixed)
