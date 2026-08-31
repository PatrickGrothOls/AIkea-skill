"""Scope: Render the reusable cabinet-door feature and its owned declarations."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cabinet_feature_builder_wrapper_renderer import (
    CabinetFeatureBuilderWrapperRenderer,
)
from door_hardware_spec_renderer import DoorHardwareSpecRenderer
from door_hinge_plan import DoorHingePlan
from riex_nc70_hinge_profile import RiexNc70HingeProfile


class CabinetDoorFeatureFileSetRenderer:
    """Create one generated door feature without review-only geometry stitching."""

    def __init__(self) -> None:
        self.hardware = DoorHardwareSpecRenderer()
        self.wrapper = CabinetFeatureBuilderWrapperRenderer()

    def render(
        self,
        assembly: Any,
        plan: DoorHingePlan,
        profile: RiexNc70HingeProfile,
    ) -> dict[Path, str]:
        root = Path("assemblies") / plan.assembly_id
        return {
            root / "door_hinges/__init__.py": (
                f'"""Scope: Contain the door feature owned by {plan.assembly_id}."""\n'
            ),
            root / "door_hinges/plan.py": self._plan(plan),
            root / "door_hinges/hardware.py": self.hardware.render(
                assembly, plan, profile
            ),
            root / "door_hinges/feature.py": self._feature(plan),
            root / "door_hinges/review.py": self._review(),
            root / "with_door_builder.py": self.wrapper.render(
                plan.assembly_id,
                "door_hinges.feature",
            ),
        }

    def _plan(self, plan: DoorHingePlan) -> str:
        return (
            f'"""Scope: Load the saved hinge plan for {plan.assembly_id}."""\n\n'
            "from pathlib import Path\n"
            "from door_hinge_plan import DoorHingePlan\n\n\n"
            "PLAN = DoorHingePlan.read(Path(__file__).with_name('installation.json'))\n"
        )

    def _feature(self, plan: DoorHingePlan) -> str:
        return (
            f'"""Scope: Apply the fitted door and hinges to {plan.assembly_id}."""\n\n'
            "from dataclasses import replace\n"
            "from assemblies.specification import (\n"
            "    BuiltAssembly, BuiltPurchasedHardware,\n"
            ")\n"
            "from concealed_hinge_machining import ConcealedHingeMachining\n"
            "from riex_nc70_hinge_profile import RIEX_NC70_FULL_OVERLAY\n\n"
            "from .hardware import DOOR_HARDWARE\n"
            "from .plan import PLAN\n\n\n"
            "class CabinetDoorFeature:\n"
            "    \"\"\"Machine the door and retain every purchased hinge instance.\"\"\"\n\n"
            "    def apply(self, cabinet) -> BuiltAssembly:\n"
            "        machined = ConcealedHingeMachining().apply(\n"
            "            cabinet, PLAN, RIEX_NC70_FULL_OVERLAY\n"
            "        )\n"
            "        replacements = {\n"
            "            'door_panel': machined.door,\n"
            "            PLAN.hinge_side.side_part_id: machined.cabinet_side,\n"
            "        }\n"
            "        parts = tuple(\n"
            "            replace(part, solid=replacements.get(part.spec.part_id, part.solid))\n"
            "            for part in cabinet.parts\n"
            "        )\n"
            "        spec = replace(\n"
            "            cabinet.spec,\n"
            "            purchased_hardware=(\n"
            "                cabinet.spec.purchased_hardware + DOOR_HARDWARE\n"
            "            ),\n"
            "        )\n"
            "        hardware = tuple(\n"
            "            BuiltPurchasedHardware(item, None) for item in DOOR_HARDWARE\n"
            "        )\n"
            "        return BuiltAssembly(\n"
            "            spec=spec, parts=parts, joints=cabinet.joints, cuts=cabinet.cuts,\n"
            "            child_assemblies=cabinet.child_assemblies,\n"
            "            purchased_hardware=cabinet.purchased_hardware + hardware,\n"
            "        )\n\n\n"
            "FEATURE = CabinetDoorFeature()\n"
        )

    def _review(self) -> str:
        return (
            '"""Scope: Contribute exact door poses to generic assembly review."""\n\n'
            "from riex_nc70_door_review_feature import RiexNc70DoorReviewFeature\n\n"
            "from .plan import PLAN\n\n\n"
            "REVIEW = RiexNc70DoorReviewFeature(PLAN)\n"
        )


__all__ = ["CabinetDoorFeatureFileSetRenderer"]
