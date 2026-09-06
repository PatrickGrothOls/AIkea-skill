"""Scope: Verify rigid KA 4532 drawer travel between two exact tree states."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class HettichKa4532SpacerMotionEvidence:
    """Carry serializable movement and its independent checks."""

    movement: dict[str, Any]
    checks: tuple[dict[str, Any], ...]


class HettichKa4532SpacerMotionChecker:
    """Require the complete drawer subtree to move while its cabinet stays fixed."""

    _TOLERANCE_MM = 1e-6

    def check(
        self,
        drawer_id: str,
        extension_mm: float,
        closed: dict[str, Any],
        opened: dict[str, Any],
        moving_names: tuple[str, ...],
        static_names: tuple[str, ...],
    ) -> HettichKa4532SpacerMotionEvidence:
        expected = (0.0, -extension_mm, 0.0)
        moving_travel = {
            name: list(self._travel(closed[name], opened[name])) for name in moving_names
        }
        static_travel = {
            name: list(self._travel(closed[name], opened[name])) for name in static_names
        }
        checks = (
            self._check(
                "closed and open contain the same item names",
                closed.keys() == opened.keys(),
            ),
            self._check(
                "the complete generated drawer subtree is present",
                self._required_moving_names(drawer_id) <= set(moving_names),
            ),
            self._check(
                "the complete drawer subtree follows the declared linear travel",
                all(
                    self._matches(tuple(travel), expected)
                    for travel in moving_travel.values()
                ),
            ),
            self._check(
                "cabinet parts, fixed runners, and both spacers remain fixed",
                all(
                    self._matches(tuple(travel), (0.0, 0.0, 0.0))
                    for travel in static_travel.values()
                ),
            ),
            self._check(
                "motion preserves every placed volume and orientation",
                self._geometry_matches(closed, opened),
            ),
        )
        return HettichKa4532SpacerMotionEvidence(
            {
                "declared_travel_mm": list(expected),
                "moving_part_travel_mm": moving_travel,
                "static_part_travel_mm": static_travel,
            },
            checks,
        )

    def _travel(self, closed: Any, opened: Any) -> tuple[float, float, float]:
        start = closed.location.toTuple()[0]
        end = opened.location.toTuple()[0]
        return tuple(round(float(b - a), 6) for a, b in zip(start, end))

    def _geometry_matches(self, closed: dict[str, Any], opened: dict[str, Any]) -> bool:
        return all(
            abs(closed[name].placed_shape().Volume() - opened[name].placed_shape().Volume())
            <= self._TOLERANCE_MM
            and self._matches(
                tuple(float(value) for value in closed[name].location.toTuple()[1]),
                tuple(float(value) for value in opened[name].location.toTuple()[1]),
            )
            for name in closed
        )

    def _required_moving_names(self, drawer_id: str) -> set[str]:
        return {
            *(
                f"{drawer_id}__{part}"
                for part in ("left_side", "right_side", "front", "back", "bottom")
            ),
            f"{drawer_id}__{drawer_id}_runner_left_moving",
            f"{drawer_id}__{drawer_id}_runner_right_moving",
        }

    def _matches(self, left: tuple[float, ...], right: tuple[float, ...]) -> bool:
        return all(abs(a - b) <= self._TOLERANCE_MM for a, b in zip(left, right))

    def _check(self, name: str, passed: bool) -> dict[str, Any]:
        return {"name": name, "passed": passed}


__all__ = [
    "HettichKa4532SpacerMotionChecker",
    "HettichKa4532SpacerMotionEvidence",
]
