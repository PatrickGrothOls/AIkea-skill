"""Scope: Verify every supplied panel is accounted for with valid sheet placement."""

from collections import Counter
from math import isfinite

from sheet_layout_values import SheetStock


class SheetLayoutValidator:
    def __init__(self, stock: SheetStock):
        self.stock = stock

    def validate(self, parts, sheets, oversized):
        expected = Counter(part.path for part in parts)
        accounted = Counter(item.part.path for sheet in sheets for item in sheet)
        accounted.update(part.path for part in oversized)
        if any(count != 1 for count in expected.values()) or expected != accounted:
            raise ValueError("layout must account for every unique physical part exactly once")
        by_path = {part.path: part for part in parts}
        for sheet in sheets:
            for index, placement in enumerate(sheet):
                self._placement(placement, by_path[placement.part.path])
                if not all(placement.clears(other, self.stock.part_gap_mm) for other in sheet[index + 1:]):
                    raise ValueError(f"overlap or insufficient spacing: {placement.part.path}")

    def _placement(self, item, part):
        dimensions = (part.height_mm, part.width_mm) if item.rotated else (part.width_mm, part.height_mm)
        if dimensions != (item.width_mm, item.height_mm):
            raise ValueError(f"placement changed panel dimensions: {part.path}")
        if item.rotated and not self.stock.allow_rotation:
            raise ValueError(f"rotation is forbidden: {part.path}")
        checks = (
            all(isfinite(value) for value in (item.x_mm, item.y_mm, item.width_mm, item.height_mm)),
            min(item.width_mm, item.height_mm) > 0,
            min(item.x_mm, item.y_mm) >= self.stock.edge_margin_mm - 1e-6,
            item.right_mm <= self.stock.width_mm - self.stock.edge_margin_mm + 1e-6,
            item.top_mm <= self.stock.height_mm - self.stock.edge_margin_mm + 1e-6,
        )
        if not all(checks):
            raise ValueError(f"placement exceeds usable sheet bounds: {part.path}")
