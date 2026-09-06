"""Scope: Protect official KA 4532 axes and exact-spacer support evidence."""

from importlib.util import find_spec

import pytest

pytestmark = pytest.mark.skipif(find_spec("cadquery") is None, reason="requires CadQuery")

if find_spec("cadquery") is not None:
    import cadquery as cq

    from hettich_ka_4532_spacer_fixing_alignment_checker import (
        HettichKa4532SpacerFixingAlignmentChecker,
        HettichKa4532SpacerFixingAlignmentError,
    )
    from hettich_ka_4532_spacer_mounting_planner import (
        HettichKa4532SpacerMountingPlanner,
    )
from hettich_ka_4532_spacer_mounting_test_support import (
    HettichKa4532SpacerMountingTestSupport,
)


class TestHettichKa4532SpacerFixingAlignmentChecker:
    """Require all four official holes and a solid drilling path on both sides."""

    _FIXTURE = HettichKa4532SpacerMountingTestSupport()

    def test_verifies_the_official_pattern_in_both_purchased_shapes(self) -> None:
        step_set, mounting = self._installed_set()

        evidence = HettichKa4532SpacerFixingAlignmentChecker().verify(
            step_set, mounting
        )

        assert evidence.installation_document == "Hettich MS 10547.00.000"
        assert evidence.hole_diameter_mm == 6.4
        assert evidence.spacer_support_width_mm == 25.0
        assert evidence.cabinet_depth_axes_mm == (37.0, 165.0, 261.0, 325.0)
        assert tuple(axis.side for axis in evidence.axes) == ("left",) * 4 + (
            "right",
        ) * 4
        assert {axis.spacer_native_height_mm for axis in evidence.axes} == {25.0}
        assert tuple(
            axis.spacer_native_depth_mm for axis in evidence.axes[:4]
        ) == (27.0, 155.0, 251.0, 315.0)

    def test_rejects_a_runner_without_an_official_opening(self) -> None:
        step_set, mounting = self._installed_set()
        step_set.runner_left.fixed_member = self._FIXTURE._member(0.0, 502.483917)

        with pytest.raises(
            HettichKa4532SpacerFixingAlignmentError,
            match="fixed runner is closed",
        ):
            HettichKa4532SpacerFixingAlignmentChecker().verify(step_set, mounting)

    def test_rejects_a_void_in_the_spacer_support_corridor(self) -> None:
        step_set, mounting = self._installed_set()
        void = cq.Solid.makeCylinder(
            3.2,
            25.0,
            cq.Vector(0.0, 27.0, 25.0),
            cq.Vector(1.0, 0.0, 0.0),
        )
        step_set.spacer_solid = step_set.spacer_solid.cut(void)

        with pytest.raises(
            HettichKa4532SpacerFixingAlignmentError,
            match="spacer lacks full material",
        ):
            HettichKa4532SpacerFixingAlignmentChecker().verify(step_set, mounting)

    def _installed_set(self):
        step_set = self._FIXTURE.step_set()
        mounting = HettichKa4532SpacerMountingPlanner().plan(
            self._FIXTURE.cabinet(),
            step_set,
            cabinet_front_mm=0.0,
            drawer_front_mm=18.0,
            drawer_bottom_mm=100.0,
        )
        return step_set, mounting


__all__ = ["TestHettichKa4532SpacerFixingAlignmentChecker"]
