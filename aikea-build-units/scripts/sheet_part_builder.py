"""Scope: Construct one generated sheet part and apply its local machining."""

from __future__ import annotations

from typing import Any

from part_blank_builder import PartBlankBuilder
from system_32_side_panel_grid import System32SidePanelGrid


class SheetPartBuilder:
    """Continue from the calculated blank through deterministic subtraction."""

    def __init__(self) -> None:
        self.blank_builder = PartBlankBuilder()
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


__all__ = ["SheetPartBuilder"]
