"""Scope: Prevent explicit connector purchases from duplicating paired-cut requirements."""

from types import SimpleNamespace as Value

import pytest

from cabineo_purchase_reconciler import CabineoPurchaseReconciler
from hardware_purchase_counter import HardwarePurchaseCounter
from physical_item_counter import PhysicalItemCounter
from purchased_hardware_spec import ConnectionPurchaseSpec, HardwarePurchaseSpec


class TestConnectionPurchaseReconciliation:
    """Use explicit purchase-to-connection links, never a product-name guess."""

    def _visit(self, component="connector", joint_id="corner", index=1):
        purchase = HardwarePurchaseSpec(
            component, f"test-{component}", "piece", "item", ("item",),
            connection=ConnectionPurchaseSpec(joint_id, index, component),
        )
        hardware = Value(spec=Value(manufacturer="test", purchase=purchase))
        return Value(path=("root_01", "cabinet_01", f"hardware:{component}"), hardware=hardware)

    def _occurrences(self):
        return [dict(path=f"root_01/cabinet_01/joint:corner/connector:{index}")
                for index in (1, 2)]

    def test_modeled_connector_and_insert_remove_only_matching_implicit_requirements(self):
        unresolved = []
        rows = HardwarePurchaseCounter().count([self._visit(), self._visit("insert")], unresolved)
        missing = CabineoPurchaseReconciler().remaining(self._occurrences(), rows, unresolved)
        assert len(rows) == 2
        assert all(items == self._occurrences()[1:] for items in missing.values())
        assert unresolved == []

    @pytest.mark.parametrize("defect", ["wrong_joint", "wrong_occurrence", "wrong_role", "duplicate", "pack"])
    def test_unverified_purchase_link_cannot_suppress_required_items(self, defect):
        unresolved = []
        visits = {
            "wrong_joint": [self._visit(joint_id="missing")],
            "wrong_occurrence": [self._visit(index=3)],
            "wrong_role": [self._visit(component="guess")],
            "duplicate": [self._visit()], "pack": [self._visit()],
        }[defect]
        rows = HardwarePurchaseCounter().count(visits, unresolved)
        if defect == "duplicate":
            rows = rows * 2
        if defect == "pack":
            rows[0]["unit"] = "pack"
        missing = CabineoPurchaseReconciler().remaining(self._occurrences(), rows, unresolved)
        assert missing["connector"] == self._occurrences()
        assert unresolved[0]["code"] == "connection.purchase_mismatch"

    def test_legacy_purchase_without_connection_does_not_suppress_connectors(self):
        missing = CabineoPurchaseReconciler().remaining(self._occurrences(), [dict(path="other")], [])
        assert missing["connector"] == self._occurrences()

    def test_physical_counter_counts_modeled_and_unmodeled_occurrences_once(self):
        source = Value(part_id="source", role="panel", material_id="mdf", local_size_mm=(600, 400, 16))
        receiver = Value(part_id="receiver", role="panel", material_id="mdf", local_size_mm=(400, 600, 16))
        joint = Value(joint_id="corner", joint_type="cabineo", source_part_id="source",
                      target_part_id="receiver", source_face=">Z", source_edge=">X",
                      connector_layout="bounded_spacing")
        cuts = tuple(Value(joint_id="corner", part_id=part.part_id, connector_index=index)
                     for part in (source, receiver) for index in (1, 2))
        owner = ("root_01", "cabinet_01")
        parts = tuple(Value(spec=part) for part in (source, receiver))
        assembly = Value(spec=Value(machining=()), parts=parts, joints=(joint,), cuts=cuts)
        visits = [Value(path=owner, assembly=assembly)]
        visits.extend(Value(path=(*owner, f"part:{part.spec.part_id}"), part=part) for part in parts)
        for component in ("connector", "insert"):
            visit = self._visit(component)
            spec = visit.hardware.spec
            spec.hardware_id = component
            spec.product_code = spec.purchase.product_code
            spec.hardware_asset_id = f"test-{component}"
            spec.geometry_selector = None
            visit.local_to_root = object()
            visits.append(visit)
        result = PhysicalItemCounter().count(visits)
        assert result["totals"]["verified_cabineos"] == result["totals"]["brass_inserts"] == 2
        assert len(result["purchased_units"]) == 2
        assert sum(row["quantity"] for row in result["purchased_summary"]) == 4
        assert {item["code"] for item in result["unresolved"]} == {"cabineo.purchase_sku_missing"}
