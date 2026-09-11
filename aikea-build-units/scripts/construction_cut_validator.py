"""Scope: Validate declared operation ownership and returned participant cuts."""

from part_construction_error import PartConstructionError
from cabineo_connector_layout import CabineoConnectorLayout


class ConstructionCutValidator:
    """Apply identical operation-accounting rules to built-in and injected tools."""

    def validate_spec(self, spec):
        joint_ids = tuple(joint.joint_id for joint in spec.joints)
        machining_ids = tuple(item.machining_id for item in spec.machining)
        operation_ids = joint_ids + machining_ids
        if len(set(operation_ids)) != len(operation_ids):
            raise PartConstructionError("machining and joint IDs must be unique")
        known = {part.part_id for part in spec.parts}
        if any(part not in known for _, part in self.required(spec)):
            raise PartConstructionError("construction operations must reference owned parts")

    def validate_cuts(self, spec, cuts):
        required = self.required(spec)
        supplied = {(cut.joint_id, cut.part_id) for cut in cuts}
        identities = tuple((cut.joint_id, cut.part_id, cut.connector_index) for cut in cuts)
        if len(set(identities)) != len(identities):
            raise PartConstructionError("cut identities must be unique per participant")
        if supplied != required:
            raise PartConstructionError(
                "machining cuts must account for every declared joint participant "
                f"and local operation; missing={sorted(required - supplied)}, "
                f"undeclared={sorted(supplied - required)}"
            )
        for joint in spec.joints:
            if joint.joint_type != "cabineo":
                continue
            positions = CabineoConnectorLayout().positions(joint, spec.part(joint.source_part_id))
            expected = {(joint.joint_id, part, index)
                        for part in joint.participant_ids for index in range(1, len(positions) + 1)}
            actual = {identity for identity in identities if identity[0] == joint.joint_id}
            if actual != expected:
                raise PartConstructionError(f"{joint.joint_id}: incomplete Cabineo occurrence cuts")

    def required(self, spec):
        return {
            (joint.joint_id, participant)
            for joint in spec.joints for participant in joint.participant_ids
        } | {(item.machining_id, item.part_id) for item in spec.machining}
