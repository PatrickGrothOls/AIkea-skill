"""Scope: Place numeric rectangles using the Vilja bottom-left packing approach."""

from sheet_layout_values import SheetPart, SheetPlacement, SheetStock
from sheet_layout_validator import SheetLayoutValidator


class RectangularSheetPlanner:
    """Produce a feasible deterministic layout, without claiming an optimal count."""

    def __init__(self, stock: SheetStock):
        self.stock = stock

    def plan(self, parts: tuple[SheetPart, ...]):
        # Compare both orientation preferences: a wide-first shelf can waste an entire column.
        candidates = [self._pack(parts, narrow_first) for narrow_first in (False, True)]
        sheets, oversized = min(candidates, key=lambda result: (len(result[1]), len(result[0])))
        SheetLayoutValidator(self.stock).validate(parts, sheets, oversized)
        return sheets, oversized

    def _pack(self, parts, narrow_first):
        sheets, oversized = [], []
        ordered = sorted(parts, key=lambda part: (
            -max(part.width_mm, part.height_mm),
            -part.width_mm * part.height_mm, part.path,
        ))
        for part in ordered:
            for sheet in sheets:
                placement = self._find(part, sheet, narrow_first)
                if placement:
                    sheet.append(placement)
                    break
            else:
                placement = self._find(part, [], narrow_first)
                if placement:
                    sheets.append([placement])
                else:
                    oversized.append(part)
        return sheets, oversized

    def _find(self, part, existing, narrow_first):
        margin, gap = self.stock.edge_margin_mm, self.stock.part_gap_mm
        xs = sorted({margin, *(item.right_mm + gap for item in existing)})
        ys = sorted({margin, *(item.top_mm + gap for item in existing)})
        orientations = [(False, part.width_mm, part.height_mm)]
        if self.stock.allow_rotation and part.width_mm != part.height_mm:
            orientations.append((True, part.height_mm, part.width_mm))
        candidates = []
        for rotated, width, height in orientations:
            for y in ys:
                for x in xs:
                    item = SheetPlacement(part, x, y, width, height, rotated)
                    fits = (item.right_mm <= self.stock.width_mm - margin + 1e-6
                            and item.top_mm <= self.stock.height_mm - margin + 1e-6)
                    if fits and all(item.clears(other, gap) for other in existing):
                        candidates.append(item)
        return min(candidates, key=lambda item: (
            item.y_mm, item.x_mm,
            item.width_mm if narrow_first else item.height_mm,
            item.top_mm, item.right_mm, item.rotated,
        ), default=None)
