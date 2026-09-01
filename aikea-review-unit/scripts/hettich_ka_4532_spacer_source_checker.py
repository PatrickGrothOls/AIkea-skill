"""Scope: Bind KA 4532 proof parts to checksum-gated purchased STEP solids."""

from __future__ import annotations

from typing import Any

from hettich_ka_4532_spacer_profile import HETTICH_KA_4532_500_WITH_13952


class HettichKa4532SpacerSourceChecker:
    """Reject labels or equal-volume substitutes for the purchased hardware."""

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
                parts[name].source_hardware_asset_id == authority[0]
                and parts[name].source_geometry_selector == authority[1]
                and parts[name].source_solid is not None
                and parts[name].solid.val().isSame(parts[name].source_solid.val())
                for name, authority in expected.items()
            )
            and parts[f"{drawer_id}_spacer_left"].solid.val().isSame(
                parts[f"{drawer_id}_spacer_right"].solid.val()
            )
        )

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
