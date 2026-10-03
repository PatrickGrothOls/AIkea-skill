"""Scope: Retain the pre-migration panel engine only as an independent compatibility test oracle."""

from __future__ import annotations

from typing import Any

from blank_sheet_builder import BlankSheetBuilder
from part_construction_error import PartConstructionError


class LegacyPartBlankBuilder:
    """Turn one generated part specification into its canonical local solid."""

    def __init__(self) -> None:
        self._role_builders = {
            "side_panel": self._build_side_panel,
            "back_panel": self._build_back_panel,
            "door_panel": self._build_door_panel,
            "top_panel": self._build_top_panel,
            "shelf_panel": self._build_local_rectangle,
            "base_deck": self._build_local_rectangle,
            "base_rail": self._build_local_rectangle,
            "base_brace": self._build_local_rectangle,
        }

    def build(self, part: Any) -> Any:
        builder = self._role_builders.get(part.role)
        if builder is None:
            raise PartConstructionError(f"unsupported part role: {part.role}")
        return builder(part)

    def _build_side_panel(self, part: Any) -> Any:
        dimensions = self._dimensions(part)
        return BlankSheetBuilder.rectangle(
            dimensions["depth"],
            dimensions["height"],
            dimensions["thickness"],
        ).build()

    def _build_back_panel(self, part: Any) -> Any:
        dimensions = self._dimensions(part)
        return BlankSheetBuilder(
            self._outline(part),
            dimensions["thickness"],
        ).build()

    def _build_door_panel(self, part: Any) -> Any:
        dimensions = self._dimensions(part)
        outline = self._outline(part) or (
            (0.0, 0.0),
            (dimensions["width"], 0.0),
            (dimensions["width"], dimensions["right_height"]),
            (0.0, dimensions["left_height"]),
        )
        return BlankSheetBuilder(outline, dimensions["thickness"]).build()

    def _build_top_panel(self, part: Any) -> Any:
        dimensions = self._dimensions(part)
        return BlankSheetBuilder.rectangle(
            dimensions["length"],
            dimensions["depth"],
            dimensions["thickness"],
        ).build()

    def _build_local_rectangle(self, part: Any) -> Any:
        return BlankSheetBuilder.rectangle(*part.local_size_mm).build()

    def _dimensions(self, part: Any) -> dict[str, float]:
        return {name: float(value) for name, value in part.dimensions_mm}

    def _outline(self, part: Any) -> tuple[tuple[float, float], ...]:
        return tuple(
            (float(point.x_mm), float(point.height_mm))
            for point in part.outline_mm
        )


from system_32_side_panel_grid import System32SidePanelGrid


class LegacySheetPartBuilder:
    """Continue from the calculated blank through deterministic subtraction."""

    def __init__(self) -> None:
        self.blank_builder = LegacyPartBlankBuilder()
        self._local_machining = {
            "side_panel": System32SidePanelGrid().apply,
        }

    def build(self, part: Any, cuts: tuple[Any, ...]) -> Any:
        workpiece = self.blank_builder.build(part)
        machining = self._local_machining.get(part.role)
        if machining is not None:
            workpiece = machining(part, workpiece)
        for cut in cuts:
            workpiece = workpiece.cut(cut.cutter.located(cut.location))
        return workpiece
