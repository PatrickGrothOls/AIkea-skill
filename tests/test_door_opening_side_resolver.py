"""Scope: Verify standard and client-selected single-door hinge hands."""

from __future__ import annotations

from dataclasses import dataclass
import unittest

from door_hinge_side import DoorHingeSide
from door_opening_side_resolver import DoorOpeningSideResolver


@dataclass(frozen=True, slots=True)
class _Assembly:
    assembly_id: str = "tall_storage_01"


class TestDoorOpeningSideResolver(unittest.TestCase):
    def setUp(self) -> None:
        self.resolver = DoorOpeningSideResolver()
        self.assembly = _Assembly()

    def test_single_door_uses_left_hinge_by_default(self) -> None:
        result = self.resolver.resolve(self.assembly)

        self.assertIs(result.proposed_side, DoorHingeSide.LEFT)
        self.assertEqual(result.selection_source, "standard")
        self.assertFalse(result.changes_default)

    def test_explicit_client_choice_changes_the_hinge_side(self) -> None:
        result = self.resolver.resolve(self.assembly, DoorHingeSide.RIGHT)

        self.assertIs(result.proposed_side, DoorHingeSide.RIGHT)
        self.assertEqual(result.selection_source, "client_choice")
        self.assertTrue(result.changes_default)


if __name__ == "__main__":
    unittest.main()
