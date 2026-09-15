"""Scope: Require deliberate fixed storage shelves and hide their Cabineo pockets underneath."""
from dataclasses import dataclass
from part_construction_error import PartConstructionError


@dataclass(frozen=True)
class FixedShelfChoice:
    shelf_id: str
    reason: str


class StorageShelfPolicy:
    def adjustable_ids(self, spec, fixed_choices=()):
        shelves = {part.part_id for part in spec.parts if part.role == "shelf_panel"}
        choices = {choice.shelf_id: choice for choice in fixed_choices}
        if len(choices) != len(fixed_choices) or any(
                key not in shelves or not value.reason.strip() for key,value in choices.items()):
            raise PartConstructionError("Fixed storage shelves need distinct shelf IDs and a recorded reason")
        for joint in spec.joints:
            touched = shelves.intersection(joint.participant_ids)
            if joint.joint_type != "cabineo" or not touched:
                continue
            if touched != {joint.source_part_id} or joint.source_part_id not in choices:
                raise PartConstructionError("Storage shelf Cabineos require a deliberate FixedShelfChoice")
            if joint.source_face != "<Z":
                raise PartConstructionError("Fixed shelf Cabineo pockets must be on the hidden underside (<Z)")
        return tuple(part.part_id for part in spec.parts if part.part_id in shelves-choices.keys())
