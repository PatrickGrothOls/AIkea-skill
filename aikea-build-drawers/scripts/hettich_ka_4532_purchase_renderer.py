"""Scope: Declare installed KA 4532 runner pairs and individual spacer purchases."""


class HettichKa4532PurchaseRenderer:
    """Give fixed and moving rail members the same cabinet-owned purchase ID."""

    def runner(self, plan, side: str, moving: bool) -> str:
        member = f"{side}-{'moving' if moving else 'fixed'}"
        return (
            "HardwarePurchaseSpec("
            f"{plan.drawer.assembly_id + '_runner_pair'!r}, "
            f"{plan.hardware.runner_item_number!r}, 'pair', {member!r}, "
            "('left-fixed', 'right-fixed', 'left-moving', 'right-moving'), "
            f"owner_levels_up={int(moving)})"
        )

    def spacer(self, plan, side: str) -> str:
        return (
            "HardwarePurchaseSpec("
            f"{plan.drawer.assembly_id + '_spacer_' + side!r}, "
            f"{plan.hardware.spacer_item_number!r}, 'piece', 'item', ('item',))"
        )
