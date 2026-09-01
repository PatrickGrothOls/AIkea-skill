"""Scope: Articulate one generated KA 4532 drawer in recursive review."""

from __future__ import annotations

from typing import Any

from assembly_tree_review_plan import AssemblyReviewMotion, AssemblyTreeReviewPlan
from unit_mockup import UnitMockupInputError


class HettichKa4532SpacerReviewFeature:
    """Move or hide the drawer subtree that owns its exact moving members."""

    _STATES = {"closed", "open", "removed"}

    def __init__(self, drawer_id: str, extension_mm: float) -> None:
        self.drawer_id = drawer_id
        self.extension_mm = extension_mm

    def plan(self, context: Any, state: str) -> AssemblyTreeReviewPlan:
        if state not in self._STATES:
            raise UnitMockupInputError(
                [f"{self.drawer_id} drawer review state is invalid: {state}"]
            )
        drawer_path = context.owner_path + (self.drawer_id,)
        motions = (
            (AssemblyReviewMotion(drawer_path, self._drawer_motion()),)
            if state == "open"
            else ()
        )
        hidden = (drawer_path,) if state == "removed" else ()
        return AssemblyTreeReviewPlan(
            motions=motions,
            hidden_subtrees=hidden,
        )

    def _drawer_motion(self) -> Any:
        import cadquery as cq

        return cq.Location(cq.Vector(0.0, -self.extension_mm, 0.0))


__all__ = ["HettichKa4532SpacerReviewFeature"]
