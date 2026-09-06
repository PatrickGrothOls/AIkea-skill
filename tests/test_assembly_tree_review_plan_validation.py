"""Scope: Verify every generic review-plan target exists in the physical tree."""

from __future__ import annotations

import pytest

from assembly_tree_review_plan import (
    AssemblyReviewMotion,
    AssemblyReviewOverlay,
    AssemblyTreeReviewPlan,
)
from assembly_tree_review_plan_validator import AssemblyTreeReviewPlanValidator
from unit_mockup import UnitMockupInputError


class AssemblyTreeAssembly:
    """Represent an assembly visit for plan validation."""


class AssemblyTreePart:
    """Represent a manufactured-part visit for plan validation."""


class AssemblyTreeHardware:
    """Represent a purchased-hardware visit for plan validation."""


class TestAssemblyTreeReviewPlanValidation:
    """Prevent misspelled path selectors from producing plausible wrong reviews."""

    @pytest.mark.parametrize(
        ("plan", "message"),
        (
            (
                AssemblyTreeReviewPlan(
                    motions=(AssemblyReviewMotion(("cabinet_01", "missing_01"), object()),)
                ),
                "motion",
            ),
            (
                AssemblyTreeReviewPlan(
                    hidden_paths=(("cabinet_01", "part:missing"),)
                ),
                "hidden item",
            ),
            (
                AssemblyTreeReviewPlan(
                    hidden_subtrees=(("cabinet_01", "missing_01"),)
                ),
                "hidden subtree",
            ),
            (
                AssemblyTreeReviewPlan(
                    overlays=(
                        AssemblyReviewOverlay(("cabinet_01", "missing_01"), ()),
                    )
                ),
                "overlay",
            ),
        ),
    )
    def test_rejects_an_unknown_target(self, plan, message) -> None:
        with pytest.raises(UnitMockupInputError, match=message):
            AssemblyTreeReviewPlanValidator().validate(self._visits(), plan)

    def test_accepts_known_recursive_targets(self) -> None:
        drawer = ("cabinet_01", "drawer_01")
        plan = AssemblyTreeReviewPlan(
            motions=(AssemblyReviewMotion(drawer, object()),),
            hidden_paths=(drawer + ("hardware:lock",),),
            hidden_subtrees=(drawer,),
            overlays=(AssemblyReviewOverlay(("cabinet_01",), ()),),
        )

        AssemblyTreeReviewPlanValidator().validate(self._visits(), plan)

    def _visits(self):
        return (
            self._visit(AssemblyTreeAssembly, ("cabinet_01",)),
            self._visit(AssemblyTreeAssembly, ("cabinet_01", "drawer_01")),
            self._visit(AssemblyTreePart, ("cabinet_01", "part:side")),
            self._visit(
                AssemblyTreeHardware,
                ("cabinet_01", "drawer_01", "hardware:lock"),
            ),
        )

    def _visit(self, visit_type, path):
        item = visit_type()
        item.path = path
        return item


__all__ = ["TestAssemblyTreeReviewPlanValidation"]
