"""Scope: Materialize explicitly designed panels and joints in any assembly tree."""

from assembly_joint_machining_builder import AssemblyJointMachiningBuilder
from construction_cut_validator import ConstructionCutValidator
from panel_blank_builder import PanelBlankBuilder
from panel_machining_builder import PanelMachiningBuilder
from part_construction_error import PartConstructionError
from part_cut import AssemblyCuts
from .construction_specification import PanelAssemblySpec, PartMachiningSpec
from .specification import BuiltAssembly, BuiltPart


class PanelAssemblyBuilder:
    """Apply paired cuts and retain authored children and purchased hardware."""

    def __init__(self, spec: PanelAssemblySpec, children=(), hardware=(),
                 blank_builder=None, joint_builder=None) -> None:
        self.spec = spec
        self.children = children
        self.hardware = hardware
        self.blanks = blank_builder or PanelBlankBuilder()
        self.joints = joint_builder or AssemblyJointMachiningBuilder(strict=True)
        self.machining = PanelMachiningBuilder()
        self.validation = ConstructionCutValidator()

    def build(self) -> BuiltAssembly:
        identifiers = tuple(part.part_id for part in self.spec.parts)
        if len(set(identifiers)) != len(identifiers):
            raise PartConstructionError("panel IDs must be unique within an assembly")
        self.validation.validate_spec(self.spec)
        blanks = tuple(self.blanks.build(part) for part in self.spec.parts)
        joints = self.joints.build(self.spec, self.spec.joints)
        cuts = AssemblyCuts(joints.all + self.machining.build(self.spec).all)
        self.validation.validate_cuts(self.spec, cuts.all)
        local_ids = {request.machining_id for request in self.spec.machining}
        parts = []
        for part, solid in zip(self.spec.parts, blanks):
            if len(solid.vals()) != 1:
                raise PartConstructionError(
                    f"{part.part_id}: return one Shape per Workplane; use a compound for multiple solids"
                )
            for cut in cuts.for_part(part.part_id):
                cutter = cut.cutter.located(cut.location)
                removed = solid.val().intersect(cutter).Volume()
                if removed <= 1e-6:
                    raise PartConstructionError(
                        f"{cut.joint_id}: cutter does not machine participant {part.part_id}"
                    )
                if cut.joint_id in local_ids and cutter.Volume() - removed > 1e-6:
                    raise PartConstructionError(
                        f"{cut.joint_id}: local machining is clipped by the panel or earlier cuts"
                    )
                solid = solid.cut(cutter)
            if not solid.val().isValid() or solid.val().Volume() <= 1e-6:
                raise PartConstructionError(f"{part.part_id}: machining left no valid material")
            parts.append(BuiltPart(part, solid))
        return BuiltAssembly(
            self.spec, tuple(parts), self.spec.joints, cuts.all,
            self.children, self.hardware,
        )
