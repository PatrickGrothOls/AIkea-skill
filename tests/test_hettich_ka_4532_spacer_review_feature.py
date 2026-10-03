"""Scope: Protect recursive KA 4532 drawer motion and visibility."""

from types import SimpleNamespace

import pytest

from hettich_ka_4532_spacer_review_feature import (
    HettichKa4532SpacerReviewFeature,
)
from unit_mockup import UnitMockupInputError


class ReviewFeatureWithoutCad(HettichKa4532SpacerReviewFeature):
    """Expose the saved travel without loading CadQuery in unit tests."""

    def _drawer_motion(self):
        return (0.0, -self.extension_mm, 0.0)


class TestHettichKa4532SpacerReviewFeature:
    """Keep movement on the drawer subtree and therefore its moving rails."""

    @pytest.mark.parametrize(
        ("state", "has_motion", "drawer_hidden"),
        (
            ("closed", False, False),
            ("open", True, False),
            ("removed", False, True),
        ),
    )
    def test_plans_the_complete_drawer_subtree(
        self,
        state,
        has_motion,
        drawer_hidden,
    ) -> None:
        feature = ReviewFeatureWithoutCad("drawer_01", 500.0)
        context = SimpleNamespace(owner_path=("wardrobe_01", "cabinet_01"))
        drawer = context.owner_path + ("drawer_01",)

        plan = feature.plan(context, state)

        assert bool(plan.motions) is has_motion
        if has_motion:
            assert plan.motions[0].assembly_path == drawer
            assert plan.motions[0].location == (0.0, -500.0, 0.0)
        assert plan.hides(drawer + ("part:left_side",)) is drawer_hidden
        assert plan.hides(
            drawer + ("hardware:drawer_01_runner_left_moving",)
        ) is drawer_hidden
        assert not plan.hides(
            context.owner_path + ("hardware:drawer_01_spacer_left",)
        )

    def test_rejects_unknown_state(self) -> None:
        feature = ReviewFeatureWithoutCad("drawer_01", 500.0)

        with pytest.raises(UnitMockupInputError, match="state is invalid"):
            feature.plan(SimpleNamespace(owner_path=("cabinet_01",)), "half-open")
