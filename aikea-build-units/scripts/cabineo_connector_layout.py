"""Scope: Resolve Cabineo connector positions along one source-panel edge."""

from __future__ import annotations

from math import ceil, isfinite
from typing import Any

from part_construction_error import PartConstructionError


class CabineoConnectorLayout:
    """Turn a named connector layout into offsets in the source local frame."""

    _AXIS_INDEX = {"X": 0, "Y": 1, "Z": 2}
    _SUPPORTED_LAYOUTS = {"bounded_spacing", "two_quarter_points", "explicit"}
    _MAX_SPACING_MM = 300.0
    _MAX_EDGE_DISTANCE_MM = 200.0
    _MIN_CONNECTOR_COUNT = 2

    def positions(self, joint: Any, source_part: Any) -> tuple[float, ...]:
        if joint.connector_layout not in self._SUPPORTED_LAYOUTS:
            raise PartConstructionError(
                f"unsupported Cabineo connector layout: {joint.connector_layout}"
            )
        length_mm = self.slide_length(
            joint.source_face,
            joint.source_edge,
            source_part,
        )
        if joint.connector_layout == "explicit":
            return self._explicit(joint.connector_positions_mm, length_mm)
        edge_distance_mm = min(self._MAX_EDGE_DISTANCE_MM, length_mm / 4.0)
        connector_span_mm = length_mm - (2.0 * edge_distance_mm)
        connector_count = max(
            self._MIN_CONNECTOR_COUNT,
            ceil(connector_span_mm / self._MAX_SPACING_MM) + 1,
        )
        spacing_mm = connector_span_mm / (connector_count - 1)
        return tuple(
            edge_distance_mm + (index * spacing_mm)
            for index in range(connector_count)
        )

    def _explicit(self, positions: tuple[float, ...], length: float) -> tuple[float, ...]:
        if len(positions) < self._MIN_CONNECTOR_COUNT or not all(isfinite(p) for p in positions):
            raise PartConstructionError("explicit Cabineo layout needs at least two finite positions")
        gaps = tuple(right - left for left, right in zip(positions, positions[1:]))
        checks = (
            (not 0 < positions[0] < positions[-1] < length, "positions must lie inside the edge"),
            (any(gap <= 0 for gap in gaps), "positions must be strictly increasing"),
            (max(gaps) > self._MAX_SPACING_MM, "connector spacing exceeds 300 mm"),
            (max(positions[0], length - positions[-1]) > self._MAX_EDGE_DISTANCE_MM,
             "connector end distance exceeds 200 mm"),
        )
        for invalid, reason in checks:
            if invalid:
                raise PartConstructionError(f"explicit Cabineo layout: {reason}")
        return positions

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

    def slide_length(self, face: str, edge: str, source_part: Any) -> float:
        slide_axis = self.slide_axis(face, edge)
        return float(source_part.local_size_mm[self._AXIS_INDEX[slide_axis]])


__all__ = ["CabineoConnectorLayout"]
