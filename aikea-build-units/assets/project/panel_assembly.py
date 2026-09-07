"""Scope: Materialize explicitly designed panels and joints in any assembly tree."""

from dataclasses import dataclass
from typing import Any

from assembly_joint_machining_builder import AssemblyJointMachiningBuilder
from blank_sheet_builder import BlankSheetBuilder
from part_construction_error import PartConstructionError
from .specification import BuiltAssembly, BuiltPart, PartSpec


@dataclass(frozen=True)
class PanelAssemblySpec:
    """Own geometry and connections without a furniture-type template."""

    assembly_id: str
    purpose: str
    parts: tuple[PartSpec, ...] = ()
    joints: tuple[Any, ...] = ()
    child_assemblies: tuple[Any, ...] = ()
    purchased_hardware: tuple[Any, ...] = ()

    def part(self, part_id: str) -> PartSpec:
        return next(part for part in self.parts if part.part_id == part_id)


class PanelBlankBuilder:
    """Build an explicitly sized blank; semantic roles never add machining."""

    def build(self, part: PartSpec) -> Any:
        if len(part.local_size_mm) != 3 or min(part.local_size_mm) <= 0:
            raise PartConstructionError(f"{part.part_id}: positive local size required")
        if part.outline_mm:
            outline = tuple((p.x_mm, p.height_mm) for p in part.outline_mm)
            return BlankSheetBuilder(outline, part.local_size_mm[2]).build()
        return BlankSheetBuilder.rectangle(*part.local_size_mm).build()


class PanelAssemblyBuilder:
    """Apply paired cuts and retain authored children and purchased hardware."""

    def __init__(self, spec: PanelAssemblySpec, children=(), hardware=(),
                 blank_builder=None, joint_builder=None) -> None:
        self.spec = spec
        self.children = children
        self.hardware = hardware
        self.blanks = blank_builder or PanelBlankBuilder()
        self.joints = joint_builder or AssemblyJointMachiningBuilder(strict=True)

    def build(self) -> BuiltAssembly:
        identifiers = tuple(part.part_id for part in self.spec.parts)
        if len(set(identifiers)) != len(identifiers):
            raise PartConstructionError("panel IDs must be unique within an assembly")
        cuts = self.joints.build(self.spec, self.spec.joints)
        self._validate_cut_ownership(cuts)
        parts = []
        for part in self.spec.parts:
            solid = self.blanks.build(part)
            if len(solid.vals()) != 1:
                raise PartConstructionError(
                    f"{part.part_id}: return one Shape per Workplane; use a compound for multiple solids"
                )
            for cut in cuts.for_part(part.part_id):
                cutter = cut.cutter.located(cut.location)
                if solid.val().intersect(cutter).Volume() <= 1e-6:
                    raise PartConstructionError(
                        f"{cut.joint_id}: cutter does not machine participant {part.part_id}"
                    )
                solid = solid.cut(cutter)
            parts.append(BuiltPart(part, solid))
        return BuiltAssembly(
            self.spec, tuple(parts), self.spec.joints, cuts.all,
            self.children, self.hardware,
        )

    def _validate_cut_ownership(self, cuts) -> None:
        joint_ids = tuple(joint.joint_id for joint in self.spec.joints)
        if len(joint_ids) != len(set(joint_ids)):
            raise PartConstructionError("machining joint IDs must be unique")
        required = {
            (joint.joint_id, participant)
            for joint in self.spec.joints for participant in joint.participant_ids
        }
        supplied = {(cut.joint_id, cut.part_id) for cut in cuts.all}
        known_parts = {part.part_id for part in self.spec.parts}
        if supplied != required or any(part_id not in known_parts for _, part_id in required):
            raise PartConstructionError(
                "machining cuts must account for every declared joint participant "
                f"and reference owned parts; missing={sorted(required - supplied)}, "
                f"undeclared={sorted(supplied - required)}"
            )
