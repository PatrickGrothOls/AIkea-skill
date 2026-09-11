"""Scope: Materialize explicitly designed panels and joints in any assembly tree."""

from assembly_joint_machining_builder import AssemblyJointMachiningBuilder
from construction_cut_validator import ConstructionCutValidator
from panel_blank_builder import PanelBlankBuilder
from panel_cut_applicator import PanelCutApplicator
from panel_machining_builder import PanelMachiningBuilder
from part_construction_error import PartConstructionError
from part_cut import AssemblyCuts
from .construction_specification import ConstructionSpecification, PanelAssemblySpec, PartMachiningSpec
from .specification import BuiltAssembly, BuiltPart


class PanelAssemblyBuilder:
    """Apply paired cuts and retain authored children and purchased hardware."""

    def __init__(self, spec: ConstructionSpecification, children=(), hardware=(),
                 blank_builder=None, joint_builder=None, allow_unresolved=False) -> None:
        self.spec = spec
        self.children = children
        self.hardware = hardware
        self.blanks = blank_builder or PanelBlankBuilder()
        self.joints = joint_builder or AssemblyJointMachiningBuilder(
            strict=True, allow_unresolved=allow_unresolved,
        )
        self.machining = PanelMachiningBuilder()
        self.validation = ConstructionCutValidator(allow_unresolved=allow_unresolved)

    def build(self) -> BuiltAssembly:
        identifiers = tuple(part.part_id for part in self.spec.parts)
        if len(set(identifiers)) != len(identifiers):
            raise PartConstructionError("panel IDs must be unique within an assembly")
        self.validation.validate_spec(self.spec)
        blanks = tuple(self.blanks.build(part) for part in self.spec.parts)
        joints = self.joints.build(self.spec, self.spec.joints)
        cuts = AssemblyCuts(joints.all + self.machining.build(self.spec).all)
        self.validation.validate_cuts(self.spec, cuts.all)
        requests = {request.machining_id: request for request in self.spec.machining}
        parts = tuple(BuiltPart(part, PanelCutApplicator().apply(
            part, solid, cuts.for_part(part.part_id), requests)) for part, solid in zip(self.spec.parts, blanks))
        return BuiltAssembly(
            self.spec, parts, self.spec.joints, cuts.all,
            self.children, self.hardware,
        )
