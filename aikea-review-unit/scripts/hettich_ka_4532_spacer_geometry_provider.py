"""Scope: Select unchanged KA 4532 and 13952 solids for project review."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from hettich_ka_4532_spacer_step_set import (
    HettichKa4532SpacerStepSetLoader,
)
from hettich_ka_4532_spacer_profile import HETTICH_KA_4532_500_WITH_13952


class HettichKa4532SpacerGeometryProvider:
    """Cache the exact purchased set and select one declared native solid."""

    _RUNNER_ASSET_ID = HETTICH_KA_4532_500_WITH_13952.runner_asset_id
    _SPACER_ASSET_ID = HETTICH_KA_4532_500_WITH_13952.spacer_asset_id
    _RUNNER_HANDS = {
        "left": "runner_left",
        "right": "runner_right",
    }
    _RUNNER_MEMBERS = {
        "left-fixed": ("runner_left", "fixed_member"),
        "left-moving": ("runner_left", "moving_member"),
        "right-fixed": ("runner_right", "fixed_member"),
        "right-moving": ("runner_right", "moving_member"),
    }

    def __init__(
        self,
        loader: HettichKa4532SpacerStepSetLoader | None = None,
    ) -> None:
        self.loader = loader or HettichKa4532SpacerStepSetLoader()
        self.cache: dict[Path, Any] = {}

    def supports(self, asset_id: str) -> bool:
        return asset_id in {self._RUNNER_ASSET_ID, self._SPACER_ASSET_ID}

    def resolve(self, project_root: Path, spec: Any) -> Any:
        step_set = self._load_step_set(project_root)
        if spec.hardware_asset_id == self._SPACER_ASSET_ID:
            if spec.geometry_selector is not None:
                raise ValueError("Hettich 13952 spacer uses its single native solid")
            return self._workplane(step_set.spacer_solid)
        if spec.hardware_asset_id != self._RUNNER_ASSET_ID:
            raise ValueError(f"unsupported Hettich asset: {spec.hardware_asset_id}")
        if spec.geometry_selector in self._RUNNER_HANDS:
            side = getattr(step_set, self._RUNNER_HANDS[spec.geometry_selector])
            return self._compound_workplane(
                (side.fixed_member, side.moving_member)
            )
        if spec.geometry_selector not in self._RUNNER_MEMBERS:
            raise ValueError(
                "Hettich KA 4532 runner requires a saved hand or member selector"
            )
        side_name, member_name = self._RUNNER_MEMBERS[spec.geometry_selector]
        side = getattr(step_set, side_name)
        return self._workplane(getattr(side, member_name))

    def _load_step_set(self, project_root: Path) -> Any:
        root = project_root.resolve()
        if root not in self.cache:
            self.cache[root] = self.loader.load(project_root / "hardware")
        return self.cache[root]

    def _workplane(self, shape: Any) -> Any:
        import cadquery as cq

        return cq.Workplane(obj=shape)

    def _compound_workplane(self, members: tuple[Any, ...]) -> Any:
        import cadquery as cq

        return cq.Workplane(obj=cq.Compound.makeCompound(list(members)))


__all__ = ["HettichKa4532SpacerGeometryProvider"]
