"""Scope: Render one resolved local assembly specification as Python source."""

from __future__ import annotations

from assembly_taxonomy import (
    BaseAssemblyTaxonomy,
    BoundaryPoint,
    CabineoJointTaxonomy,
    JointTaxonomy,
    LocalAssemblyTaxonomy,
)
from part_spec_source_renderer import PartSpecSourceRenderer


class AssemblySpecRenderer:
    """Keep every generated local value in one authoritative specification."""

    def __init__(self) -> None:
        self.parts = PartSpecSourceRenderer()

    def render(self, assembly: LocalAssemblyTaxonomy | BaseAssemblyTaxonomy) -> str:
        if isinstance(assembly, BaseAssemblyTaxonomy):
            return self._base(assembly)
        return self._storage(assembly)

    def _storage(self, assembly: LocalAssemblyTaxonomy) -> str:
        parts = "\n".join(
            self.parts.render(part) for part in assembly.parts
        )
        joints = "\n".join(self._joint(joint) for joint in assembly.joints)
        top = self._points(assembly.top)
        return (
            f'"""Scope: Own local dimensions, parts, and joints for {assembly.assembly_id}."""\n\n'
            "from assemblies.specification import (\n"
            "    AssemblySpec,\n"
            "    BoundaryPoint,\n"
            "    CabineoJointSpec,\n"
            "    JointSpec,\n"
            "    LocalToParentPlacement,\n"
            "    PartSpec,\n"
            "    Point3D,\n"
            "    AxisBasis,\n"
            "    AxisDirection,\n"
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
            f"    door_bottom={assembly.door_bottom!r},\n"
            f"    door_bottom_mm={assembly.door_bottom_mm!r},\n"
            "    parts=(\n"
            f"{parts}\n"
            "    ),\n"
            "    joints=(\n"
            f"{joints}\n"
            "    ),\n"
            ")\n"
        )

    def _base(self, assembly: BaseAssemblyTaxonomy) -> str:
        parts = "\n".join(
            self.parts.render(part) for part in assembly.parts
        )
        joints = "\n".join(self._joint(joint) for joint in assembly.joints)
        modules = "\n".join(
            "        BaseModuleSpec("
            f"{module.module_id!r}, {module.start_x_mm!r}, {module.end_x_mm!r}),"
            for module in assembly.modules
        )
        return (
            f'"""Scope: Own local dimensions, parts, and joints for {assembly.assembly_id}."""\n\n'
            "from assemblies.specification import (\n"
            "    BaseAssemblySpec,\n"
            "    BaseModuleSpec,\n"
            "    CabineoJointSpec,\n"
            "    JointSpec,\n"
            "    LocalToParentPlacement,\n"
            "    PartSpec,\n"
            "    Point3D,\n"
            "    AxisBasis,\n"
            "    AxisDirection,\n"
            ")\n\n\n"
            "SPEC = BaseAssemblySpec(\n"
            f"    assembly_id={assembly.assembly_id!r},\n"
            f"    purpose={assembly.purpose!r},\n"
            f"    global_left_mm={assembly.global_left_mm!r},\n"
            f"    global_right_mm={assembly.global_right_mm!r},\n"
            f"    width_mm={assembly.width_mm!r},\n"
            f"    depth_mm={assembly.depth_mm!r},\n"
            f"    height_mm={assembly.height_mm!r},\n"
            f"    plinth_front={assembly.plinth_front!r},\n"
            f"    plinth_recess_mm={assembly.plinth_recess_mm!r},\n"
            "    modules=(\n"
            f"{modules}\n"
            "    ),\n"
            "    parts=(\n"
            f"{parts}\n"
            "    ),\n"
            "    joints=(\n"
            f"{joints}\n"
            "    ),\n"
            ")\n"
        )

    def _joint(self, joint: JointTaxonomy | CabineoJointTaxonomy) -> str:
        if isinstance(joint, CabineoJointTaxonomy):
            return (
                "        CabineoJointSpec(\n"
                f"            joint_id={joint.joint_id!r},\n"
                f"            source_part_id={joint.source_part_id!r},\n"
                f"            target_part_id={joint.target_part_id!r},\n"
                f"            source_face={joint.source_face!r},\n"
                f"            source_edge={joint.source_edge!r},\n"
                f"            connector_layout={joint.connector_layout!r},\n"
                f"            purpose={joint.purpose!r},\n"
                "        ),"
            )
        return (
            "        JointSpec(\n"
            f"            joint_id={joint.joint_id!r},\n"
            f"            participant_ids={joint.participant_ids!r},\n"
            f"            purpose={joint.purpose!r},\n"
            f"            joint_type={joint.joint_type!r},\n"
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
