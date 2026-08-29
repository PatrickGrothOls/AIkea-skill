"""Scope: Supply deterministic visual hardware doubles to review unit tests."""

from __future__ import annotations

import json
from pathlib import Path

from drawer_review_state import DrawerReviewState


class DrawerHardwarePositionReportTestDouble:
    """Behave like one already-passed exact position report."""

    is_valid = True

    def write(self, path: Path) -> None:
        path.write_text(json.dumps({"status": "valid"}) + "\n", encoding="utf-8")

    def failed_check_names(self) -> list[str]:
        return []


class RunnerMovementPreviewReportTestDouble:
    """Behave like one already-passed review-only movement report."""

    is_valid = True

    def write(self, path: Path) -> None:
        payload = {
            "status": "valid",
            "representation": "review_only_runner_movement",
            "manufacturing_authority": False,
        }
        path.write_text(json.dumps(payload) + "\n", encoding="utf-8")

    def failed_check_names(self) -> list[str]:
        return []


class DrawerHardwareReviewBuilderTestDouble:
    """Create named test solids without reading manufacturer CAD files."""

    def build(
        self,
        built_cabinet,
        cabinet_parts,
        drawer_parts,
        hardware_directory,
        state: DrawerReviewState,
    ) -> DrawerHardwareReview:
        import cadquery as cq

        from drawer_hardware_review import DrawerHardwareReview
        from unit_mockup import MockupPart

        solid = cq.Workplane("XY").box(1.0, 1.0, 1.0)
        location = cq.Location(cq.Vector(100.0, 100.0, 500.0))
        exact_runners = tuple(
            MockupPart(
                f"runner_{hand}__source_cad",
                solid,
                location,
                (0.2, 0.2, 0.2, 1.0),
            )
            for hand in ("left", "right")
        )
        preview_parts = tuple(
            MockupPart(
                f"review_only__runner_{hand}__{part}",
                solid,
                location,
                (0.3, 0.3, 0.3, 1.0),
            )
            for hand in ("left", "right")
            for part in ("fixed_path", "drawer_side_guide")
        )
        locks = tuple(
            MockupPart(
                f"drawer_01__locking_device_{hand}__source_cad",
                solid,
                location,
                (0.8, 0.4, 0.1, 1.0),
            )
            for hand in ("left", "right")
        )
        closed_parts = exact_runners + locks
        review_parts = {
            DrawerReviewState.CLOSED: closed_parts,
            DrawerReviewState.OPEN: preview_parts + locks,
            DrawerReviewState.REMOVED: exact_runners,
        }[state]
        return DrawerHardwareReview(
            closed_parts=closed_parts,
            review_parts=review_parts,
            position_report=DrawerHardwarePositionReportTestDouble(),
            movement_report=RunnerMovementPreviewReportTestDouble(),
        )


__all__ = ["DrawerHardwareReviewBuilderTestDouble"]
