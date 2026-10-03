"""Scope: Select one exact hand from a registered Hettich KA 5332 pair."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from hettich_ka_5332_step_assembly import HettichKa5332StepAssemblyLoader


class HettichKa5332GeometryProvider:
    """Verify the paired source once and return one unchanged handed mechanism."""

    _ASSET_ID = "hettich-ka-5332-500-runner-pair"

    def __init__(self) -> None:
        self.loader = HettichKa5332StepAssemblyLoader()
        self.cache: dict[Path, Any] = {}

    def supports(self, asset_id: str) -> bool:
        return asset_id == self._ASSET_ID

    def resolve(self, project_root: Path, spec: Any) -> Any:
        source = project_root / "hardware/hettich/ka-5332/9057405/source"
        root = project_root.resolve()
        if root not in self.cache:
            self.cache[root] = self.loader.load(source)
        assembly = self.cache[root]
        if spec.geometry_selector not in {"left", "right"}:
            raise ValueError("Hettich runner geometry requires a saved hand")
        side = getattr(assembly, spec.geometry_selector)
        return self._workplane(
            (side.cabinet_member, side.middle_member, side.drawer_member)
        )

    def _workplane(self, members: tuple[Any, ...]) -> Any:
        import cadquery as cq

        return cq.Workplane(obj=cq.Compound.makeCompound(list(members)))


__all__ = ["HettichKa5332GeometryProvider"]
