"""Scope: Produce one proven Cabineo cutter in a requested local position."""

from __future__ import annotations

import cadquery as cq

from cabineo_cutter_geometry import CabineoCutterGeometry
from cabineo_cutter_placement import CabineoCutterPlacement
from cabineo_profile import CabineoProfile, NON_BOTTOM_CABINEO


class CabineoCutter:
    """Combine fixed cutter geometry with face-and-edge placement."""

    def __init__(
        self,
        profile: CabineoProfile = NON_BOTTOM_CABINEO,
        geometry: CabineoCutterGeometry | None = None,
    ) -> None:
        self.profile = profile
        self.geometry = geometry or CabineoCutterGeometry()
        self.placement = CabineoCutterPlacement()

    def cutout(
        self,
        face: str,
        edge: str,
        primary_offset_mm: float,
        panel_thickness_mm: float,
        edge_position_mm: float,
    ) -> cq.Shape:
        shape = self.geometry.build(self.profile)
        oriented = self.placement.orient(shape, face, edge)
        return self.placement.translate(
            oriented,
            face,
            edge,
            primary_offset_mm,
            panel_thickness_mm,
            edge_position_mm,
        )


__all__ = ["CabineoCutter"]
