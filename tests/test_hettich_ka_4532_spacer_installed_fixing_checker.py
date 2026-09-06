"""Scope: Reject corrupted installed KA 4532 rail and spacer geometry."""

from dataclasses import replace

import cadquery as cq
import pytest

from hettich_ka_4532_spacer_installed_fixing_checker import (
    HettichKa4532SpacerInstalledFixingChecker,
)
from hettich_ka_4532_spacer_proof_test_support import (
    HettichKa4532SpacerProofTestSupport,
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
        support = HettichKa4532SpacerProofTestSupport()
        self.source = support.source()
        self.parts = {part.name: part for part in support.parts(0.0, self.source)}
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
        shifted = self._shifted_parts(
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
            location=self._tilted_location((25.0, 11.5, 23.0)),
        )

        assert self._height(tilted) is None

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
        shifted = self._shifted_parts((part_name,), x_mm=x_mm, y_mm=y_mm)

        assert self._height(shifted) is None

    def test_rejects_front_and_rails_shifted_without_drawer_box(self) -> None:
        shifted = self._shifted_parts(
            (
                "drawer_01__front",
                "drawer_01__drawer_01_runner_left_moving",
                "drawer_01__drawer_01_runner_right_moving",
            ),
            y_mm=1.0,
        )

        assert self._height(shifted) is None

    def test_accepts_valid_complete_drawer_front_inset(self) -> None:
        drawer_names = tuple(
            name for name in self.parts if name.startswith("drawer_01__")
        )
        inset = self._shifted_parts(drawer_names, y_mm=20.0)

        assert self._height(inset) == 23.0

    def test_rejects_rotated_moving_member(self) -> None:
        rotated = dict(self.parts)
        part = rotated["drawer_01__drawer_01_runner_left_moving"]
        rotated[part.name] = replace(
            part,
            location=self._tilted_location((25.0, 0.0, 22.0)),
        )

        assert self._height(rotated) is None

    @pytest.mark.parametrize(
        "part_name",
        ("drawer_01_runner_left_fixed", "drawer_01_spacer_right"),
    )
    def test_rejects_broken_rail_spacer_interface(self, part_name: str) -> None:
        shifted = self._shifted_parts((part_name,), x_mm=1.0)

        assert self._height(shifted) is None

    def _height(self, parts: dict) -> float | None:
        return self.checker.axis_height("drawer_01", parts, self.source)

    def _shifted_parts(
        self,
        names: tuple[str, ...],
        *,
        x_mm: float = 0.0,
        y_mm: float = 0.0,
        z_mm: float = 0.0,
    ) -> dict:
        shifted = dict(self.parts)
        translation = cq.Location(cq.Vector(x_mm, y_mm, z_mm))
        for name in names:
            part = shifted[name]
            shifted[name] = replace(part, location=translation * part.location)
        return shifted

    def _tilted_location(self, origin: tuple[float, ...]):
        return cq.Location(
            cq.Plane(
                origin=origin,
                xDir=(0.984807753, 0.0, -0.173648178),
                normal=(0.173648178, 0.0, 0.984807753),
            )
        )


__all__ = ["TestHettichKa4532SpacerInstalledFixingChecker"]
