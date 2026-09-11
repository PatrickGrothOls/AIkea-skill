"""Scope: Add declared machining to current assembly parts without replacing other features."""

from dataclasses import replace

from assembly_joint_machining_builder import AssemblyJointMachiningBuilder

from construction_cut_validator import ConstructionCutValidator
from construction_result_validator import ConstructionResultValidator
from panel_cut_applicator import PanelCutApplicator
from panel_machining_builder import PanelMachiningBuilder


class PanelMachiningFeature:
    """Use the same cut execution and result boundary as the shared blank builder."""

    def apply(self, assembly, machining=(), requirements=(), *, joints=(), joint_builder=None):
        spec = replace(assembly.spec, joints=assembly.joints+joints, machining=assembly.spec.machining + machining,
                       requirements=(assembly.spec.requirements + requirements
                                     if assembly.spec.requirements is not None else None))
        ConstructionCutValidator(allow_unresolved=True).validate_spec(spec)
        builder = joint_builder or AssemblyJointMachiningBuilder(strict=True)
        cuts = (builder.build(spec, joints).all +
                PanelMachiningBuilder().build(replace(spec, machining=machining)).all)
        requests = {request.machining_id: request for request in spec.machining}
        parts = tuple(replace(part, solid=PanelCutApplicator().apply(
            part.spec, part.solid, tuple(cut for cut in cuts if cut.part_id == part.spec.part_id), requests,
            tuple(cut for cut in assembly.cuts if cut.part_id == part.spec.part_id))) for part in assembly.parts)
        result = replace(assembly, spec=spec, parts=parts, joints=spec.joints, cuts=assembly.cuts + cuts)
        ConstructionResultValidator().validate(result)
        return result
