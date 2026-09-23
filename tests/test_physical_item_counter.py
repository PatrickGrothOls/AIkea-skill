"""Scope: Verify counting against generated mixed-rail furniture and damaged cuts."""

from dataclasses import replace
import json
from pathlib import Path

import pytest
import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator
from cabinet_drawer_plan import DrawerLayout
from count_physical_items import CountPhysicalItemsCommand
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from hettich_ka_4532_spacer_cabinet_drawer_generator import HettichKa4532SpacerCabinetDrawerGenerator
from hettich_ka_4532_spacer_mounting_test_support import HettichKa4532StepSetLoaderProbe
from hettich_ka_5332_cabinet_drawer_generator import HettichKa5332CabinetDrawerGenerator
from hettich_ka_5332_test_support import HettichKa5332StepAssemblyLoaderTestDouble
from physical_item_counter import PhysicalItemCounter


class TestPhysicalItemCounter:
    """Exercise actual generated ownership without claiming vendor CAD fidelity."""

    @pytest.fixture(scope="class")
    def counted_project(self, tmp_path_factory):
        root = tmp_path_factory.mktemp("item-counter")
        fixture = Path(__file__).parent / "fixtures/four-unit-review-aikea.yaml"
        project = yaml.safe_load(fixture.read_text(encoding="utf-8"))
        AssemblyTaxonomyGenerator().generate(project, root)
        self._use_legacy_contract(root)
        HettichKa5332CabinetDrawerGenerator(HettichKa5332StepAssemblyLoaderTestDouble()).generate(
            root, "tall_storage_01", DrawerLayout("drawer_01", bottom_height_mm=356.0),
            hardware_directory=root / "hardware",
        )
        HettichKa4532SpacerCabinetDrawerGenerator(HettichKa4532StepSetLoaderProbe()).generate(
            root, "tall_storage_02", DrawerLayout("drawer_01", 356.0, box_height_mm=150.0, box_depth_mm=500.0),
            hardware_directory=root / "hardware", cabinet_front_mm=0.0, drawer_front_mm=18.0,
        )
        loader = GeneratedAssemblyBuilderLoader()
        return root, loader.walk(root, loader.load_assembly(root, "wardrobe_01"))

    def _use_legacy_contract(self, root):
        # A released project owns its older contract; new features must work without regenerating it.
        composition = root / "assemblies/assembly_composition.py"
        legacy = (
            "@dataclass(frozen=True)\nclass PurchasedHardwareSpec:\n"
            "    hardware_id: str\n    manufacturer: str\n    product_code: str\n"
            "    hardware_asset_id: str\n    local_to_parent: Any | None\n"
            "    geometry_selector: str | None = None\n"
        )
        import_line = "from purchased_hardware_spec import ConnectionPurchaseSpec, HardwarePurchaseSpec, PurchasedHardwareSpec"
        assert import_line in composition.read_text()
        composition.write_text(composition.read_text().replace(import_line, legacy))
        specification = root / "assemblies/specification.py"
        specification.write_text(specification.read_text().replace("    HardwarePurchaseSpec,\n", "")
                                 .replace("    ConnectionPurchaseSpec,\n", ""))
        assert "class PurchasedHardwareSpec:" in composition.read_text()

    def test_counts_panels_connectors_and_exact_purchase_sets(self, counted_project):
        _, visits = counted_project
        report = PhysicalItemCounter().count(visits)
        assert report["totals"] == dict(manufactured_parts=47, hardware_components=88,
                                         verified_cabineos=79, brass_inserts=79)
        purchased = {row["product_code"]: row for row in report["purchased_summary"]}
        assert {sku: purchased[sku]["quantity"] for sku in ("9057405", "9114276", "13952", "267.91.314")} == {
            "9057405": 1, "9114276": 1, "13952": 2, "267.91.314": 79,
        }
        assert purchased["267.91.314"]["supplier_pack_quantity"] == 100
        assert all(row["mounting_fasteners_included"] == (row["product_code"] != "61854")
                   for row in report["purchased_units"])
        assert {sku: purchased[sku]["quantity"] for sku in ("46642", "61854", "70151")} == {
            "46642": 48, "61854": 16, "70151": 16,
        }
        pair = next(row for row in report["purchased_units"] if row["product_code"] == "9114276")
        assert len(pair["component_paths"]) == 4
        assert sum("/drawer_01/" in path for path in pair["component_paths"]) == 2
        paths = [row["path"] for row in report["manufactured_parts"]]
        assert len(paths) == len(set(paths)) == 47
        assert any("tall_storage_01/drawer_01/" in path for path in paths)
        assert any("tall_storage_02/drawer_01/" in path for path in paths)
        codes = [row["code"] for row in report["unresolved"]]
        missing = {row["path"] for row in report["unresolved"]
                   if row["code"] == "part.material_missing"}
        assert missing == {path for path in paths if "/drawer_01/" in path}
        assert len(missing) == 10  # Legacy drawer geometry has no selected stock.
        assert sum(bool(row["material_id"]) for row in report["manufactured_parts"]) == 37
        assert codes.count("joint.unresolved") == 7
        assert "shelf.support_product_undefined" in codes
        assert report["status"] == "draft"

    @pytest.mark.parametrize("damage", ["missing", "duplicate", "wrong_index", "wrong_part"])
    def test_rejects_bad_pair_evidence(self, counted_project, damage):
        _, original = counted_project
        visits = list(original)
        position = next(index for index, visit in enumerate(visits)
                        if hasattr(visit, "assembly") and any(
                            joint.joint_type == "cabineo" for joint in visit.assembly.joints))
        visit = visits[position]
        cuts = list(visit.assembly.cuts)
        connector_joints = {joint.joint_id for joint in visit.assembly.joints if joint.joint_type == "cabineo"}
        cut_index = next(index for index, cut in enumerate(cuts) if cut.joint_id in connector_joints)
        cut = cuts[cut_index]
        if damage == "missing":
            cuts.pop(cut_index)
        elif damage == "duplicate":
            cuts.append(cut)
        else:
            field = {"wrong_index": dict(connector_index=999), "wrong_part": dict(part_id="unknown")}[damage]
            cuts[cut_index] = replace(cut, **field)
        visits[position] = replace(visit, assembly=replace(visit.assembly, cuts=tuple(cuts)))
        report = PhysicalItemCounter().count(visits)
        assert report["totals"]["verified_cabineos"] < 79
        assert report["totals"]["verified_cabineos"] == report["totals"]["brass_inserts"]
        assert any(row["code"] == "cabineo.cut_mismatch" for row in report["unresolved"])

    def test_rejects_duplicate_physical_paths(self, counted_project):
        _, visits = counted_project
        with pytest.raises(ValueError, match="duplicate instance paths"):
            PhysicalItemCounter().count((*visits, visits[-1]))

    def test_generated_inventory_nests_on_standard_sheets(self, counted_project):
        from inventory_sheet_requirements import InventorySheetRequirements
        from sheet_layout_values import SheetStock

        _, visits = counted_project
        inventory = PhysicalItemCounter().count(visits)
        report = InventorySheetRequirements(SheetStock(allow_rotation=True)).calculate(inventory)
        assert {(group["material_id"], group["thickness_mm"]): group["sheet_count"]
                for group in report["groups"]} == {
            ("", 9.0): 1, ("", 15.0): 1,
            ("Test white back panel, 18 mm", 18.0): 4,
            ("Test white cabinet panel, 18 mm", 18.0): 8,
            ("Test white door panel, 18 mm", 18.0): 4,
        }
        assert report["part_count"] == 47
        assert report["oversized_part_paths"] == []

    def test_command_writes_draft_without_replacing_fabrication_bom(self, counted_project):
        root, _ = counted_project
        bom = root / "manufacturing/bom.json"
        bom.parent.mkdir(exist_ok=True)
        bom.write_text("preserve fabrication evidence", encoding="utf-8")
        assert CountPhysicalItemsCommand().run(root) == 2
        report = json.loads((root / "manufacturing/item-counts.json").read_text())
        assert report["totals"]["brass_inserts"] == 79
        assert bom.read_text() == "preserve fabrication evidence"

    def test_failed_builder_revokes_previous_count(self, tmp_path):
        output = tmp_path / "manufacturing/item-counts.json"
        output.parent.mkdir()
        output.write_text('{"status":"draft","totals":{"brass_inserts":127}}')
        with pytest.raises(ValueError):
            CountPhysicalItemsCommand().run(tmp_path)
        assert json.loads(output.read_text())["status"] == "invalid"
