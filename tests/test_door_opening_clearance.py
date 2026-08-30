"""Scope: Verify door hands come from measured 90-degree opening clearance."""

from __future__ import annotations

import unittest

from door_hinge_side import DoorHingeSide
from door_opening_side_resolver import DoorOpeningSideResolver
from door_opening_test_case import DoorOpeningAssembly, DoorOpeningFixture
from riex_nc70_hinge_profile import RiexNc70HingeProfile


class TestDoorOpeningClearance(unittest.TestCase):
    def setUp(self) -> None:
        self.profile = RiexNc70HingeProfile()
        self.resolver = DoorOpeningSideResolver()
        self.fixture = DoorOpeningFixture()

    def test_ordinary_left_hinge_is_kept_when_it_clears_the_room(self) -> None:
        assembly = DoorOpeningAssembly(2280.0, 2280.0)
        inputs = self.fixture.flat_inputs(2400.0)

        result = self.resolver.resolve(inputs, assembly, self.profile)

        self.assertIs(result.proposed_side, DoorHingeSide.LEFT)
        self.assertFalse(result.changes_default)
        self.assertTrue(result.checks[0].passes)
        self.assertGreater(dict(result.checks[0].boundary_clearances_mm)["left"], 0)

    def test_right_hinge_is_used_only_when_rising_ceiling_blocks_left_sweep(self) -> None:
        assembly = DoorOpeningAssembly(1980.5, 2279.5)
        inputs = self.fixture.sloped_inputs(2000.0, 2500.0)

        result = self.resolver.resolve(inputs, assembly, self.profile)

        self.assertIs(result.proposed_side, DoorHingeSide.RIGHT)
        self.assertTrue(result.changes_default)
        self.assertIs(result.checks[0].hinge_side, DoorHingeSide.LEFT)
        self.assertFalse(result.checks[0].passes)
        self.assertTrue(result.checks[1].passes)

    def test_neither_side_is_proposed_when_the_closed_door_exceeds_the_room(self) -> None:
        assembly = DoorOpeningAssembly(2310.0, 2310.0)
        inputs = self.fixture.flat_inputs(2400.0)

        result = self.resolver.resolve(inputs, assembly, self.profile)

        self.assertIsNone(result.proposed_side)
        self.assertFalse(result.passes)
        self.assertTrue(all(check.passes is False for check in result.checks))

    def test_client_requested_right_hinge_is_rechecked_before_it_is_proposed(self) -> None:
        assembly = DoorOpeningAssembly(2280.0, 2280.0)
        inputs = self.fixture.flat_inputs(2400.0)

        result = self.resolver.resolve(
            inputs,
            assembly,
            self.profile,
            DoorHingeSide.RIGHT,
        )

        self.assertIs(result.proposed_side, DoorHingeSide.RIGHT)
        self.assertEqual(result.selection_source, "client_choice")
        self.assertTrue(result.checks[0].passes)

if __name__ == "__main__":
    unittest.main()
