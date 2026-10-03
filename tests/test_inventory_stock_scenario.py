"""Scope: Verify stock scenarios preserve originals and cannot hide broken inputs."""

from copy import deepcopy
from hashlib import sha256
import json

import pytest

from calculate_sheet_requirements import CalculateSheetRequirementsCommand
from inventory_stock_scenario import InventoryStockScenario
from sheet_layout_values import SheetStock


class TestInventoryStockScenario:
    def inventory(self):
        return dict(schema_version=1, status="draft", unresolved=[dict(code="hardware.missing")],
                    manufactured_parts=[
                        dict(path="back", local_size_mm=[1268, 1550, 6.5], material_id="", quantity=1),
                        dict(path="shelf", local_size_mm=[600, 400, 18], material_id="", quantity=1),
                        dict(path="rod", local_size_mm=[25, 590, 25], material_id="", quantity=1),
                    ])

    def test_scenario_preserves_original_dimensions_and_non_sheet_evidence(self):
        data = self.inventory()
        before = deepcopy(data)
        result, metadata = InventoryStockScenario(16, "MDF", ("rod",)).apply(data)
        assert data == before
        assert [row["local_size_mm"] for row in result["manufactured_parts"]] == [
            [1268, 1550, 16], [600, 400, 16]]
        assert metadata["non_sheet_parts"] == [before["manufactured_parts"][2]]
        assert metadata["geometry_regenerated"] is False
        assert result["unresolved"] == before["unresolved"]

    def test_oversized_back_and_missing_hardware_remain_visible(self, tmp_path):
        source = tmp_path / "inventory.json"
        source.write_text(json.dumps(self.inventory()))
        digest = sha256(source.read_bytes()).hexdigest()
        scenario = InventoryStockScenario(16, "MDF", ("rod",))
        assert CalculateSheetRequirementsCommand().run(source, tmp_path, SheetStock(allow_rotation=True), scenario) == 2
        report = json.loads((tmp_path / "sheet-requirements.json").read_text())
        assert report["oversized_part_paths"] == ["back"]
        assert report["inventory_unresolved"] == [dict(code="hardware.missing")]
        assert report["source"]["sha256"] == digest == sha256(source.read_bytes()).hexdigest()
        assert "construction has not been regenerated" in (tmp_path / "sheet-requirements.html").read_text()

    @pytest.mark.parametrize("paths", [("unknown",), ("rod", "rod")])
    def test_non_sheet_selections_cannot_silently_miss_or_repeat(self, paths):
        with pytest.raises(ValueError, match="unique existing"):
            InventoryStockScenario(non_sheet_paths=paths).apply(self.inventory())

    @pytest.mark.parametrize("thickness", [0, -1, float("nan"), float("inf")])
    def test_invalid_proposed_thickness_fails(self, thickness):
        with pytest.raises(ValueError, match="positive and finite"):
            InventoryStockScenario(thickness)

    def test_filter_cannot_conceal_duplicate_source_parts(self, tmp_path):
        data = self.inventory()
        data["manufactured_parts"].append(data["manufactured_parts"][-1])
        source = tmp_path / "inventory.json"
        source.write_text(json.dumps(data))
        with pytest.raises(ValueError, match="uniquely identified"):
            CalculateSheetRequirementsCommand().run(
                source, tmp_path, SheetStock(), InventoryStockScenario(non_sheet_paths=("rod",)))
        assert json.loads((tmp_path / "sheet-requirements.json").read_text())["status"] == "invalid"
