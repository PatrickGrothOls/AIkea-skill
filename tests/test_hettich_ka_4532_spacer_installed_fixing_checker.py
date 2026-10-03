"""Scope: Reject corrupted installed KA 4532 rail and spacer geometry."""

from dataclasses import replace

import cadquery as cq
import pytest

from hettich_ka_4532_installed_geometry_test_support import (
    HettichKa4532InstalledGeometryTestSupport,
)
from hettich_ka_4532_spacer_installed_fixing_checker import (
    HettichKa4532SpacerInstalledFixingChecker,
)


class TestHettichKa4532SpacerInstalledFixingChecker:
    """Bind both exact runner hands and spacers to cabinet and drawer datums."""

    _STATIC_HARDWARE = (
        "drawer_01_runner_left_fixed",
        "drawer_01_runner_right_fixed",
        "drawer_01_spacer_left",
        "drawer_01_spacer_right",
    )

    def setup_method(self) -> None:
        self.support = HettichKa4532InstalledGeometryTestSupport()
        self.source = self.support.source
        self.parts = self.support.parts
        self.checker = HettichKa4532SpacerInstalledFixingChecker()

    def test_accepts_exact_installed_relationship(self) -> None:
        assert self._height(self.parts) == 23.0

    @pytest.mark.parametrize(
        ("x_mm", "y_mm", "z_mm"),
        (
            (1000.0, 0.0, 0.0),
            (0.0, 1000.0, 0.0),
            (0.0, 0.0, 1000.0),
        ),
    )
    def test_rejects_coordinated_static_hardware_shift(
        self, x_mm: float, y_mm: float, z_mm: float
    ) -> None:
        shifted = self.support.shifted_parts(
            self._STATIC_HARDWARE,
            x_mm=x_mm,
            y_mm=y_mm,
            z_mm=z_mm,
        )

        assert self._height(shifted) is None

    def test_rejects_right_spacer_with_same_envelope_but_wrong_hand(self) -> None:
        wrong_hand = dict(self.parts)
        part = wrong_hand["drawer_01_spacer_right"]
        wrong_hand[part.name] = replace(
            part,
            location=cq.Location(cq.Vector(72.0, 10.0, -2.0)),
        )

        assert self._height(wrong_hand) is None

    def test_rejects_right_spacer_and_rail_placed_outside_cabinet(self) -> None:
        outside = dict(self.parts)
        spacer = outside["drawer_01_spacer_right"]
        runner = outside["drawer_01_runner_right_fixed"]
        outside[spacer.name] = replace(
            spacer,
            location=cq.Location(cq.Vector(97.0, 10.0, -2.0)),
        )
        outside[runner.name] = replace(
            runner,
            location=cq.Location(cq.Vector(120.0, 11.5, 23.0)),
        )

        assert self._height(outside) is None

    def test_rejects_fixed_rail_tilted_around_hole_centres(self) -> None:
        tilted = dict(self.parts)
        part = tilted["drawer_01_runner_left_fixed"]
        tilted[part.name] = replace(
            part,
            location=self.support.tilted_location((25.0, 11.5, 23.0)),
        )

        assert self._height(tilted) is None

    @pytest.mark.parametrize(
        "part_name",
        ("drawer_01_runner_left_fixed", "drawer_01_spacer_right"),
    )
    def test_rejects_broken_rail_spacer_interface(self, part_name: str) -> None:
        shifted = self.support.shifted_parts((part_name,), x_mm=1.0)

        assert self._height(shifted) is None

    def _height(self, parts: dict) -> float | None:
        return self.checker.axis_height("drawer_01", parts, self.source)


__all__ = ["TestHettichKa4532SpacerInstalledFixingChecker"]
