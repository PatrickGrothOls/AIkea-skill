"""Scope: Apply each declared Korrekt plate's negative to its supporting deck parts."""

from dataclasses import dataclass
from math import pi
from typing import Any

import cadquery as cq

from blank_sheet_builder import BlankSheetBuilder
from korrekt_mounting_cutter import KorrektMountingCutter
from korrekt_plate_clearance import KorrektPlateClearance
from local_to_parent_location import LocalToParentLocation
from part_construction_error import PartConstructionError
from panel_machining_feature import PanelMachiningFeature
from korrekt_mounting_cut_builder import KorrektMountingCutBuilder


@dataclass(frozen=True)
class KorrektMountingJoint:
    joint_id: str
    part_id: str
    hardware_id: str
    plate_edge_clearance_mm: float
    minimum_edge_margin_mm: float
    joint_type: str = "korrekt_mounting"

    @property
    def participant_ids(self) -> tuple[str, ...]:
        return (self.part_id,)


class KorrektMountingMachining:
    """Use declared hardware placement even when its detailed visual CAD is absent."""

    def __init__(self) -> None:
        self.cutter = KorrektMountingCutter()
        self.locations = LocalToParentLocation()
        self.cut_builder = KorrektMountingCutBuilder()

    def apply(self, built: Any, deck_part_ids: tuple[str, ...],
              plate_hardware_ids: tuple[str, ...], *, minimum_edge_margin_mm: float) -> Any:
        parts_by_id = {part.spec.part_id: part for part in built.parts}
        hardware_by_id = {item.hardware_id: item for item in built.spec.purchased_hardware}
        if (not deck_part_ids or not plate_hardware_ids
                or len(set(deck_part_ids)) != len(deck_part_ids)
                or len(set(plate_hardware_ids)) != len(plate_hardware_ids)
                or not set(deck_part_ids) <= parts_by_id.keys()
                or not set(plate_hardware_ids) <= hardware_by_id.keys()):
            raise PartConstructionError("Korrekt machining needs unique, declared deck and plate IDs")
        deck = tuple(parts_by_id[name] for name in deck_part_ids)
        support = self._support(deck)
        thickness = support.BoundingBox().zlen
        negative = self.cutter.cutout(thickness)
        expected_volume = sum(pi * (diameter / 2)**2 * thickness
                              for _, _, diameter in self.cutter.profile.bores)
        result = built
        for hardware_id in plate_hardware_ids:
            hardware = self.cut_builder.plate(result.spec, hardware_id)
            location = self.locations.build(hardware.local_to_parent)
            footprint = self.cutter.footprint().moved(location)
            footprint_bounds = footprint.BoundingBox()
            if (footprint_bounds.zlen > 1e-6
                    or abs(footprint_bounds.zmin - support.BoundingBox().zmin) > 1e-6
                    or hardware.local_to_parent.axis_basis.local_z_in_parent.z < 0.999999):
                raise PartConstructionError("Korrekt plate must contact the horizontal deck underside")
            clearance = KorrektPlateClearance().check(support, footprint, minimum_edge_margin_mm)
            removed_volume, joints = 0.0, []
            parts_by_id = {part.spec.part_id: part for part in result.parts}
            for part_id in deck_part_ids:
                part = parts_by_id[part_id]
                local_location = self.locations.build(part.spec.local_to_parent).inverse * location
                local_cutter = negative.moved(local_location)
                removed = part.solid.val().intersect(local_cutter).Volume()
                if removed <= 1e-6:
                    continue
                joint_id = f"korrekt_mounting_{hardware_id}_{part_id}"
                joints.append(KorrektMountingJoint(joint_id, part_id, hardware_id,
                                                   clearance, minimum_edge_margin_mm))
                removed_volume += removed
            if abs(removed_volume - expected_volume) > 1e-4:
                raise PartConstructionError(
                    f"{hardware_id}: mounting bores meet missing, overlapping or already machined material")
            result = PanelMachiningFeature().apply(result, joints=tuple(joints), joint_builder=self.cut_builder)
        return result

    def _support(self, parts: tuple[Any, ...]) -> cq.Shape:
        """Union declared panel outlines for outside-edge checks without internal seams."""
        blanks = []
        levels = []
        for part in parts:
            spec = part.spec
            if spec.local_to_parent.axis_basis.local_z_in_parent.z < 0.999999:
                raise PartConstructionError("Korrekt deck panels must have local +Z pointing up")
            width, depth, thickness = spec.local_size_mm
            outline = (tuple((point.x_mm, point.height_mm) for point in spec.outline_mm)
                       if spec.outline_mm else ((0, 0), (width, 0), (width, depth), (0, depth)))
            blank = BlankSheetBuilder(outline, thickness).build().val().moved(
                self.locations.build(spec.local_to_parent))
            blanks.append(blank)
            levels.append((blank.BoundingBox().zmin, blank.BoundingBox().zmax))
        if any(abs(a-b) > 1e-6 for level in levels for a, b in zip(level, levels[0])):
            raise PartConstructionError("Supporting deck panels must share their top and bottom levels")
        return blanks[0].fuse(*blanks[1:]).clean() if len(blanks) > 1 else blanks[0]
