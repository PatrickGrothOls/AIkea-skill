"""Scope: Render one resolved local assembly specification as Python source."""

from __future__ import annotations

from assembly_taxonomy import (
    BoundaryPoint,
    JointTaxonomy,
    LocalAssemblyTaxonomy,
    PartTaxonomy,
)


class AssemblySpecRenderer:
    """Keep every generated local value in one authoritative specification."""

    def render(self, assembly: LocalAssemblyTaxonomy) -> str:
        parts = "\n".join(self._part(part) for part in assembly.parts)
        joints = "\n".join(self._joint(joint) for joint in assembly.joints)
        top = self._points(assembly.top)
        return (
            f'"""Scope: Own local dimensions, parts, and joints for {assembly.assembly_id}."""\n\n'
            "from assemblies.specification import (\n"
            "    AssemblySpec,\n"
            "    BoundaryPoint,\n"
            "    JointSpec,\n"
            "    PartSpec,\n"
            ")\n\n\n"
            "SPEC = AssemblySpec(\n"
            f"    assembly_id={assembly.assembly_id!r},\n"
            f"    purpose={assembly.purpose!r},\n"
            f"    global_left_mm={assembly.global_left_mm!r},\n"
            f"    global_right_mm={assembly.global_right_mm!r},\n"
            f"    width_mm={assembly.width_mm!r},\n"
            f"    top={top},\n"
            f"    depth_mm={assembly.depth_mm!r},\n"
            f"    inside_depth_mm={assembly.inside_depth_mm!r},\n"
            f"    door_width_mm={assembly.door_width_mm!r},\n"
            f"    base_height_mm={assembly.base_height_mm!r},\n"
            "    parts=(\n"
            f"{parts}\n"
            "    ),\n"
            "    joints=(\n"
            f"{joints}\n"
            "    ),\n"
            ")\n"
        )

    def _part(self, part: PartTaxonomy) -> str:
        return (
            "        PartSpec(\n"
            f"            part_id={part.part_id!r},\n"
            f"            role={part.role!r},\n"
            f"            dimensions_mm={part.dimensions_mm!r},\n"
            f"            outline_mm={self._points(part.outline_mm)},\n"
            "        ),"
        )

    def _joint(self, joint: JointTaxonomy) -> str:
        return (
            "        JointSpec(\n"
            f"            joint_id={joint.joint_id!r},\n"
            f"            participant_ids={joint.participant_ids!r},\n"
            f"            purpose={joint.purpose!r},\n"
            "        ),"
        )

    def _points(self, points: tuple[BoundaryPoint, ...]) -> str:
        if not points:
            return "()"
        values = ", ".join(
            f"BoundaryPoint({point.x_mm!r}, {point.height_mm!r})" for point in points
        )
        suffix = "," if len(points) == 1 else ""
        return f"({values}{suffix})"
