"""Scope: Check one exact KA 4532 spacer drawer through its full travel."""

from __future__ import annotations

from typing import Any

from hettich_ka_4532_spacer_collision_checker import (
    HettichKa4532SpacerCollisionChecker,
)
from hettich_ka_4532_spacer_fixing_evidence_checker import (
    HettichKa4532SpacerFixingEvidenceChecker,
)
from hettich_ka_4532_spacer_motion_checker import HettichKa4532SpacerMotionChecker
from hettich_ka_4532_spacer_proof_report import HettichKa4532SpacerProofReport
from hettich_ka_4532_spacer_source_checker import (
    HettichKa4532SpacerSourceChecker,
)


class HettichKa4532SpacerProofChecker:
    """Compare exact closed and open trees, including conservative sweep bounds."""

    def __init__(self) -> None:
        self.collisions = HettichKa4532SpacerCollisionChecker()
        self.fixings = HettichKa4532SpacerFixingEvidenceChecker()
        self.motion = HettichKa4532SpacerMotionChecker()
        self.sources = HettichKa4532SpacerSourceChecker()

    def check(
        self,
        assembly_id: str,
        drawer_id: str,
        extension_mm: float,
        closed_parts: tuple[Any, ...],
        open_parts: tuple[Any, ...],
        source_cad: dict[str, Any],
        step_set: Any,
        artifacts: dict[str, Any],
        machining_blocker: dict[str, Any],
        reservations: tuple[dict[str, Any], ...],
    ) -> HettichKa4532SpacerProofReport:
        closed = self._parts_by_name(closed_parts)
        opened = self._parts_by_name(open_parts)
        moving_names = tuple(name for name in closed if name.startswith(f"{drawer_id}__"))
        static_names = tuple(name for name in closed if name not in moving_names)
        motion_evidence = self.motion.check(
            drawer_id,
            extension_mm,
            closed,
            opened,
            moving_names,
            static_names,
        )
        collision_evidence = self.collisions.check(
            drawer_id, closed, opened, moving_names, static_names
        )
        checks = (
            *motion_evidence.checks,
            self._check(
                "all six purchased items are the checksum-gated source STEP solids",
                self.sources.matches(drawer_id, closed, source_cad, step_set)
                and self.sources.matches(drawer_id, opened, source_cad, step_set),
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
                "official rail axes and remaining blocker match installed hardware",
                self.fixings.matches(
                    machining_blocker,
                    assembly_id,
                    drawer_id,
                    closed,
                    step_set,
                ),
            ),
        )
        return HettichKa4532SpacerProofReport(
            assembly_id,
            drawer_id,
            source_cad,
            artifacts,
            machining_blocker,
            reservations,
            motion_evidence.movement,
            collision_evidence,
            checks,
        )

    def _parts_by_name(self, parts: tuple[Any, ...]) -> dict[str, Any]:
        return {part.name: part for part in parts}

    def _check(self, name: str, passed: bool) -> dict[str, Any]:
        return {"name": name, "passed": passed}


__all__ = ["HettichKa4532SpacerProofChecker"]
