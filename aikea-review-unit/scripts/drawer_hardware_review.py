"""Scope: Verify and prepare one exact mounted drawer-hardware review."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from drawer_hardware_position_checker import DrawerHardwarePositionChecker
from drawer_hardware_review_geometry import DrawerHardwareReviewGeometry
from drawer_hardware_set_verifier import DrawerHardwareSetVerifierFactory
from drawer_review_state import DrawerReviewState
from movento_runner_catalog import MOVENTO_RUNNER_CATALOG
from runner_movement_preview_geometry import RunnerMovementPreviewGeometry
from runner_movement_preview_position_checker import (
    RunnerMovementPreviewPositionChecker,
)
from unit_mockup import MockupPart, UnitMockupInputError


@dataclass(frozen=True, slots=True)
class DrawerHardwareReview:
    """Carry checked closed hardware and the selected presentation pose."""

    closed_parts: tuple[MockupPart, ...]
    review_parts: tuple[MockupPart, ...]
    position_report: Any
    movement_report: Any


class DrawerHardwareReviewBuilder:
    """Verify source CAD, place it, and check its closed mounting frame."""

    def __init__(
        self,
        verifier_factory: DrawerHardwareSetVerifierFactory | None = None,
    ) -> None:
        self.verifier_factory = verifier_factory or DrawerHardwareSetVerifierFactory()
        self.geometry = DrawerHardwareReviewGeometry()
        self.movement_preview = RunnerMovementPreviewGeometry()
        self.movement_checker = RunnerMovementPreviewPositionChecker()
        self.position_checker = DrawerHardwarePositionChecker()

    def build(
        self,
        built_cabinet: Any,
        cabinet_parts: tuple[MockupPart, ...],
        drawer_parts: tuple[MockupPart, ...],
        hardware_directory: Path,
        state: DrawerReviewState,
    ) -> DrawerHardwareReview:
        runner = self._runner_for(built_cabinet)
        hardware = self.verifier_factory.create(hardware_directory).verify(runner)
        closed_parts = self.geometry.build(
            built_cabinet,
            hardware,
            DrawerReviewState.CLOSED,
        )
        preview_closed = self._movement_parts(
            built_cabinet,
            hardware,
            runner,
            DrawerReviewState.CLOSED,
        )
        preview_open = self._movement_parts(
            built_cabinet,
            hardware,
            runner,
            DrawerReviewState.OPEN,
        )
        return DrawerHardwareReview(
            closed_parts=closed_parts,
            review_parts=(
                preview_open
                if state is DrawerReviewState.OPEN
                else self.geometry.build(built_cabinet, hardware, state)
            ),
            position_report=self.position_checker.check(
                built_cabinet,
                cabinet_parts,
                drawer_parts,
                hardware,
            ),
            movement_report=self.movement_checker.check(
                built_cabinet,
                preview_closed,
                preview_open,
            ),
        )

    def _movement_parts(self, built_cabinet, hardware, runner, state):
        child = next(
            item
            for item in built_cabinet.child_assemblies
            if item.spec.purpose == "drawer"
        )
        return self.movement_preview.build(built_cabinet, runner, state) + (
            self.geometry.build_locks(child, hardware, state)
        )

    def _runner_for(self, built_cabinet: Any) -> Any:
        child = next(
            item
            for item in built_cabinet.child_assemblies
            if item.spec.purpose == "drawer"
        )
        product_code = child.assembly.spec.runner_product_code
        try:
            return next(
                runner
                for runner in MOVENTO_RUNNER_CATALOG.profiles
                if runner.product_code == product_code
            )
        except StopIteration as error:
            raise UnitMockupInputError(
                [f"drawer uses an unregistered runner: {product_code}"]
            ) from error


__all__ = ["DrawerHardwareReview", "DrawerHardwareReviewBuilder"]
