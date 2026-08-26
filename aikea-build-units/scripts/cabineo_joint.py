"""Scope: Derive both participants' cuts from one Cabineo joint definition."""

from __future__ import annotations

from typing import Any

import cadquery as cq

from cabineo_connector_layout import CabineoConnectorLayout
from cabineo_cutter import CabineoCutter
from part_construction_error import PartConstructionError
from part_cut import PartCut


class CabineoJoint:
    """Create source pockets and exact transformed receiver cuts together."""

    def __init__(self) -> None:
        self.cutter = CabineoCutter()
        self.layout = CabineoConnectorLayout()

    def build(
        self,
        joint: Any,
        source_part: Any,
        target_part: Any,
        source_location: cq.Location,
        target_location: cq.Location,
    ) -> tuple[PartCut, ...]:
        self._validate_sheet_thickness(source_part)
        self._validate_sheet_thickness(target_part)
        source_to_target = target_location.inverse * source_location
        edge_position_mm = self.layout.edge_position(joint.source_edge, source_part)
        panel_thickness_mm = self.layout.panel_thickness(
            joint.source_face,
            source_part,
        )
        cuts: list[PartCut] = []
        for index, position_mm in enumerate(
            self.layout.positions(joint, source_part),
            start=1,
        ):
            source_cutter = self.cutter.cutout(
                joint.source_face,
                joint.source_edge,
                position_mm,
                panel_thickness_mm,
                edge_position_mm,
            )
            cuts.extend(
                (
                    PartCut(
                        joint.joint_id,
                        source_part.part_id,
                        index,
                        source_cutter,
                        cq.Location(),
                    ),
                    PartCut(
                        joint.joint_id,
                        target_part.part_id,
                        index,
                        source_cutter,
                        source_to_target,
                    ),
                )
            )
        return tuple(cuts)

    def _validate_sheet_thickness(self, part: Any) -> None:
        thickness_mm = float(part.local_size_mm[2])
        required_mm = self.cutter.profile.minimum_sheet_thickness_mm
        if thickness_mm < required_mm:
            raise PartConstructionError(
                f"{part.part_id} is {thickness_mm:g} mm thick; "
                f"{self.cutter.profile.profile_id} requires at least {required_mm:g} mm"
            )


__all__ = ["CabineoJoint"]
