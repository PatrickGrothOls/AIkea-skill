"""Scope: Verify explicit purchase membership, missing declarations and fasteners."""

from types import SimpleNamespace as Value

import pytest

from hardware_purchase_counter import HardwarePurchaseCounter


class TestHardwarePurchaseCounter:
    """Prevent partial, duplicated or colliding members from becoming purchases."""

    def visit(self, member="left", owner=("wardrobe_01", "cabinet_01"), **overrides):
        purchase = Value(**(dict(purchase_id="drawer_01_runners", product_code="test-sku",
                                unit="pair", member=member, required_members=("left", "right"),
                                owner_levels_up=0, mounting_fasteners_included=True) | overrides))
        spec = Value(manufacturer="test-maker", purchase=purchase)
        return Value(path=(*owner, f"hardware:{purchase.purchase_id}_{member}"), hardware=Value(spec=spec))

    @pytest.mark.parametrize("case", ["missing", "duplicate", "different_sku", "different_members", "outside_root"])
    def test_incomplete_or_conflicting_members_do_not_count(self, case):
        left, right = self.visit(), self.visit("right")
        variants = {
            "missing": [left], "duplicate": [left, left, right],
            "different_sku": [left, self.visit("right", product_code="other-sku")],
            "different_members": [left, self.visit("right", required_members=("right",))],
            "outside_root": [self.visit(owner_levels_up=2)],
        }
        unresolved = []
        assert HardwarePurchaseCounter().count(variants[case], unresolved) == []
        assert unresolved

    def test_repeated_drawer_ids_in_separate_cabinets_stay_separate(self):
        visits = [self.visit(side, ("wardrobe_01", cabinet))
                  for cabinet in ("cabinet_01", "cabinet_02") for side in ("left", "right")]
        unresolved = []
        counter = HardwarePurchaseCounter()
        rows = counter.count(visits, unresolved)
        assert len(rows) == 2
        assert counter.summarize(rows)[0]["quantity"] == 2
        assert unresolved == []

    def test_hinges_and_handles_are_pieces_with_included_fasteners(self):
        visits = [self.visit("item", purchase_id=kind, product_code=f"test-{kind}",
                             unit="piece", required_members=("item",))
                  for kind in ("hinge", "plate", "handle")]
        unresolved = []
        rows = HardwarePurchaseCounter().count(visits, unresolved)
        assert len(rows) == 3
        assert all(row["quantity"] == 1 and row["mounting_fasteners_included"] for row in rows)
        assert unresolved == []

    def test_explicit_fastener_exception_is_reported(self):
        unresolved = []
        visits = [self.visit(side, mounting_fasteners_included=False) for side in ("left", "right")]
        assert len(HardwarePurchaseCounter().count(visits, unresolved)) == 1
        assert unresolved[0]["code"] == "hardware.separate_fasteners_required"

    def test_legacy_hardware_is_unresolved_without_guessing_sets(self):
        visit = self.visit()
        del visit.hardware.spec.purchase
        unresolved = []
        assert HardwarePurchaseCounter().count([visit], unresolved) == []
        assert unresolved[0]["code"] == "hardware.purchase_undefined"
