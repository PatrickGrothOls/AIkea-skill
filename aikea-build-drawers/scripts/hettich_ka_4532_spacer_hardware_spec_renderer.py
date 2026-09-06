"""Scope: Render exact KA 4532 and 13952 instances in their physical frames."""

from __future__ import annotations

from drawer_hardware_mounting_plan import HardwarePlacement
from hardware_placement_renderer import HardwarePlacementRenderer


class HettichKa4532SpacerHardwareSpecRenderer:
    """Separate cabinet-fixed hardware from drawer-following members."""

    def __init__(self) -> None:
        self.placements = HardwarePlacementRenderer()

    def render(self, plan) -> str:
        profile = plan.hardware
        mounting = plan.hardware_mounting
        step = plan.hardware_step
        fixed = tuple(
            (
                f"runner_{side}_fixed",
                profile.runner_product_code,
                profile.runner_asset_id,
                f"{side}-fixed",
                getattr(mounting, f"fixed_runner_{side}_in_cabinet"),
                getattr(step, f"runner_{side}").fixed_member,
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
                step.spacer_solid,
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
                getattr(step, f"runner_{side}").moving_member,
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
        shape,
    ) -> str:
        selector_source = f", geometry_selector={selector!r}" if selector else ""
        installed = self._installed_placement(placement, shape)
        return (
            "    PurchasedHardwareSpec(\n"
            f"        {drawer_id + '_' + suffix!r}, 'Hettich', {product!r}, {asset!r},\n"
            "        " + self.placements.render(installed, "        ")
            + selector_source + ",\n"
            "    ),\n"
        )

    def _installed_placement(self, placement, shape) -> HardwarePlacement:
        import cadquery as cq
        from OCP.gp import gp_Pnt, gp_Vec

        mounting = cq.Location(
            cq.Plane(
                origin=placement.origin_mm,
                xDir=placement.local_x_in_owner,
                normal=placement.local_z_in_owner,
            )
        )
        transform = (mounting * shape.location()).wrapped.Transformation()
        origin = gp_Pnt().Transformed(transform)
        axes = tuple(
            gp_Vec(*values).Transformed(transform)
            for values in (
                (1.0, 0.0, 0.0),
                (0.0, 1.0, 0.0),
                (0.0, 0.0, 1.0),
            )
        )
        return HardwarePlacement(
            self._coordinates(origin),
            self._coordinates(axes[0]),
            self._coordinates(axes[1]),
            self._coordinates(axes[2]),
        )

    def _coordinates(self, value) -> tuple[float, float, float]:
        return (float(value.X()), float(value.Y()), float(value.Z()))


__all__ = ["HettichKa4532SpacerHardwareSpecRenderer"]
