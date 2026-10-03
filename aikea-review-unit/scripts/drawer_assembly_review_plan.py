"""Scope: Translate one drawer review state into generic assembly-tree changes."""

from __future__ import annotations

from typing import Any

from assembly_tree_review_plan import (
    AssemblyReviewMotion,
    AssemblyReviewOverlay,
    AssemblyTreeReviewPlan,
)
from drawer_review_motion import DrawerReviewMotion
from drawer_review_state import DrawerReviewState


class DrawerAssemblyReviewPlanBuilder:
    """Keep drawer semantics outside the generic recursive tree renderer."""

    def __init__(self) -> None:
        self.motion = DrawerReviewMotion()

    def build(
        self,
        built_cabinet: Any,
        state: DrawerReviewState,
        hardware_parts: tuple[Any, ...],
    ) -> AssemblyTreeReviewPlan:
        child = next(
            item
            for item in built_cabinet.child_assemblies
            if item.spec.purpose == "drawer"
        )
        cabinet_path = ("wardrobe_01", built_cabinet.spec.assembly_id)
        drawer_path = cabinet_path + (child.spec.assembly_id,)
        runner_ids = {
            "runner_left",
            "runner_right",
            f"{child.spec.assembly_id}_runner_left",
            f"{child.spec.assembly_id}_runner_right",
        }
        locking_device_ids = {"locking_device_left", "locking_device_right"}
        hidden_hardware = tuple(
            cabinet_path + (f"hardware:{item.spec.hardware_id}",)
            for item in built_cabinet.purchased_hardware
            if item.spec.hardware_id in runner_ids
        ) + tuple(
            drawer_path + (f"hardware:{item.spec.hardware_id}",)
            for item in child.assembly.purchased_hardware
            if item.spec.hardware_id in locking_device_ids
        )
        motions = (
            (
                AssemblyReviewMotion(
                    drawer_path,
                    self.motion.location(
                        state,
                        child.assembly.spec.box.side_length_mm,
                    ),
                ),
            )
            if state is DrawerReviewState.OPEN
            else ()
        )
        hidden_subtrees = (
            (drawer_path,) if state is DrawerReviewState.REMOVED else ()
        )
        return AssemblyTreeReviewPlan(
            motions=motions,
            hidden_paths=hidden_hardware,
            hidden_subtrees=hidden_subtrees,
            overlays=(AssemblyReviewOverlay(cabinet_path, hardware_parts),),
        )


__all__ = ["DrawerAssemblyReviewPlanBuilder"]
