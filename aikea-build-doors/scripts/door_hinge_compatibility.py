"""Scope: Check one door against the selected concealed-hinge profile."""

from __future__ import annotations

from riex_nc70_hinge_profile import RiexNc70HingeProfile


class DoorHingeCompatibilityChecker:
    """Report only physical incompatibilities supported by profile facts."""

    def check(
        self,
        dimensions: dict[str, float],
        overlay_mm: float,
        profile: RiexNc70HingeProfile,
    ) -> tuple[str, ...]:
        checks = (
            (
                dimensions["width"] <= profile.maximum_door_width_mm,
                f"door width {dimensions['width']:.1f} mm exceeds the 600 mm profile limit",
            ),
            (
                max(dimensions["left_height"], dimensions["right_height"])
                <= profile.maximum_door_height_mm,
                "door height exceeds the profile's published quantity chart",
            ),
            (
                profile.minimum_door_thickness_mm
                <= dimensions["thickness"]
                <= profile.maximum_door_thickness_mm,
                "door thickness is outside the profile range",
            ),
            (
                abs(overlay_mm - profile.supported_overlay_mm) <= 0.1,
                "door overlay does not match the K6/H0 profile",
            ),
        )
        return tuple(message for passed, message in checks if not passed)


__all__ = ["DoorHingeCompatibilityChecker"]
