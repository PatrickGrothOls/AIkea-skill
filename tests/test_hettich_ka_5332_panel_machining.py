"""Scope: Verify exact KA 5332 cabinet and drawer holes in local part frames."""

from __future__ import annotations

from dataclasses import dataclass
import unittest

import cadquery as cq

from hettich_ka_5332_panel_machining import HettichKa5332PanelMachining
from hettich_ka_5332_runner_profile import HETTICH_KA_5332_500


@dataclass(frozen=True)
class _Spec:
    part_id: str
    local_size_mm: tuple[float, float, float]


@dataclass(frozen=True)
class _BuiltPart:
    spec: _Spec
    solid: cq.Workplane


@dataclass(frozen=True)
class _BuiltBox:
    parts: tuple[_BuiltPart, ...]


class TestHettichKa5332PanelMachining(unittest.TestCase):
    """Prove both handed panels receive blind manufacturer-positioned holes."""

    def setUp(self) -> None:
        self.machining = HettichKa5332PanelMachining()

    def test_profile_owns_both_official_500_mm_fixing_patterns(self) -> None:
        self.assertEqual(
            HETTICH_KA_5332_500.cabinet_fixing_positions_from_front_mm,
            (37.0, 128.0, 224.0, 352.0, 416.0),
        )
        self.assertEqual(
            HETTICH_KA_5332_500.drawer_fixing_positions_from_front_mm,
            (37.0, 128.0, 192.0, 352.0, 442.0),
        )

    def test_cabinet_holes_are_mirrored_and_remain_blind(self) -> None:
        left = self._part("left_side", (582.0, 800.0, 18.0))
        right = self._part("right_side", (582.0, 800.0, 18.0))
        machined = self.machining.cabinet_parts((left, right), (388.0,))

        self._assert_hole(machined[0].solid, 128.0, 388.0, 17.0, 1.0)
        self._assert_hole(machined[1].solid, 582.0 - 128.0, 388.0, 17.0, 1.0)

    def test_drawer_holes_follow_each_side_from_the_drawer_front(self) -> None:
        left = self._part("left_side", (490.0, 160.0, 15.0))
        right = self._part("right_side", (490.0, 160.0, 15.0))
        box = _BuiltBox((left, right))

        machined = self.machining.drawer_box(box)

        self._assert_hole(machined.parts[0].solid, 490.0 - 128.0, 23.0, 14.0, 1.0)
        self._assert_hole(machined.parts[1].solid, 128.0, 23.0, 14.0, 1.0)

    def _part(self, part_id: str, size_mm: tuple[float, float, float]) -> _BuiltPart:
        return _BuiltPart(_Spec(part_id, size_mm), cq.Workplane("XY").box(*size_mm, centered=False))

    def _assert_hole(
        self,
        solid: cq.Workplane,
        x_mm: float,
        y_mm: float,
        open_z_mm: float,
        blind_z_mm: float,
    ) -> None:
        self.assertFalse(solid.val().isInside(cq.Vector(x_mm, y_mm, open_z_mm)))
        self.assertTrue(solid.val().isInside(cq.Vector(x_mm, y_mm, blind_z_mm)))


if __name__ == "__main__":
    unittest.main()
