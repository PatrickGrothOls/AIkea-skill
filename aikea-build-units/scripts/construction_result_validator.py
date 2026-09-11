"""Scope: Verify declared machining against the actual returned parts and cutters."""

from math import isfinite

from assembly_joint_machining_builder import AssemblyJointMachiningBuilder
from construction_cut_validator import ConstructionCutValidator
from panel_blank_builder import PanelBlankBuilder
from panel_machining_builder import PanelMachiningBuilder
from part_construction_error import PartConstructionError
from surface_drilling_reuse import SurfaceDrillingReuse


class BuiltConstructionSpecification:
    """Read the construction contract from current or older built assemblies."""

    def __init__(self, assembly):
        self.parts = tuple(part.spec for part in assembly.parts)
        self.joints = assembly.joints
        self.machining = getattr(assembly.spec, "machining", ())

    def part(self, part_id):
        return next(part for part in self.parts if part.part_id == part_id)


class ConstructionResultValidator:
    """Check all builders at their output boundary, independently of execution."""

    TOLERANCE_MM3 = 1e-5
    BUILTIN_JOINTS = frozenset(("cabineo", "equal_thickness_miter"))

    def validate(self, assembly):
        spec = BuiltConstructionSpecification(assembly)
        parts = self._parts(assembly)
        declared = getattr(assembly.spec, "joints", assembly.joints)
        if declared != assembly.joints:
            raise PartConstructionError("built joints differ from their declared specification")
        validation = ConstructionCutValidator(allow_unresolved=True)
        validation.validate_spec(spec)
        validation.validate_cuts(spec, assembly.cuts)
        expected = self._builtin_cuts(spec)
        actual = {self._identity(cut): cut for cut in assembly.cuts}
        expected_ids = {self._identity(cut) for cut in expected}
        builtin_ids = {cut.joint_id for cut in expected}
        if {key for key in actual if key[0] in builtin_ids} != expected_ids:
            raise PartConstructionError("built-in cut occurrences differ from their construction inputs")
        for cut in expected:
            received = actual[self._identity(cut)]
            left = cut.cutter.located(cut.location)
            right = received.cutter.located(received.location)
            difference = left.cut(right).Volume() + right.cut(left).Volume()
            if difference > self.TOLERANCE_MM3:
                raise PartConstructionError(f"{cut.joint_id}: cutter differs from its construction inputs")
        blanks = {part_id: PanelBlankBuilder().build(parts[part_id].spec).val()
                  for part_id in {cut.part_id for cut in assembly.cuts}}
        self._local_requests_fit(spec, assembly.cuts, blanks)
        for cut in assembly.cuts:
            cutter = cut.cutter.located(cut.location)
            if not cutter.isValid() or not cutter.Solids() or cutter.Volume() <= self.TOLERANCE_MM3:
                raise PartConstructionError(f"{cut.joint_id}: invalid cutter solid")
            if blanks[cut.part_id].intersect(cutter).Volume() <= self.TOLERANCE_MM3:
                raise PartConstructionError(f"{cut.joint_id}: cutter misses its declared participant")
            if parts[cut.part_id].solid.val().intersect(cutter).Volume() > self.TOLERANCE_MM3:
                raise PartConstructionError(f"{cut.joint_id}: machining is absent from {cut.part_id}")
        return tuple(joint for joint in spec.joints
                     if joint.joint_type not in self.BUILTIN_JOINTS | {"unresolved"})

    def _builtin_cuts(self, spec):
        joints = tuple(joint for joint in spec.joints if joint.joint_type in self.BUILTIN_JOINTS)
        return (AssemblyJointMachiningBuilder(strict=True).build(spec, joints).all
                + PanelMachiningBuilder().build(spec).all)

    def _local_requests_fit(self, spec, cuts, blanks):
        local_ids = {request.machining_id for request in spec.machining}
        preceding = [cut for cut in cuts if cut.joint_id not in local_ids]
        for request in spec.machining:
            cut = next(cut for cut in cuts if cut.joint_id == request.machining_id)
            cutter = cut.cutter.located(cut.location)
            blank = blanks[cut.part_id]
            in_blank = blank.intersect(cutter)
            reuse = SurfaceDrillingReuse().resolve(request, preceding, local_ids)
            clipped = cutter.Volume() - in_blank.Volume() > self.TOLERANCE_MM3
            overlaps = (in_blank.intersect(prior.cutter.located(prior.location))
                        for prior in preceding if prior.part_id == cut.part_id)
            collides = any(overlap.Volume() > self.TOLERANCE_MM3
                           and (overlap.cut(reuse) if reuse is not None else overlap).Volume()
                           > self.TOLERANCE_MM3 for overlap in overlaps)
            if clipped or collides:
                raise PartConstructionError(f"{cut.joint_id}: local machining is clipped by the panel or earlier cuts")
            preceding.append(cut)

    def _parts(self, assembly):
        parts = {part.spec.part_id: part for part in assembly.parts}
        if len(parts) != len(assembly.parts):
            raise PartConstructionError("built part IDs must be unique")
        for part in parts.values():
            if len(part.solid.vals()) != 1:
                raise PartConstructionError(f"{part.spec.part_id}: expected one physical shape")
            shape = part.solid.val()
            if (not shape.isValid() or not shape.Solids() or not isfinite(shape.Volume())
                    or shape.Volume() <= self.TOLERANCE_MM3):
                raise PartConstructionError(f"{part.spec.part_id}: invalid manufactured solid")
        return parts

    def _identity(self, cut):
        return cut.joint_id, cut.part_id, cut.connector_index
