"""Scope: Place verified source-CAD drawer hardware in its saved owner frames."""

from __future__ import annotations

from typing import Any

import cadquery as cq

from drawer_hardware_set_verifier import VerifiedDrawerHardwareSet
from drawer_review_motion import DrawerReviewMotion
from drawer_review_state import DrawerReviewState
from local_to_parent_location import LocalToParentLocation
from unit_mockup import MockupPart, UnitMockupInputError


class DrawerHardwareReviewGeometry:
    """Keep fixed runners in the cabinet and locks with the moving drawer."""

    _RUNNER_COLOR = (0.20, 0.22, 0.24, 1.0)
    _LOCK_COLOR = (0.87, 0.42, 0.14, 1.0)

    def __init__(self) -> None:
        self.frame_location = LocalToParentLocation()
        self.review_motion = DrawerReviewMotion()

    def build(
        self,
        built_cabinet: Any,
        hardware: VerifiedDrawerHardwareSet,
        state: DrawerReviewState,
    ) -> tuple[MockupPart, ...]:
        child = self._drawer_child(built_cabinet)
        runners = self._hardware_by_id(built_cabinet.purchased_hardware)
        fixed = (
            self._part(
                "runner_left__source_cad",
                hardware.runner_left.shape,
                runners["runner_left"].spec.local_to_parent,
                self._RUNNER_COLOR,
            ),
            self._part(
                "runner_right__source_cad",
                hardware.runner_right.shape,
                runners["runner_right"].spec.local_to_parent,
                self._RUNNER_COLOR,
            ),
        )
        if state is DrawerReviewState.REMOVED:
            return fixed
        return fixed + self.build_locks(child, hardware, state)

    def build_locks(
        self,
        child: Any,
        hardware: VerifiedDrawerHardwareSet,
        state: DrawerReviewState,
    ) -> tuple[MockupPart, ...]:
        locks = self._hardware_by_id(child.assembly.purchased_hardware)
        child_frame = self.frame_location.build(child.spec.local_to_parent)
        motion = self.review_motion.location(
            state,
            child.assembly.spec.box.side_length_mm,
        )
        return tuple(
            MockupPart(
                f"{child.spec.assembly_id}__{hardware_id}__source_cad",
                cq.Workplane(obj=step.shape),
                child_frame
                * motion
                * self.frame_location.build(locks[hardware_id].spec.local_to_parent),
                self._LOCK_COLOR,
            )
            for hardware_id, step in (
                ("locking_device_left", hardware.locking_device_left),
                ("locking_device_right", hardware.locking_device_right),
            )
        )

    def _part(
        self,
        name: str,
        shape: Any,
        placement: Any,
        color: tuple[float, float, float, float],
    ) -> MockupPart:
        if placement is None:
            raise UnitMockupInputError([f"{name} is missing its saved mounting frame"])
        return MockupPart(
            name,
            cq.Workplane(obj=shape),
            self.frame_location.build(placement),
            color,
        )

    def _drawer_child(self, built_cabinet: Any) -> Any:
        drawers = tuple(
            child
            for child in built_cabinet.child_assemblies
            if child.spec.purpose == "drawer"
        )
        if len(drawers) != 1:
            raise UnitMockupInputError(
                ["source-CAD hardware review requires exactly one drawer child"]
            )
        return drawers[0]

    def _hardware_by_id(self, hardware: tuple[Any, ...]) -> dict[str, Any]:
        return {item.spec.hardware_id: item for item in hardware}


__all__ = ["DrawerHardwareReviewGeometry"]
