"""Scope: Contribute exact Riex door states to generic assembly review."""

from __future__ import annotations

from assembly_feature_review import AssemblyFeatureReviewContext
from assembly_tree_review_plan import (
    AssemblyReviewOverlay,
    AssemblyTreeReviewPlan,
)
from concealed_hinge_machining import HingedPanelSet
from door_hinge_review_geometry import DoorHingeReviewGeometry
from riex_nc70_hardware_loader import RiexNc70HardwareLoader
from riex_nc70_hinge_profile import RIEX_NC70_FULL_OVERLAY
from unit_mockup import UnitMockupInputError


class RiexNc70DoorReviewFeature:
    """Replace closed tree items only when an alternate door pose is requested."""

    _STATES = {"closed", "open", "removed"}

    def __init__(self, plan) -> None:
        self.saved_plan = plan
        self.geometry = DoorHingeReviewGeometry()
        self.hardware = RiexNc70HardwareLoader()

    def plan(
        self,
        context: AssemblyFeatureReviewContext,
        state: str,
    ) -> AssemblyTreeReviewPlan:
        if state not in self._STATES:
            raise UnitMockupInputError([f"unsupported door review state: {state}"])
        if state == "closed":
            return AssemblyTreeReviewPlan()
        hidden = self._hidden_paths(context)
        if state == "removed":
            return AssemblyTreeReviewPlan(hidden_paths=hidden)
        parts = {part.spec.part_id: part for part in context.assembly.parts}
        machined = HingedPanelSet(
            door=parts[self.saved_plan.door_part_id].solid,
            cabinet_side=parts[self.saved_plan.support_part_id].solid,
        )
        exact = self.geometry.build(
            context.assembly,
            machined,
            self.hardware.load(context.project_root / "hardware/riex/nc70"),
            self.saved_plan,
            RIEX_NC70_FULL_OVERLAY,
            True,
        )
        owned_names = {self.saved_plan.door_part_id, *(name for item in self.saved_plan.placements
                       for name in (f"{item.hinge_id}__source_cad", f"{item.hinge_id}_plate__source_cad"))}
        overlay = tuple(
            part
            for part in exact
            if part.name in owned_names
        )
        return AssemblyTreeReviewPlan(
            hidden_paths=hidden,
            overlays=(AssemblyReviewOverlay(context.owner_path, overlay),),
        )

    def _hidden_paths(
        self,
        context: AssemblyFeatureReviewContext,
    ) -> tuple[tuple[str, ...], ...]:
        door = context.owner_path + (f"part:{self.saved_plan.door_part_id}",)
        owned_ids = {f"{item.hinge_id}_{kind}" for item in self.saved_plan.placements for kind in ("hinge", "plate")}
        hardware = tuple(
            context.owner_path + (f"hardware:{item.spec.hardware_id}",)
            for item in context.assembly.purchased_hardware
            if item.spec.hardware_id in owned_ids
        )
        return (door, *hardware)


__all__ = ["RiexNc70DoorReviewFeature"]
