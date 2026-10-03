"""Scope: Read client-selected door hands from the global furniture specification."""

from __future__ import annotations

from typing import Any

from door_hinge_side import DoorHingeSide


class DoorOpeningPreferenceReader:
    """Validate only explicit exceptions while leaving ordinary doors automatic."""

    def read(
        self,
        project: dict[str, Any],
        assembly_ids: tuple[str, ...],
    ) -> dict[str, DoorHingeSide]:
        settings = project.get("design_settings", {})
        raw = settings.get("door_openings", {}) if isinstance(settings, dict) else {}
        if not isinstance(raw, dict):
            raise ValueError("design_settings.door_openings must be a mapping")
        unknown = tuple(assembly_id for assembly_id in raw if assembly_id not in assembly_ids)
        if unknown:
            raise ValueError(f"door opening refers to unknown assembly: {unknown[0]}")
        preferences: dict[str, DoorHingeSide] = {}
        for assembly_id, value in raw.items():
            if value not in (DoorHingeSide.LEFT.value, DoorHingeSide.RIGHT.value):
                raise ValueError(
                    f"door opening for {assembly_id} must be left or right"
                )
            preferences[assembly_id] = DoorHingeSide(value)
        return preferences


__all__ = ["DoorOpeningPreferenceReader"]
