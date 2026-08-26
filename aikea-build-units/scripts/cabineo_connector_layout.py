"""Scope: Resolve Cabineo connector positions along one source-panel edge."""

from __future__ import annotations

from typing import Any

from part_construction_error import PartConstructionError


class CabineoConnectorLayout:
    """Turn a named connector layout into offsets in the source local frame."""

    _AXIS_INDEX = {"X": 0, "Y": 1, "Z": 2}

    def positions(self, joint: Any, source_part: Any) -> tuple[float, ...]:
        if joint.connector_layout != "two_quarter_points":
            raise PartConstructionError(
                f"unsupported Cabineo connector layout: {joint.connector_layout}"
            )
        slide_axis = self.slide_axis(joint.source_face, joint.source_edge)
        length_mm = float(source_part.local_size_mm[self._AXIS_INDEX[slide_axis]])
        return length_mm / 4.0, length_mm * 3.0 / 4.0

    def edge_position(self, edge: str, source_part: Any) -> float:
        axis = edge[-1]
        return (
            float(source_part.local_size_mm[self._AXIS_INDEX[axis]])
            if edge.startswith(">")
            else 0.0
        )

    def panel_thickness(self, face: str, source_part: Any) -> float:
        return float(source_part.local_size_mm[self._AXIS_INDEX[face[-1]]])

    def slide_axis(self, face: str, edge: str) -> str:
        return ({"X", "Y", "Z"} - {face[-1], edge[-1]}).pop()


__all__ = ["CabineoConnectorLayout"]
