"""Scope: Verify System 32 nodes and real hardware envelopes share one plan."""

from __future__ import annotations

from dataclasses import dataclass
import unittest

from door_hinge_side import DoorHingeSide
from hettich_ka_5332_hardware_reservations import (
    HettichKa5332HardwareReservations,
)
from hettich_ka_5332_runner_profile import HETTICH_KA_5332_500
from hettich_ka_5332_system_32_row_resolver import (
    HettichKa5332System32RowResolver,
)
from riex_nc70_hardware_reservations import RiexNc70HardwareReservations
from riex_nc70_hinge_profile import RIEX_NC70_FULL_OVERLAY
from system_32_hinge_placement_resolver import System32HingePlacementResolver


@dataclass(frozen=True)
class _Part:
    part_id: str
    role: str
    dimensions_mm: tuple[tuple[str, float], ...]
    local_size_mm: tuple[float, float, float] = ()


class _Assembly:
    assembly_id = "cabinet_01"
    base_height_mm = 0.0
    door_bottom_mm = 0.0

    def __init__(self) -> None:
        self.parts = (
            _Part(
                "door_panel",
                "door_panel",
                (("width", 500.0), ("left_height", 1000.0),
                 ("right_height", 1000.0), ("thickness", 18.0)),
            ),
            _Part(
                "left_side",
                "side_panel",
                (("height", 1000.0), ("depth", 582.0), ("thickness", 18.0)),
                (582.0, 1000.0, 18.0),
            ),
            _Part(
                "right_side",
                "side_panel",
                (("height", 1000.0), ("depth", 582.0), ("thickness", 18.0)),
                (582.0, 1000.0, 18.0),
            ),
        )

    def part(self, part_id: str) -> _Part:
        return next(part for part in self.parts if part.part_id == part_id)


class TestPanelHardwareReservations(unittest.TestCase):
    """Protect the distinction between node occupancy and physical overlap."""

    def test_one_runner_uses_one_node_per_side_and_a_46_mm_band(self) -> None:
        reservations = HettichKa5332HardwareReservations().build(
            "drawer_01", 388.0, HETTICH_KA_5332_500
        )

        self.assertEqual(reservations[0].system_32_node_rows_mm, (388.0,))
        self.assertEqual(reservations[0].height_interval_mm, (365.0, 411.0))
        self.assertEqual(reservations[0].depth_interval_mm, (2.0, 502.0))

    def test_adjacent_hinge_pair_conflicts_without_sharing_a_node(self) -> None:
        self.assertEqual(RIEX_NC70_FULL_OVERLAY.plate_height_mm, 52.0)
        self.assertEqual(RIEX_NC70_FULL_OVERLAY.plate_depth_interval_from_front_mm, (19.576999, 63.576999))
        runner = HettichKa5332HardwareReservations().build(
            "drawer_01", 388.0, HETTICH_KA_5332_500
        )[0]
        hinge = RiexNc70HardwareReservations().for_position(
            "hinge_01",
            DoorHingeSide.LEFT,
            (420.0, 452.0),
            436.0,
            RIEX_NC70_FULL_OVERLAY,
        )

        self.assertFalse(
            set(runner.system_32_node_rows_mm)
            & set(hinge.system_32_node_rows_mm)
        )
        self.assertTrue(runner.conflicts_with(hinge))

    def test_drawer_row_moves_to_avoid_an_existing_hinge_plate(self) -> None:
        hinge = RiexNc70HardwareReservations().for_position(
            "hinge_01",
            DoorHingeSide.LEFT,
            (420.0, 452.0),
            436.0,
            RIEX_NC70_FULL_OVERLAY,
        )

        row_mm = HettichKa5332System32RowResolver().resolve(
            _Assembly(),
            "drawer_01",
            356.0,
            HETTICH_KA_5332_500,
            (hinge,),
        )

        self.assertEqual(row_mm, 356.0)

    def test_hinge_resolver_skips_runner_node_and_adjacent_overlap(self) -> None:
        runner = HettichKa5332HardwareReservations().build(
            "drawer_01", 100.0, HETTICH_KA_5332_500
        )[0]

        placements = System32HingePlacementResolver().resolve(
            _Assembly(),
            2,
            DoorHingeSide.LEFT,
            RIEX_NC70_FULL_OVERLAY,
            (runner,),
        )

        self.assertEqual(placements[0].cabinet_fixing_rows_mm, (164.0, 196.0))

    def test_hinge_resolver_treats_a_shelf_as_physical_panel_space(self) -> None:
        assembly = _Assembly()
        assembly.parts += (
            _Part(
                "shelf_01",
                "shelf_panel",
                (("bottom_height", 100.0), ("thickness", 18.0),
                 ("assembly_y", 0.0), ("depth", 582.0)),
            ),
        )

        placements = System32HingePlacementResolver().resolve(assembly, 2)

        self.assertEqual(placements[0].cabinet_fixing_rows_mm, (132.0, 164.0))


if __name__ == "__main__":
    unittest.main()
