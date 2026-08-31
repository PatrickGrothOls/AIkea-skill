"""Scope: Merge independent feature review contributions into one tree plan."""

from __future__ import annotations

from assembly_tree_review_plan import AssemblyTreeReviewPlan


class AssemblyReviewPlanComposer:
    """Combine feature plans while retaining the tree plan's validation."""

    def compose(
        self,
        plans: tuple[AssemblyTreeReviewPlan, ...],
    ) -> AssemblyTreeReviewPlan:
        return AssemblyTreeReviewPlan(
            motions=tuple(item for plan in plans for item in plan.motions),
            hidden_paths=tuple(
                item for plan in plans for item in plan.hidden_paths
            ),
            hidden_subtrees=tuple(
                item for plan in plans for item in plan.hidden_subtrees
            ),
            overlays=tuple(item for plan in plans for item in plan.overlays),
        )


__all__ = ["AssemblyReviewPlanComposer"]
