"""Scope: Check one exact KA 4532 spacer drawer through its full travel."""

from __future__ import annotations

from typing import Any

from hettich_ka_4532_spacer_collision_checker import (
    HettichKa4532SpacerCollisionChecker,
)
from hettich_ka_4532_spacer_proof_report import HettichKa4532SpacerProofReport


class HettichKa4532SpacerProofChecker:
    """Compare exact closed and open trees, including conservative sweep bounds."""

    _TOLERANCE_MM = 1e-6
    _MISSING_AUTHORITY = {
        "spacer_to_cabinet_fixing_hole_subset",
        "spacer_to_cabinet_fastener_identity",
        "cabinet_pilot_diameter_mm",
        "cabinet_pilot_depth_mm",
    }

    def __init__(self) -> None:
        self.collisions = HettichKa4532SpacerCollisionChecker()

    def check(
        self,
        assembly_id: str,
        drawer_id: str,
        extension_mm: float,
        closed_parts: tuple[Any, ...],
        open_parts: tuple[Any, ...],
        source_cad: dict[str, Any],
        artifacts: dict[str, Any],
        machining_blocker: dict[str, Any],
        reservations: tuple[dict[str, Any], ...],
    ) -> HettichKa4532SpacerProofReport:
        closed = self._parts_by_name(closed_parts)
        opened = self._parts_by_name(open_parts)
        moving_names = tuple(name for name in closed if name.startswith(f"{drawer_id}__"))
        static_names = tuple(name for name in closed if name not in moving_names)
        expected = (0.0, -extension_mm, 0.0)
        moving_travel = {
            name: list(self._travel(closed[name], opened[name])) for name in moving_names
        }
        static_travel = {
            name: list(self._travel(closed[name], opened[name])) for name in static_names
        }
        collision_evidence = self.collisions.check(
            drawer_id, closed, opened, moving_names, static_names
        )
        checks = (
            self._check(
                "closed and open contain the same item names",
                closed.keys() == opened.keys(),
            ),
            self._check(
                "the saved purchased set declares exact KA 4532 and two article 13952 spacers",
                source_cad["runner"]["item_number"] == "9114276"
                and source_cad["spacer"]["item_number"] == "13952"
                and source_cad["spacer"]["instances"] == 2,
            ),
            self._check(
                "the complete drawer subtree follows the declared linear travel",
                all(self._matches(tuple(travel), expected) for travel in moving_travel.values()),
            ),
            self._check(
                "cabinet parts, fixed runners, and both spacers remain fixed",
                all(self._matches(tuple(travel), (0.0, 0.0, 0.0)) for travel in static_travel.values()),
            ),
            self._check(
                "motion preserves every placed volume and orientation",
                self._geometry_matches(closed, opened),
            ),
            self._check(
                "both exact spacer instances preserve one source volume",
                self._spacer_volumes_match(closed, drawer_id),
            ),
            self._check(
                "closed endpoint has no unintended collision",
                not collision_evidence["closed_endpoint_pairs"],
            ),
            self._check(
                "open endpoint has no unintended collision",
                not collision_evidence["open_endpoint_pairs"],
            ),
            self._check(
                "linear swept envelopes have no unintended conflict",
                not collision_evidence["swept_envelope_pairs"],
            ),
            self._check(
                "both panel hardware reservations are saved",
                len(reservations) == 2
                and {item["side_part_id"] for item in reservations}
                == {"left_side", "right_side"},
            ),
            self._check(
                "unresolved spacer machining remains an explicit blocker",
                machining_blocker.get("manufacturing_authority") is False
                and set(machining_blocker.get("missing_authority", ()))
                == self._MISSING_AUTHORITY,
            ),
        )
        return HettichKa4532SpacerProofReport(
            assembly_id,
            drawer_id,
            source_cad,
            artifacts,
            machining_blocker,
            reservations,
            {
                "declared_travel_mm": list(expected),
                "moving_part_travel_mm": moving_travel,
                "static_part_travel_mm": static_travel,
            },
            collision_evidence,
            checks,
        )

    def _parts_by_name(self, parts: tuple[Any, ...]) -> dict[str, Any]:
        return {part.name: part for part in parts}

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

    def _spacer_volumes_match(self, parts: dict[str, Any], drawer_id: str) -> bool:
        volumes = tuple(
            parts[f"{drawer_id}_spacer_{hand}"].placed_shape().Volume()
            for hand in ("left", "right")
        )
        return abs(volumes[0] - volumes[1]) <= self._TOLERANCE_MM

    def _matches(self, left: tuple[float, ...], right: tuple[float, ...]) -> bool:
        return all(abs(a - b) <= self._TOLERANCE_MM for a, b in zip(left, right))

    def _check(self, name: str, passed: bool) -> dict[str, Any]:
        return {"name": name, "passed": passed}


__all__ = ["HettichKa4532SpacerProofChecker"]
