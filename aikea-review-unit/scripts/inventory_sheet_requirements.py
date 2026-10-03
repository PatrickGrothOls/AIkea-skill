"""Scope: Group inventory rectangles by stock compatibility and report sheet counts."""

from collections import defaultdict
from dataclasses import asdict
from math import ceil, isfinite

from rectangular_sheet_planner import RectangularSheetPlanner
from sheet_layout_values import SheetPart, SheetStock


class InventorySheetRequirements:
    def __init__(self, stock: SheetStock):
        self.stock = stock

    def calculate(self, inventory: dict) -> dict:
        if inventory.get("schema_version") != 1 or inventory.get("status") != "draft":
            raise ValueError("expected a valid version-1 draft item inventory")
        parts = inventory["manufactured_parts"]
        self._validate_parts(parts)
        grouped = defaultdict(list)
        for row in parts:
            width, height, thickness = row["local_size_mm"]
            grouped[(row["material_id"], thickness)].append(SheetPart(row["path"], width, height))
        groups = [self._group(material, thickness, tuple(items))
                  for (material, thickness), items in sorted(grouped.items())]
        oversized = [path for group in groups for path in group["oversized_part_paths"]]
        provisional = any(not group["material_id"] for group in groups)
        return dict(
            schema_version=1, status="incomplete" if oversized else "provisional",
            stock=asdict(self.stock), part_count=len(parts),
            sheet_count=sum(group["sheet_count"] for group in groups),
            groups=groups, oversized_part_paths=oversized,
            assumptions=[
                "Rectangular finished-part envelopes; feasible heuristic layout, not a proven minimum.",
                "No machining stock allowance beyond the stated sheet margin and part gap.",
                "Material and grain compatibility must be confirmed before purchasing.",
            ] + (["Unknown materials assumed identical within each thickness for this estimate."] if provisional else []),
            inventory_unresolved=inventory.get("unresolved", []),
        )

    def _validate_parts(self, parts):
        paths = [row["path"] for row in parts]
        if not parts or len(paths) != len(set(paths)):
            raise ValueError("inventory must contain uniquely identified panel instances")
        for row in parts:
            sizes = row["local_size_mm"]
            checks = (
                isinstance(row["path"], str) and bool(row["path"]),
                isinstance(row["material_id"], str),
                row["quantity"] == 1,
                len(sizes) == 3 and all(isfinite(size) and size > 0 for size in sizes),
            )
            if not all(checks):
                raise ValueError(f"invalid physical panel record: {row['path']}")

    def _group(self, material, thickness, parts):
        sheets, oversized = RectangularSheetPlanner(self.stock).plan(parts)
        area = sum(part.width_mm * part.height_mm for part in parts)
        stock_area = self.stock.width_mm * self.stock.height_mm
        usable_area = ((self.stock.width_mm - 2 * self.stock.edge_margin_mm)
                       * (self.stock.height_mm - 2 * self.stock.edge_margin_mm))
        return dict(
            material_id=material, thickness_mm=thickness, part_count=len(parts),
            sheet_count=len(sheets), rectangle_area_m2=area / 1e6,
            area_lower_bound=ceil(area / usable_area),
            oversized_part_paths=[part.path for part in oversized],
            sheets=[dict(
                index=index, placements=[asdict(item) for item in sheet],
                rectangle_utilization=sum(item.width_mm * item.height_mm for item in sheet) / stock_area,
            ) for index, sheet in enumerate(sheets, start=1)],
        )
