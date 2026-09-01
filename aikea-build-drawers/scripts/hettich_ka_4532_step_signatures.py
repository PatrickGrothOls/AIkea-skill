"""Scope: Validate and name the exact native solids in the KA 4532 set."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class HettichKa4532StepSignatureError(ValueError):
    """Report native solids that no longer match the approved purchased set."""


@dataclass(frozen=True, slots=True)
class HettichKa4532ClassifiedStepSolids:
    """Name each verified source solid without changing its native geometry."""

    left_fixed: Any
    left_moving: Any
    right_moving: Any
    right_fixed: Any
    spacer: Any


@dataclass(frozen=True, slots=True)
class _NativeSolidSignature:
    role: str
    bounds_and_volume: tuple[float, ...]


class HettichKa4532StepSignatureClassifier:
    """Match exact article 9114276 and 13952 solids by measured signatures."""

    _TOLERANCE = 1e-3
    _EXPECTED = (
        _NativeSolidSignature(
            "left-fixed",
            (-0.0000001, 8.777139874, -9.5, 492.983917012,
             -22.85009328, 22.85009328, 44121.466839636),
        ),
        _NativeSolidSignature(
            "left-moving",
            (4.2, 12.5000001, -9.5, 495.54,
             -12.149518924, 12.149518924, 24166.280706188),
        ),
        _NativeSolidSignature(
            "right-moving",
            (188.4999999, 196.8, -9.5, 495.54,
             -12.149518924, 12.149518924, 24166.280706188),
        ),
        _NativeSolidSignature(
            "right-fixed",
            (192.222860126, 201.0000001, -9.5, 492.983917012,
             -22.85009328, 22.85009328, 44121.466875251),
        ),
        _NativeSolidSignature(
            "spacer",
            (-0.0000001, 25.0000001, 0.0, 486.0,
             0.0, 50.0, 576658.608794442),
        ),
    )

    def classify(
        self,
        runner_solids: tuple[Any, ...],
        spacer_solid: Any,
    ) -> HettichKa4532ClassifiedStepSolids:
        by_role = {
            self._matching_role(solid): solid for solid in runner_solids
        }
        runner_roles = {
            "left-fixed",
            "left-moving",
            "right-moving",
            "right-fixed",
        }
        if len(runner_solids) != len(runner_roles) or set(by_role) != runner_roles:
            raise HettichKa4532StepSignatureError(
                "KA 4532 native solid set is incomplete or duplicated"
            )
        if self._matching_role(spacer_solid) != "spacer":
            raise HettichKa4532StepSignatureError(
                "article 13952 source does not contain the exact spacer solid"
            )
        return HettichKa4532ClassifiedStepSolids(
            left_fixed=by_role["left-fixed"],
            left_moving=by_role["left-moving"],
            right_moving=by_role["right-moving"],
            right_fixed=by_role["right-fixed"],
            spacer=spacer_solid,
        )

    def _matching_role(self, solid: Any) -> str:
        measured = self._measure(solid)
        matches = tuple(
            signature.role
            for signature in self._EXPECTED
            if all(
                abs(actual - expected) <= self._TOLERANCE
                for actual, expected in zip(measured, signature.bounds_and_volume)
            )
        )
        if len(matches) != 1:
            raise HettichKa4532StepSignatureError(
                "native solid does not match exact KA 4532 article 9114276 or 13952"
            )
        return matches[0]

    def _measure(self, solid: Any) -> tuple[float, ...]:
        bounds = solid.BoundingBox()
        return (
            bounds.xmin,
            bounds.xmax,
            bounds.ymin,
            bounds.ymax,
            bounds.zmin,
            bounds.zmax,
            solid.Volume(),
        )


__all__ = [
    "HettichKa4532ClassifiedStepSolids",
    "HettichKa4532StepSignatureClassifier",
    "HettichKa4532StepSignatureError",
]
