"""Scope: Validate every review-plan target against one unposed assembly tree."""

from __future__ import annotations

from typing import Any

from assembly_tree_review_plan import AssemblyTreeReviewPlan
from unit_mockup import UnitMockupInputError


class AssemblyTreeReviewPlanValidator:
    """Reject presentation changes that would otherwise disappear silently."""

    def validate(
        self,
        visits: tuple[Any, ...],
        plan: AssemblyTreeReviewPlan,
    ) -> None:
        assembly_paths = {
            item.path
            for item in visits
            if type(item).__name__ == "AssemblyTreeAssembly"
        }
        physical_paths = {
            item.path
            for item in visits
            if type(item).__name__ in {"AssemblyTreePart", "AssemblyTreeHardware"}
        }
        target_groups = (
            ("motion", (item.assembly_path for item in plan.motions), assembly_paths),
            ("hidden item", iter(plan.hidden_paths), physical_paths),
            ("hidden subtree", iter(plan.hidden_subtrees), assembly_paths),
            ("overlay", (item.owner_path for item in plan.overlays), assembly_paths),
        )
        problems = tuple(
            f"review {label} targets an unknown path: {'/'.join(path)}"
            for label, paths, known_paths in target_groups
            for path in paths
            if path not in known_paths
        )
        if problems:
            raise UnitMockupInputError(problems)


__all__ = ["AssemblyTreeReviewPlanValidator"]
