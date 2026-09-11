"""Scope: Build panel blanks from explicit manufacturing geometry, independent of roles."""

from math import isfinite

from blank_sheet_builder import BlankSheetBuilder
from part_construction_error import PartConstructionError


class PanelBlankBuilder:
    """Use the same explicit dimensions for standard and authored panel blanks."""

    def build(self, part):
        size = part.local_size_mm
        if len(size) != 3 or any(not isfinite(value) or value <= 0 for value in size):
            raise PartConstructionError(f"{part.part_id}: positive finite local size required")
        if part.outline_mm:
            outline = tuple((point.x_mm, point.height_mm) for point in part.outline_mm)
            if any(not isfinite(value) for point in outline for value in point):
                raise PartConstructionError(f"{part.part_id}: finite outline required")
            return BlankSheetBuilder(outline, size[2]).build()
        return BlankSheetBuilder.rectangle(*size).build()
