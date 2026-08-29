"""Scope: Select an exact registered KA 5332 runner length for one drawer."""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose

from hettich_ka_5332_runner_profile import (
    HETTICH_KA_5332_500,
    HettichKa5332RunnerProfile,
)


class HettichKa5332RunnerSelectionError(ValueError):
    """Report a requested depth with no verified matching runner profile."""


@dataclass(frozen=True, slots=True)
class HettichKa5332RunnerCatalog:
    """Choose only registered runner lengths whose real depth fits."""

    profiles: tuple[HettichKa5332RunnerProfile, ...]

    def select(
        self,
        requested_depth_mm: float | None,
        cabinet_inside_depth_mm: float,
    ) -> HettichKa5332RunnerProfile:
        fitting = tuple(
            profile
            for profile in self.profiles
            if profile.minimum_cabinet_depth_mm <= cabinet_inside_depth_mm
        )
        if requested_depth_mm is None:
            if not fitting:
                raise HettichKa5332RunnerSelectionError(
                    "no verified KA 5332 runner fits the cabinet depth"
                )
            return max(fitting, key=lambda profile: profile.nominal_length_mm)
        matches = tuple(
            profile
            for profile in fitting
            if isclose(
                profile.nominal_length_mm,
                requested_depth_mm,
                rel_tol=0.0,
                abs_tol=1e-6,
            )
        )
        if not matches:
            raise HettichKa5332RunnerSelectionError(
                f"no verified KA 5332 runner is registered for {requested_depth_mm:g} mm"
            )
        return matches[0]


HETTICH_KA_5332_RUNNER_CATALOG = HettichKa5332RunnerCatalog(
    (HETTICH_KA_5332_500,)
)


__all__ = [
    "HETTICH_KA_5332_RUNNER_CATALOG",
    "HettichKa5332RunnerCatalog",
    "HettichKa5332RunnerSelectionError",
]
