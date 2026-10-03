"""Scope: Make explicit stock-only estimates without changing source geometry."""

from copy import deepcopy
from math import isfinite


class InventoryStockScenario:
    """Retain non-sheet items and distinguish proposed stock from built dimensions."""

    def __init__(self, thickness_mm=None, material_id=None, non_sheet_paths=()):
        if thickness_mm is not None and (not isfinite(thickness_mm) or thickness_mm <= 0):
            raise ValueError("scenario thickness must be positive and finite")
        if material_id is not None and not material_id.strip():
            raise ValueError("scenario material must have an identity")
        self.thickness = thickness_mm
        self.material = material_id
        self.non_sheet_paths = tuple(non_sheet_paths)

    def apply(self, inventory):
        rows = inventory["manufactured_parts"]
        paths = {row["path"] for row in rows}
        if (len(set(self.non_sheet_paths)) != len(self.non_sheet_paths)
                or not set(self.non_sheet_paths) <= paths):
            raise ValueError("non-sheet selections must be unique existing part paths")
        result = deepcopy(inventory)
        result["manufactured_parts"] = []
        excluded = []
        for row in rows:
            if row["path"] in self.non_sheet_paths:
                excluded.append(deepcopy(row))
                continue
            panel = deepcopy(row)
            if self.thickness is not None:
                panel["local_size_mm"][2] = self.thickness
            if self.material is not None:
                panel["material_id"] = self.material
            result["manufactured_parts"].append(panel)
        metadata = dict(thickness_mm=self.thickness, material_id=self.material,
                        geometry_regenerated=False, non_sheet_parts=excluded)
        return result, metadata
