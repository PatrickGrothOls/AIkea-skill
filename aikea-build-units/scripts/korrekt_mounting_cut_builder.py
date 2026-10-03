"""Scope: Resolve recorded Korrekt participant cuts from the current plate and panel frames."""

from korrekt_mounting_cutter import KorrektMountingCutter
from local_to_parent_location import LocalToParentLocation
from part_construction_error import PartConstructionError
from part_cut import AssemblyCuts, PartCut


class KorrektMountingCutBuilder:
    def __init__(self):
        self.cutter = KorrektMountingCutter()
        self.locations = LocalToParentLocation()

    def plate(self, assembly, hardware_id):
        hardware = next(item for item in assembly.purchased_hardware if item.hardware_id == hardware_id)
        if (hardware.manufacturer != "Hettich" or hardware.product_code != "61854" or
                hardware.local_to_parent is None):
            raise PartConstructionError("Korrekt machining requires a placed Hettich 61854 plate")
        return hardware

    def build(self, assembly, joints):
        parts = {part.part_id: part for part in assembly.parts}
        cuts = []
        for joint in joints:
            if joint.joint_type != "korrekt_mounting":
                raise PartConstructionError("Korrekt cut builder requires a recorded mounting operation")
            part = parts[joint.part_id]
            plate = self.plate(assembly, joint.hardware_id)
            negative = self.cutter.cutout(part.local_size_mm[2])
            location = self.locations.build(part.local_to_parent).inverse * self.locations.build(plate.local_to_parent)
            cuts.append(PartCut(joint.joint_id, part.part_id, 1, negative, location))
        return AssemblyCuts(tuple(cuts))
