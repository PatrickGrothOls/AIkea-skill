"""Scope: Render exact KA 4532 and 13952 instances in their physical frames."""

from __future__ import annotations

from hardware_placement_renderer import HardwarePlacementRenderer
from hettich_ka_4532_purchase_renderer import HettichKa4532PurchaseRenderer


class HettichKa4532SpacerHardwareSpecRenderer:
    """Separate cabinet-fixed hardware from drawer-following members."""

    def __init__(self) -> None:
        self.placements = HardwarePlacementRenderer()
        self.purchases = HettichKa4532PurchaseRenderer()

    def render(self, plan) -> str:
        profile = plan.hardware
        mounting = plan.hardware_mounting
        fixed = tuple(
            (
                f"runner_{side}_fixed",
                profile.runner_product_code,
                profile.runner_asset_id,
                f"{side}-fixed",
                getattr(mounting, f"fixed_runner_{side}_in_cabinet"),
                self.purchases.runner(plan, side, moving=False),
            )
            for side in ("left", "right")
        )
        spacers = tuple(
            (
                f"spacer_{side}",
                profile.spacer_product_code,
                profile.spacer_asset_id,
                None,
                getattr(mounting, f"spacer_{side}_in_cabinet"),
                self.purchases.spacer(plan, side),
            )
            for side in ("left", "right")
        )
        moving = tuple(
            (
                f"runner_{side}_moving",
                profile.runner_product_code,
                profile.runner_asset_id,
                f"{side}-moving",
                getattr(mounting, f"moving_runner_{side}_in_drawer"),
                self.purchases.runner(plan, side, moving=True),
            )
            for side in ("left", "right")
        )
        drawer_id = plan.drawer.assembly_id
        return self._collection(
            "CABINET_HARDWARE",
            drawer_id,
            fixed + spacers,
        ) + self._collection("DRAWER_HARDWARE", drawer_id, moving)

    def _collection(self, name, drawer_id, values) -> str:
        items = "".join(
            self._hardware(drawer_id, *value) for value in values
        )
        return f"{name} = (\n{items})\n"

    def _hardware(
        self,
        drawer_id,
        suffix,
        product,
        asset,
        selector,
        placement,
        purchase,
    ) -> str:
        selector_source = f", geometry_selector={selector!r}" if selector else ""
        return (
            "    PurchasedHardwareSpec(\n"
            f"        {drawer_id + '_' + suffix!r}, 'Hettich', {product!r}, {asset!r},\n"
            "        " + self.placements.render(placement, "        ")
            + selector_source + ",\n"
            f"        purchase={purchase},\n"
            "    ),\n"
        )

__all__ = ["HettichKa4532SpacerHardwareSpecRenderer"]
