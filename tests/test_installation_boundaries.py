"""Scope: Verify the global brief preserves individual room boundaries."""

import unittest

from fitted_dimensions import FittedDimensions
from installation_boundaries import InstallationBoundaryReader


class TestInstallationBoundaries(unittest.TestCase):
    def test_existing_project_derives_boundaries_from_fitted_dimensions(self) -> None:
        problems: list[str] = []

        result = InstallationBoundaryReader().read(
            {},
            FittedDimensions(width=True, depth=False, height=True),
            problems,
        )

        self.assertEqual((result.left, result.right, result.top), (True, True, True))
        self.assertEqual(problems, [])

    def test_one_fixed_side_is_preserved_without_marking_width_fitted(self) -> None:
        data = {
            "design_settings": {
                "installation_boundaries": {
                    "left": True,
                    "right": False,
                    "top": True,
                }
            }
        }
        problems: list[str] = []

        result = InstallationBoundaryReader().read(
            data,
            FittedDimensions(width=False, depth=False, height=True),
            problems,
        )

        self.assertEqual((result.left, result.right, result.top), (True, False, True))
        self.assertEqual(problems, [])

    def test_individual_boundaries_must_agree_with_fitted_dimensions(self) -> None:
        data = {
            "design_settings": {
                "installation_boundaries": {
                    "left": True,
                    "right": False,
                    "top": False,
                }
            }
        }
        problems: list[str] = []

        InstallationBoundaryReader().read(
            data,
            FittedDimensions(width=True, depth=False, height=True),
            problems,
        )

        self.assertEqual(len(problems), 2)
        self.assertIn("both left and right", problems[0])
        self.assertIn("top boundary", problems[1])


if __name__ == "__main__":
    unittest.main()
