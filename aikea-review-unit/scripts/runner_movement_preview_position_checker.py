"""Scope: Prove runner preview parts preserve known drawer motion relationships."""

from __future__ import annotations

from typing import Any

from drawer_review_motion import DrawerReviewMotion
from drawer_review_state import DrawerReviewState
from runner_movement_preview_report import RunnerMovementPreviewReport


class RunnerMovementPreviewPositionChecker:
    """Compare closed and open frames for both runner hands and drawer locks."""

    _TOLERANCE_MM = 1e-6

    def __init__(self) -> None:
        self.review_motion = DrawerReviewMotion()

    def check(
        self,
        built_cabinet: Any,
        closed_parts: tuple[Any, ...],
        open_parts: tuple[Any, ...],
    ) -> RunnerMovementPreviewReport:
        child = next(
            item
            for item in built_cabinet.child_assemblies
            if item.spec.purpose == "drawer"
        )
        expected = self._expected_travel(child)
        closed = {part.name: part for part in closed_parts}
        opened = {part.name: part for part in open_parts}
        relationships = tuple(
            self._hand_relationship(child.spec.assembly_id, hand, closed, opened)
            for hand in ("left", "right")
        )
        checks = tuple(
            check
            for relation in relationships
            for check in self._checks(relation, expected)
        )
        return RunnerMovementPreviewReport(expected, relationships, checks)

    def _expected_travel(self, child: Any) -> tuple[float, float, float]:
        extension = self.review_motion.extension_mm(
            DrawerReviewState.OPEN,
            child.assembly.spec.box.side_length_mm,
        )
        direction = child.spec.local_to_parent.axis_basis.local_y_in_parent
        return self._rounded(
            (
                -extension * direction.x,
                -extension * direction.y,
                -extension * direction.z,
            )
        )

    def _hand_relationship(self, drawer_id, hand, closed, opened):
        fixed = f"review_only__runner_{hand}__fixed_path"
        drawer_guide = f"review_only__runner_{hand}__drawer_side_guide"
        lock = f"{drawer_id}__locking_device_{hand}__source_cad"
        return {
            "hand": hand,
            "fixed_path_travel_mm": self._travel(closed[fixed], opened[fixed]),
            "drawer_side_guide_travel_mm": self._travel(
                closed[drawer_guide], opened[drawer_guide]
            ),
            "locking_device_travel_mm": self._travel(closed[lock], opened[lock]),
            "guide_to_lock_closed": self._relative_frame(
                closed[drawer_guide], closed[lock]
            ),
            "guide_to_lock_open": self._relative_frame(
                opened[drawer_guide], opened[lock]
            ),
        }

    def _checks(self, relation, expected):
        hand = relation["hand"]
        return (
            {
                "name": f"{hand} fixed runner path stays in the cabinet",
                "passed": self._matches(
                    relation["fixed_path_travel_mm"], (0.0, 0.0, 0.0)
                ),
            },
            {
                "name": f"{hand} drawer-side guide matches drawer travel",
                "passed": self._matches(
                    relation["drawer_side_guide_travel_mm"], expected
                ),
            },
            {
                "name": f"{hand} locking device matches drawer travel",
                "passed": self._matches(relation["locking_device_travel_mm"], expected),
            },
            {
                "name": f"{hand} locking device stays fixed to its drawer-side guide",
                "passed": self._matches(
                    relation["guide_to_lock_closed"],
                    relation["guide_to_lock_open"],
                ),
            },
        )

    def _travel(self, closed: Any, opened: Any) -> tuple[float, float, float]:
        closed_origin = closed.location.toTuple()[0]
        opened_origin = opened.location.toTuple()[0]
        return self._rounded(
            tuple(end - start for start, end in zip(closed_origin, opened_origin))
        )

    def _relative_frame(self, follower: Any, lock: Any) -> tuple[float, ...]:
        origin, rotation = (follower.location.inverse * lock.location).toTuple()
        return self._rounded((*origin, *rotation))

    def _matches(self, left, right) -> bool:
        return all(abs(a - b) <= self._TOLERANCE_MM for a, b in zip(left, right))

    def _rounded(self, values) -> tuple[float, ...]:
        rounded = tuple(round(float(value), 6) for value in values)
        return tuple(
            0.0 if abs(value) <= self._TOLERANCE_MM else value
            for value in rounded
        )


__all__ = ["RunnerMovementPreviewPositionChecker"]
