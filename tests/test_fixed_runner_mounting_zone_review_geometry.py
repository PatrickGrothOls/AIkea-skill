"""Scope: Verify the visible guide for unresolved fixed runner placement."""

from importlib.util import find_spec
from types import SimpleNamespace
import unittest

from drawer_box_planner import DrawerBoxPlanner
from drawer_box_spec import CabinetDrawerOpening, DrawerBoxSizingProfile


@unittest.skipUnless(find_spec("cadquery"), "requires CadQuery")
class TestFixedRunnerMountingZoneReviewGeometry(unittest.TestCase):
    """Protect guide names, length, and cabinet-fixed placement."""

    def test_builds_two_labeled_500_mm_display_bands(self) -> None:
        from fixed_runner_mounting_zone_review_geometry import (
            FixedRunnerMountingZoneReviewGeometry,
        )

        geometry = FixedRunnerMountingZoneReviewGeometry().build(self._cabinet())

        self.assertEqual(
            [part.name for part in geometry],
            [
                "review_only__runner_left__760h5000s_mounting_zone",
                "review_only__runner_right__760h5000s_mounting_zone",
            ],
        )
        for part in geometry:
            bounds = part.placed_shape().BoundingBox()
            self.assertAlmostEqual(bounds.ylen, 500.0)
            self.assertAlmostEqual(bounds.xlen, 12.0)
            self.assertAlmostEqual(bounds.zlen, 24.0)
        self.assertAlmostEqual(geometry[0].placed_shape().BoundingBox().xmin, 18.0)
        self.assertAlmostEqual(geometry[1].placed_shape().BoundingBox().xmax, 725.0)

    def _cabinet(self):
        box = DrawerBoxPlanner().plan(
            CabinetDrawerOpening(707.0, 564.0),
            DrawerBoxSizingProfile(runner_length_mm=500.0),
        )
        child = SimpleNamespace(
            spec=SimpleNamespace(
                purpose="drawer",
                local_to_parent=self._placement(),
            ),
            assembly=SimpleNamespace(
                spec=SimpleNamespace(
                    box=box,
                    runner_product_code="760H5000S",
                )
            ),
        )
        runners = tuple(
            SimpleNamespace(
                spec=SimpleNamespace(
                    hardware_id=hardware_id,
                    product_code="760H5000S",
                ),
                has_geometry=False,
            )
            for hardware_id in ("runner_left", "runner_right")
        )
        return SimpleNamespace(
            child_assemblies=(child,),
            purchased_hardware=runners,
        )

    def _placement(self):
        return SimpleNamespace(
            origin_in_parent=SimpleNamespace(x_mm=24.0, y_mm=18.0, z_mm=456.0),
            axis_basis=SimpleNamespace(
                local_x_in_parent=self._direction(1.0, 0.0, 0.0),
                local_y_in_parent=self._direction(0.0, 1.0, 0.0),
                local_z_in_parent=self._direction(0.0, 0.0, 1.0),
            ),
        )

    def _direction(self, x: float, y: float, z: float):
        return SimpleNamespace(x=x, y=y, z=z)


if __name__ == "__main__":
    unittest.main()
