"""Scope: Verify official KA 4532 fixing axes against both purchased STEPs."""

from __future__ import annotations

from hettich_ka_4532_fixed_member_hole_pattern import (
    HETTICH_KA_4532_500_FIXED_MEMBER_HOLES,
)
from hettich_ka_4532_spacer_fixing_alignment import (
    HettichKa4532SpacerFixingAlignment,
    HettichKa4532SpacerFixingAxis,
)
from hettich_ka_4532_spacer_profile import HETTICH_KA_4532_500_WITH_13952


class HettichKa4532SpacerFixingAlignmentError(ValueError):
    """Reject a source shape or placement that breaks the approved axes."""


class HettichKa4532SpacerFixingAlignmentChecker:
    """Require exact rail openings and full-width spacer support on both hands."""

    _TOLERANCE_MM = 1e-5
    _VOLUME_TOLERANCE_MM3 = 1e-5

    def verify(self, step_set, mounting) -> HettichKa4532SpacerFixingAlignment:
        pattern = HETTICH_KA_4532_500_FIXED_MEMBER_HOLES
        profile = HETTICH_KA_4532_500_WITH_13952
        axes = []
        for side in ("left", "right"):
            fixed = getattr(step_set, f"runner_{side}").fixed_member
            runner = getattr(mounting, f"fixed_runner_{side}_in_cabinet")
            spacer = getattr(mounting, f"spacer_{side}_in_cabinet")
            interface_x_mm = self._interface_x(
                fixed, runner, spacer, profile.spacer_width_per_side_mm
            )
            for index, native_depth_mm in enumerate(
                pattern.fixed_member_native_depth_axes_mm
            ):
                self._require_runner_opening(fixed, native_depth_mm)
                owner_point = runner.to_owner(
                    (
                        interface_x_mm,
                        native_depth_mm,
                        pattern.fixed_member_native_height_mm,
                    ),
                )
                expected_depth_mm = (
                    mounting.cabinet_front_mm
                    + pattern.cabinet_depth_axes_mm[index]
                )
                self._require_close(owner_point[1], expected_depth_mm, "depth")
                spacer_point = spacer.to_local(owner_point)
                self._require_close(
                    spacer_point[0], profile.spacer_width_per_side_mm, "contact"
                )
                self._require_spacer_support(
                    step_set.spacer_solid,
                    spacer_point[1],
                    spacer_point[2],
                    profile.spacer_width_per_side_mm,
                    pattern.hole_diameter_mm,
                )
                axes.append(
                    HettichKa4532SpacerFixingAxis(
                        side,
                        pattern.cabinet_depth_axes_mm[index],
                        self._millimetres(owner_point[2]),
                        native_depth_mm,
                        self._millimetres(spacer_point[1]),
                        self._millimetres(spacer_point[2]),
                    )
                )
        return HettichKa4532SpacerFixingAlignment(
            pattern.installation_document,
            pattern.installation_url,
            pattern.hole_diameter_mm,
            profile.spacer_width_per_side_mm,
            tuple(axes),
        )

    def _require_runner_opening(self, fixed, depth_mm: float) -> None:
        import cadquery as cq

        bounds = fixed.BoundingBox()
        bore = cq.Solid.makeCylinder(
            HETTICH_KA_4532_500_FIXED_MEMBER_HOLES.hole_diameter_mm / 2.0,
            bounds.xlen + 2.0,
            cq.Vector(bounds.xmin - 1.0, depth_mm, 0.0),
            cq.Vector(1.0, 0.0, 0.0),
        )
        if fixed.intersect(bore).Volume() > self._VOLUME_TOLERANCE_MM3:
            raise HettichKa4532SpacerFixingAlignmentError(
                "exact fixed runner is closed at an official fixing axis"
            )

    def _require_spacer_support(
        self, spacer, depth_mm, height_mm, width_mm, diameter_mm
    ) -> None:
        import cadquery as cq

        corridor = cq.Solid.makeCylinder(
            diameter_mm / 2.0,
            width_mm,
            cq.Vector(0.0, depth_mm, height_mm),
            cq.Vector(1.0, 0.0, 0.0),
        )
        missing = corridor.Volume() - spacer.intersect(corridor).Volume()
        if missing > self._VOLUME_TOLERANCE_MM3:
            raise HettichKa4532SpacerFixingAlignmentError(
                "exact spacer lacks full material at an official rail fixing axis"
            )

    def _interface_x(self, fixed, runner, spacer, width_mm):
        bounds = fixed.BoundingBox()
        return min(
            (bounds.xmin, bounds.xmax),
            key=lambda value: abs(
                spacer.to_local(runner.to_owner((value, 0.0, 0.0)))[0]
                - width_mm
            ),
        )

    def _require_close(self, actual: float, expected: float, label: str) -> None:
        if abs(actual - expected) > self._TOLERANCE_MM:
            raise HettichKa4532SpacerFixingAlignmentError(
                f"official rail fixing misses the spacer {label}"
            )

    def _millimetres(self, value: float) -> float:
        return round(float(value), 6)


__all__ = [
    "HettichKa4532SpacerFixingAlignmentChecker",
    "HettichKa4532SpacerFixingAlignmentError",
]
