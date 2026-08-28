"""Scope: Verify drawer review motion respects every declared child axis."""

from __future__ import annotations

from importlib.util import find_spec
from types import SimpleNamespace
import unittest

from drawer_assembly_spec import DrawerAssemblySpec
from drawer_box_planner import DrawerBoxPlanner
from drawer_box_spec import CabinetDrawerOpening, DrawerBoxSizingProfile
from drawer_review_state import DrawerReviewState


@unittest.skipUnless(find_spec("cadquery"), "requires CadQuery")
class TestDrawerReviewFrames(unittest.TestCase):
    """Use a rotated child to expose transform-order and handedness errors."""

    def test_open_pose_moves_along_the_drawer_local_opening_axis(self) -> None:
        from drawer_box_builder import DrawerBoxBuilder
        from drawer_review_geometry import DrawerReviewGeometry

        box = DrawerBoxPlanner().plan(
            CabinetDrawerOpening(707.0, 564.0),
            DrawerBoxSizingProfile(runner_length_mm=500.0),
        )
        built_box = DrawerBoxBuilder().build(box)
        drawer_spec = DrawerAssemblySpec(
            "drawer_01",
            "drawer",
            "760H5000S",
            "05083446",
            "source_cad_verification_required",
            box,
        )
        child = SimpleNamespace(
            spec=SimpleNamespace(
                assembly_id="drawer_01",
                purpose="drawer",
                local_to_parent=self._placement(
                    x_axis=(0.0, 1.0, 0.0),
                    y_axis=(-1.0, 0.0, 0.0),
                    z_axis=(0.0, 0.0, 1.0),
                ),
            ),
            assembly=SimpleNamespace(spec=drawer_spec, parts=built_box.parts),
        )
        cabinet = SimpleNamespace(child_assemblies=(child,))
        geometry = DrawerReviewGeometry()

        closed = geometry.build(cabinet, DrawerReviewState.CLOSED)[0]
        opened = geometry.build(cabinet, DrawerReviewState.OPEN)[0]
        removed = geometry.build(cabinet, DrawerReviewState.REMOVED)
        closed_center = closed.placed_shape().Center()
        opened_center = opened.placed_shape().Center()

        self.assertAlmostEqual(opened_center.x - closed_center.x, 367.5)
        self.assertAlmostEqual(opened_center.y - closed_center.y, 0.0)
        self.assertAlmostEqual(opened_center.z - closed_center.z, 0.0)
        self.assertEqual(removed, ())

    def _placement(self, x_axis, y_axis, z_axis):
        return SimpleNamespace(
            origin_in_parent=SimpleNamespace(x_mm=100.0, y_mm=200.0, z_mm=300.0),
            axis_basis=SimpleNamespace(
                local_x_in_parent=self._direction(x_axis),
                local_y_in_parent=self._direction(y_axis),
                local_z_in_parent=self._direction(z_axis),
            ),
        )

    def _direction(self, values):
        return SimpleNamespace(x=values[0], y=values[1], z=values[2])
