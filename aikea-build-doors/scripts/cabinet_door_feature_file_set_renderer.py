"""Scope: Render the reusable cabinet-door feature and its owned declarations."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cabinet_feature_builder_wrapper_renderer import (
    CabinetFeatureBuilderWrapperRenderer,
)
from door_hardware_spec_renderer import DoorHardwareSpecRenderer
from door_machining_source_renderer import DoorMachiningSourceRenderer
from complete_assembly_builder_renderer import CompleteAssemblyBuilderRenderer
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
            root / "complete_builder.py": CompleteAssemblyBuilderRenderer().render(plan.assembly_id),
            root / "door_hinges/machining.py": DoorMachiningSourceRenderer().render(assembly, plan, profile),
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
            f'"""Scope: Apply declared hinge machining and owned purchases to {plan.assembly_id}."""\n\n'
            "from dataclasses import replace\n"
            "from assemblies.specification import BuiltPurchasedHardware\n"
            "from panel_machining_feature import PanelMachiningFeature\n\n"
            "from .hardware import DOOR_HARDWARE\n"
            "from .machining import DOOR_MACHINING, DOOR_REQUIREMENTS\n\n\n"
            "class CabinetDoorFeature:\n"
            "    def apply(self, cabinet):\n"
            "        machined = PanelMachiningFeature().apply(cabinet, DOOR_MACHINING, DOOR_REQUIREMENTS)\n"
            "        spec = replace(machined.spec, purchased_hardware=machined.spec.purchased_hardware + DOOR_HARDWARE)\n"
            "        hardware = tuple(BuiltPurchasedHardware(item, None) for item in DOOR_HARDWARE)\n"
            "        return replace(machined, spec=spec, purchased_hardware=machined.purchased_hardware + hardware)\n\n\n"
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
