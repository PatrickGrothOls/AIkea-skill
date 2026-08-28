"""Scope: Verify the drawer review command accepts every supported visual state."""

from pathlib import Path
import unittest

from generate_drawer_wardrobe_review import GenerateDrawerWardrobeReviewCommand


class TestDrawerReviewCli(unittest.TestCase):
    """Keep command choices aligned with the reusable drawer state contract."""

    def test_accepts_removed_drawer_state(self) -> None:
        arguments = GenerateDrawerWardrobeReviewCommand.parser().parse_args(
            [
                "project/aikea.yaml",
                "--assembly",
                "tall_storage_01",
                "--drawer-state",
                "removed",
            ]
        )

        self.assertEqual(arguments.aikea_yaml, Path("project/aikea.yaml"))
        self.assertEqual(arguments.drawer_state, "removed")

    def test_defaults_to_open_drawer_state(self) -> None:
        arguments = GenerateDrawerWardrobeReviewCommand.parser().parse_args(
            ["project/aikea.yaml", "--assembly", "tall_storage_01"]
        )

        self.assertEqual(arguments.drawer_state, "open")


if __name__ == "__main__":
    unittest.main()
