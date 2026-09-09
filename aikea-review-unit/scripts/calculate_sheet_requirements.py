"""Scope: Convert a saved item inventory into JSON and standalone sheet diagrams."""

import argparse
from hashlib import sha256
import json
from pathlib import Path

from inventory_sheet_requirements import InventorySheetRequirements
from inventory_stock_scenario import InventoryStockScenario
from sheet_layout_values import SheetStock
from sheet_requirements_html import SheetRequirementsHtml


class CalculateSheetRequirementsCommand:
    def run(self, inventory_path: Path, output: Path, stock: SheetStock,
            scenario: InventoryStockScenario | None = None) -> int:
        output.mkdir(parents=True, exist_ok=True)
        json_path = output / "sheet-requirements.json"
        html_path = output / "sheet-requirements.html"
        if inventory_path.resolve() in (json_path.resolve(), html_path.resolve()):
            raise ValueError("report destinations must differ from the source inventory")
        json_path.write_text('{"status":"invalid","reason":"Calculation has not completed for this run."}\n')
        html_path.write_text("<!doctype html><meta charset='utf-8'><p>Sheet calculation has not completed for this run.</p>")
        raw = inventory_path.read_bytes()
        inventory = json.loads(raw)
        planner = InventorySheetRequirements(stock)
        report = planner.calculate(inventory)
        if scenario is not None:
            proposed, metadata = scenario.apply(inventory)
            report = planner.calculate(proposed)
            report["stock_scenario"] = metadata
            report["assumptions"].append(
                "Stock scenario only: original panel outlines are retained; construction has not been regenerated or fit-checked.")
            report["assumptions"].append(
                f"{len(metadata['non_sheet_parts'])} explicitly identified non-sheet items remain in the source inventory and need separate stock.")
        report["source"] = dict(path=str(inventory_path.resolve()), sha256=sha256(raw).hexdigest())
        report["inventory_scope"] = inventory.get("scope", "Scope not supplied by source inventory.")
        report["assumptions"].append(report["inventory_scope"])
        json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        html_path.write_text(SheetRequirementsHtml().render(report), encoding="utf-8")
        summary = dict(status=report["status"], sheet_count=report["sheet_count"],
                       groups=[{key: group[key] for key in ("material_id", "thickness_mm", "sheet_count", "part_count")}
                               for group in report["groups"]], oversized=report["oversized_part_paths"],
                       html=str(html_path), json=str(json_path))
        print(json.dumps(summary, indent=2))
        return 2 if report["oversized_part_paths"] else 0


# This function only adapts CLI arguments to the command and numeric stock objects.
def main() -> int:
    parser = argparse.ArgumentParser(description="Estimate 1220 × 2440 mm sheet requirements from an AIkea inventory.")
    parser.add_argument("inventory", type=Path)
    parser.add_argument("--output-directory", type=Path)
    parser.add_argument("--width", type=float, default=1220.0)
    parser.add_argument("--height", type=float, default=2440.0)
    parser.add_argument("--edge-margin", type=float, default=10.0)
    parser.add_argument("--part-gap", type=float, default=8.0)
    parser.add_argument("--allow-rotation", action="store_true")
    parser.add_argument("--scenario-thickness", type=float)
    parser.add_argument("--scenario-material")
    parser.add_argument("--non-sheet-part", action="append", default=[])
    args = parser.parse_args()
    stock = SheetStock(args.width, args.height, args.edge_margin, args.part_gap, args.allow_rotation)
    scenario = (InventoryStockScenario(args.scenario_thickness, args.scenario_material, args.non_sheet_part)
                if args.scenario_thickness is not None or args.scenario_material is not None or args.non_sheet_part
                else None)
    return CalculateSheetRequirementsCommand().run(
        args.inventory, args.output_directory or args.inventory.parent, stock, scenario)


if __name__ == "__main__":
    raise SystemExit(main())
