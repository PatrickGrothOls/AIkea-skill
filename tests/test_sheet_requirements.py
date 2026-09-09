"""Scope: Verify sheet grouping, physical fit, accounting and report provenance."""

from dataclasses import replace
from hashlib import sha256
import json

import pytest

from calculate_sheet_requirements import CalculateSheetRequirementsCommand
from inventory_sheet_requirements import InventorySheetRequirements
from rectangular_sheet_planner import RectangularSheetPlanner
from sheet_layout_validator import SheetLayoutValidator
from sheet_layout_values import SheetPart, SheetPlacement, SheetStock


class TestSheetRequirements:
    def inventory(self, *rows):
        return dict(schema_version=1, status="draft", manufactured_parts=list(rows), unresolved=[])

    def part(self, path, width, height, thickness=18, material="plywood"):
        return dict(path=path, local_size_mm=[width, height, thickness], material_id=material, quantity=1)

    def test_equal_rectangles_need_four_incompatible_stock_groups(self):
        report = InventorySheetRequirements(SheetStock()).calculate(self.inventory(
            self.part("cabinet_01/side", 500, 500),
            self.part("cabinet_02/side", 500, 500),
            self.part("back", 500, 500, thickness=9),
            self.part("door", 500, 500, material="mdf"),
            self.part("unknown", 500, 500, material=""),
        ))
        assert report["sheet_count"] == 4
        assert report["part_count"] == 5
        assert report["oversized_part_paths"] == []
        assert any("Unknown materials" in note for note in report["assumptions"])

    def test_rotation_is_explicit_and_oversize_never_disappears(self):
        data = self.inventory(self.part("long-panel", 2000, 500))
        locked = InventorySheetRequirements(SheetStock()).calculate(data)
        turned = InventorySheetRequirements(SheetStock(allow_rotation=True)).calculate(data)
        assert locked["status"] == "incomplete"
        assert locked["oversized_part_paths"] == ["long-panel"]
        assert turned["sheet_count"] == 1
        assert turned["groups"][0]["sheets"][0]["placements"][0]["rotated"]

    def test_gaps_and_margins_determine_sheet_count(self):
        data = self.inventory(self.part("a", 600, 2420), self.part("b", 600, 2420))
        assert InventorySheetRequirements(SheetStock()).calculate(data)["sheet_count"] == 2
        assert InventorySheetRequirements(SheetStock(part_gap_mm=0)).calculate(data)["sheet_count"] == 1

    def test_shelves_rotate_to_use_both_sheet_columns(self):
        parts = tuple(SheetPart(f"shelf-{i}", 707, 564) for i in range(6))
        sheets, omitted = RectangularSheetPlanner(SheetStock(allow_rotation=True)).plan(parts)
        assert len(sheets) == 1
        assert len(sheets[0]) == 6
        assert omitted == []

    @pytest.mark.parametrize("dimensions", [(0, 50, 18), (50, -1, 18), (50, 50, float("nan"))])
    def test_invalid_dimensions_do_not_become_a_sheet_estimate(self, dimensions):
        with pytest.raises(ValueError, match="invalid physical panel"):
            InventorySheetRequirements(SheetStock()).calculate(self.inventory(self.part("bad", *dimensions)))

    def test_duplicate_physical_paths_fail(self):
        row = self.part("same", 500, 500)
        with pytest.raises(ValueError, match="uniquely identified"):
            InventorySheetRequirements(SheetStock()).calculate(self.inventory(row, row))

    def test_order_does_not_change_layout_and_every_part_appears_once(self):
        parts = (SheetPart("a", 700, 1300), SheetPart("b", 400, 600), SheetPart("c", 600, 900))
        planner = RectangularSheetPlanner(SheetStock(allow_rotation=True))
        first, omitted = planner.plan(parts)
        assert (first, omitted) == planner.plan(tuple(reversed(parts)))
        assert sorted(item.part.path for sheet in first for item in sheet) == ["a", "b", "c"]

    @pytest.mark.parametrize("damage", ["overlap", "outside", "changed_size", "missing"])
    def test_validator_rejects_corrupt_layout(self, damage):
        parts = (SheetPart("a", 500, 500), SheetPart("b", 500, 500))
        first = SheetPlacement(parts[0], 10, 10, 500, 500, False)
        second = SheetPlacement(parts[1], 518, 10, 500, 500, False)
        variants = {
            "overlap": [[first, replace(second, x_mm=510)]],
            "outside": [[first, replace(second, x_mm=900)]],
            "changed_size": [[first, replace(second, width_mm=100)]],
            "missing": [[first]],
        }
        with pytest.raises(ValueError):
            SheetLayoutValidator(SheetStock()).validate(parts, variants[damage], [])

    def test_exports_source_hash_and_escapes_part_labels(self, tmp_path):
        source = tmp_path / "item-counts.json"
        source.write_text(json.dumps(self.inventory(self.part("<script>bad()</script>", 600, 1000))))
        output = tmp_path / "result"
        assert CalculateSheetRequirementsCommand().run(source, output, SheetStock()) == 0
        report = json.loads((output / "sheet-requirements.json").read_text())
        assert report["source"]["sha256"] == sha256(source.read_bytes()).hexdigest()
        html = (output / "sheet-requirements.html").read_text()
        assert "<script>" not in html
        assert "&lt;script&gt;" in html
        assert "Estimated sheets: 1" in html

    def test_invalid_inventory_revokes_previous_diagrams(self, tmp_path):
        source = tmp_path / "item-counts.json"
        source.write_text('{"status":"invalid"}')
        (tmp_path / "sheet-requirements.html").write_text("old estimate")
        with pytest.raises(ValueError):
            CalculateSheetRequirementsCommand().run(source, tmp_path, SheetStock())
        assert json.loads((tmp_path / "sheet-requirements.json").read_text())["status"] == "invalid"
        assert "old estimate" not in (tmp_path / "sheet-requirements.html").read_text()
