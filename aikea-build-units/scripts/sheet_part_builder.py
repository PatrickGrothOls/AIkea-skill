"""Scope: Construct one generated sheet part and apply its resolved local cuts."""

from __future__ import annotations

from typing import Any

from part_blank_builder import PartBlankBuilder


class SheetPartBuilder:
    """Continue from the calculated blank through deterministic subtraction."""

    def __init__(self) -> None:
        self.blank_builder = PartBlankBuilder()

    def build(self, part: Any, cuts: tuple[Any, ...]) -> Any:
        workpiece = self.blank_builder.build(part)
        for cut in cuts:
            workpiece = workpiece.cut(cut.cutter.located(cut.location))
        return workpiece


__all__ = ["SheetPartBuilder"]
