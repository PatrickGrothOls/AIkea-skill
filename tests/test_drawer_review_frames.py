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
        from drawer_review_geometry import DrawerReviewGeometry

        cabinet = self._cabinet()
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

    def test_runner_follower_and_lock_share_the_rotated_drawer_travel(self) -> None:
        import cadquery as cq

        from drawer_hardware_review_geometry import DrawerHardwareReviewGeometry
        from movento_runner_catalog import MOVENTO_760H5000S
        from runner_movement_preview_geometry import RunnerMovementPreviewGeometry
        from runner_movement_preview_position_checker import (
            RunnerMovementPreviewPositionChecker,
        )

        cabinet = self._cabinet()
        child = cabinet.child_assemblies[0]
        step = SimpleNamespace(shape=cq.Workplane("XY").box(1.0, 1.0, 1.0).val())
        hardware = SimpleNamespace(
            locking_device_left=step,
            locking_device_right=step,
        )
        preview = RunnerMovementPreviewGeometry()
        exact = DrawerHardwareReviewGeometry()
        closed = preview.build(cabinet, MOVENTO_760H5000S, DrawerReviewState.CLOSED)
        closed += exact.build_locks(child, hardware, DrawerReviewState.CLOSED)
        opened = preview.build(cabinet, MOVENTO_760H5000S, DrawerReviewState.OPEN)
        opened += exact.build_locks(child, hardware, DrawerReviewState.OPEN)

        report = RunnerMovementPreviewPositionChecker().check(
            cabinet,
            closed,
            opened,
        )

        self.assertTrue(report.is_valid, report.failed_check_names())
        self.assertEqual(report.drawer_travel_mm, (367.5, 0.0, 0.0))
        self.assertFalse(report.as_dict()["manufacturing_authority"])

    def _cabinet(self):
        from drawer_box_builder import DrawerBoxBuilder

        box = DrawerBoxPlanner().plan(
            CabinetDrawerOpening(707.0, 564.0),
            DrawerBoxSizingProfile(runner_length_mm=500.0),
        )
        drawer_spec = DrawerAssemblySpec(
            "drawer_01",
            "drawer",
            "760H5000S",
            "05083446",
            "source_cad_verification_required",
            box,
        )
        child_frame = self._placement(
            x_axis=(0.0, 1.0, 0.0),
            y_axis=(-1.0, 0.0, 0.0),
            z_axis=(0.0, 0.0, 1.0),
        )
        hardware_frame = self._placement()
        locks = tuple(
            self._hardware(f"locking_device_{hand}", hardware_frame)
            for hand in ("left", "right")
        )
        child = SimpleNamespace(
            spec=SimpleNamespace(
                assembly_id="drawer_01",
                purpose="drawer",
                local_to_parent=child_frame,
            ),
            assembly=SimpleNamespace(
                spec=drawer_spec,
                parts=DrawerBoxBuilder().build(box).parts,
                purchased_hardware=locks,
            ),
        )
        runners = tuple(
            self._hardware(f"runner_{hand}", hardware_frame)
            for hand in ("left", "right")
        )
        return SimpleNamespace(
            child_assemblies=(child,),
            purchased_hardware=runners,
        )

    def _hardware(self, hardware_id, placement):
        return SimpleNamespace(
            spec=SimpleNamespace(
                hardware_id=hardware_id,
                local_to_parent=placement,
            )
        )

    def _placement(
        self,
        x_axis=(1.0, 0.0, 0.0),
        y_axis=(0.0, 0.0, 1.0),
        z_axis=(0.0, -1.0, 0.0),
    ):
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
