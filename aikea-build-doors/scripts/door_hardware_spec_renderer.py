"""Scope: Render exact closed hinge and plate instances for one cabinet."""

from __future__ import annotations

from typing import Any

from door_hinge_plan import DoorHingePlan
from riex_nc70_hardware_frame import (
    RiexNc70HardwareFrame,
    RiexNc70HardwareFrameResolver,
)
from riex_nc70_hinge_profile import RiexNc70HingeProfile


class DoorHardwareSpecRenderer:
    """Write each purchased hinge component in its cabinet-local frame."""

    def __init__(self) -> None:
        self.frames = RiexNc70HardwareFrameResolver()

    def render(
        self,
        assembly: Any,
        plan: DoorHingePlan,
        profile: RiexNc70HingeProfile,
    ) -> str:
        hardware = []
        for placement in plan.placements:
            hardware.extend(
                (
                    self._hardware(
                        f"{placement.hinge_id}_hinge",
                        "F000001",
                        "riex-nc70-f000001-closed",
                        self.frames.hinge(
                            assembly,
                            profile,
                            float(assembly.door_bottom_mm)
                            + placement.door_height_mm,
                            plan.hinge_side,
                        ),
                    ),
                    self._hardware(
                        f"{placement.hinge_id}_plate",
                        "F000049",
                        "riex-nc70-f000049-h0-euroscrew-plate",
                        self.frames.plate(
                            assembly,
                            profile,
                            float(assembly.base_height_mm)
                            + placement.cabinet_height_mm,
                            plan.hinge_side,
                        ),
                    ),
                )
            )
        return (
            f'"""Scope: Declare exact purchased hinge instances for {plan.assembly_id}."""\n\n'
            "from assemblies.specification import (\n"
            "    AxisBasis, AxisDirection, LocalToParentPlacement, Point3D,\n"
            "    PurchasedHardwareSpec,\n"
            ")\n\n\n"
            "DOOR_HARDWARE = (\n"
            + "".join(hardware)
            + ")\n"
        )

    def _hardware(
        self,
        hardware_id: str,
        product_code: str,
        asset_id: str,
        frame: RiexNc70HardwareFrame,
    ) -> str:
        return (
            "    PurchasedHardwareSpec(\n"
            f"        hardware_id={hardware_id!r},\n"
            "        manufacturer='Riex',\n"
            f"        product_code={product_code!r},\n"
            f"        hardware_asset_id={asset_id!r},\n"
            f"        local_to_parent={self._placement(frame)},\n"
            "    ),\n"
        )

    def _placement(self, frame: RiexNc70HardwareFrame) -> str:
        return (
            "LocalToParentPlacement("
            f"Point3D{frame.origin_mm!r}, "
            "AxisBasis("
            f"AxisDirection{frame.local_x_in_cabinet!r}, "
            f"AxisDirection{frame.local_y_in_cabinet!r}, "
            f"AxisDirection{frame.local_z_in_cabinet!r}"
            ")"
            ")"
        )


__all__ = ["DoorHardwareSpecRenderer"]
