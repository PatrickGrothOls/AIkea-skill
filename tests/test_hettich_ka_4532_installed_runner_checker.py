"""Scope: Verify installed KA 4532 runner articulation and drawer datums."""

from dataclasses import replace

import pytest

from hettich_ka_4532_installed_geometry_test_support import (
    HettichKa4532InstalledGeometryTestSupport,
)
from hettich_ka_4532_installed_runner_checker import (
    HettichKa4532InstalledRunnerChecker,
)


class TestHettichKa4532InstalledRunnerChecker:
    """Bind exact fixed and moving runner members to drawer geometry."""

    def setup_method(self) -> None:
        self.support = HettichKa4532InstalledGeometryTestSupport()
        self.checker = HettichKa4532InstalledRunnerChecker()

    def test_accepts_exact_runner_and_drawer_relationship(self) -> None:
        datums = self._check(self.support.parts)

        assert datums is not None
        assert datums.drawer_axis_height_mm == 23.0

    @pytest.mark.parametrize(
        ("part_name", "x_mm", "y_mm"),
        (
            ("drawer_01__drawer_01_runner_left_moving", 1.0, 0.0),
            ("drawer_01__drawer_01_runner_right_moving", 0.0, 1.0),
            ("drawer_01__left_side", 1.0, 0.0),
            ("drawer_01__left_side", 0.0, 1.0),
        ),
    )
    def test_rejects_broken_closed_articulation(
        self, part_name: str, x_mm: float, y_mm: float
    ) -> None:
        shifted = self.support.shifted_parts(
            (part_name,), x_mm=x_mm, y_mm=y_mm
        )

        assert self._check(shifted) is None

    def test_rejects_front_and_rails_shifted_without_drawer_box(self) -> None:
        shifted = self.support.shifted_parts(
            (
                "drawer_01__front",
                "drawer_01__drawer_01_runner_left_moving",
                "drawer_01__drawer_01_runner_right_moving",
            ),
            y_mm=1.0,
        )

        assert self._check(shifted) is None

    def test_accepts_valid_complete_drawer_front_inset(self) -> None:
        drawer_names = tuple(
            name for name in self.support.parts if name.startswith("drawer_01__")
        )
        inset = self.support.shifted_parts(drawer_names, y_mm=20.0)

        assert self._check(inset) is not None

    def test_rejects_rotated_moving_member(self) -> None:
        rotated = dict(self.support.parts)
        part = rotated["drawer_01__drawer_01_runner_left_moving"]
        rotated[part.name] = replace(
            part,
            location=self.support.tilted_location((25.0, 0.0, 22.0)),
        )

        assert self._check(rotated) is None

    def _check(self, parts: dict):
        return self.checker.check("drawer_01", parts, self.support.source)


__all__ = ["TestHettichKa4532InstalledRunnerChecker"]
