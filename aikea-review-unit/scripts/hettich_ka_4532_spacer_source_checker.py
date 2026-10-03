"""Scope: Bind KA 4532 proof parts to checksum-gated purchased STEP solids."""

from __future__ import annotations

from typing import Any

from hettich_ka_4532_spacer_profile import HETTICH_KA_4532_500_WITH_13952


class HettichKa4532SpacerSourceChecker:
    """Reject labels or equal-volume substitutes for the purchased hardware."""

    _TOLERANCE_MM3 = 1e-5
    _RUNNER_MEMBERS = {
        "left-fixed": ("runner_left", "fixed_member"),
        "left-moving": ("runner_left", "moving_member"),
        "right-fixed": ("runner_right", "fixed_member"),
        "right-moving": ("runner_right", "moving_member"),
    }

    def matches(
        self,
        drawer_id: str,
        parts: dict[str, Any],
        source_cad: dict[str, Any],
        step_set: Any,
    ) -> bool:
        expected = self._expected_authority(drawer_id)
        return (
            expected.keys() <= parts.keys()
            and self._metadata_matches(source_cad, step_set)
            and all(
                self._part_matches(parts[name], authority, step_set)
                for name, authority in expected.items()
            )
        )

    def _part_matches(
        self,
        part: Any,
        authority: tuple[str, str | None],
        step_set: Any,
    ) -> bool:
        asset_id, selector = authority
        return (
            part.source_hardware_asset_id == asset_id
            and part.source_geometry_selector == selector
            and self._geometry_matches(
                part.solid.val(),
                self._source_solid(selector, step_set),
            )
        )

    def _geometry_matches(self, rendered: Any, source: Any) -> bool:
        rendered_volume = rendered.Volume()
        source_volume = source.Volume()
        shared_volume = rendered.intersect(source).Volume()
        return all(
            abs(left - right) <= self._TOLERANCE_MM3
            for left, right in (
                (rendered_volume, source_volume),
                (shared_volume, rendered_volume),
                (shared_volume, source_volume),
            )
        )

    def _source_solid(self, selector: str | None, step_set: Any) -> Any:
        if selector is None:
            return step_set.spacer_solid
        side_name, member_name = self._RUNNER_MEMBERS[selector]
        return getattr(getattr(step_set, side_name), member_name)

    def _metadata_matches(self, source_cad: dict[str, Any], step_set: Any) -> bool:
        profile = HETTICH_KA_4532_500_WITH_13952
        runner = source_cad["runner"]
        spacer = source_cad["spacer"]
        return all(
            (
                runner["item_number"] == profile.runner_item_number,
                runner["asset_id"] == profile.runner_asset_id,
                runner["sha256"] == step_set.runner_source.asset.sha256,
                spacer["item_number"] == profile.spacer_item_number,
                spacer["asset_id"] == profile.spacer_asset_id,
                spacer["sha256"] == step_set.spacer_source.asset.sha256,
                spacer["instances"] == 2,
            )
        )

    def _expected_authority(
        self,
        drawer_id: str,
    ) -> dict[str, tuple[str, str | None]]:
        profile = HETTICH_KA_4532_500_WITH_13952
        return {
            f"{drawer_id}_runner_left_fixed": (profile.runner_asset_id, "left-fixed"),
            f"{drawer_id}_runner_right_fixed": (profile.runner_asset_id, "right-fixed"),
            f"{drawer_id}_spacer_left": (profile.spacer_asset_id, None),
            f"{drawer_id}_spacer_right": (profile.spacer_asset_id, None),
            f"{drawer_id}__{drawer_id}_runner_left_moving": (
                profile.runner_asset_id,
                "left-moving",
            ),
            f"{drawer_id}__{drawer_id}_runner_right_moving": (
                profile.runner_asset_id,
                "right-moving",
            ),
        }


__all__ = ["HettichKa4532SpacerSourceChecker"]
