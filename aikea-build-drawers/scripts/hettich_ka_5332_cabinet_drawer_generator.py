"""Scope: Save one KA 5332 drawer child beneath an existing cabinet."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from cabinet_drawer_plan import DrawerLayout
from hettich_ka_5332_cabinet_drawer_plan import (
    HettichKa5332CabinetDrawerPlan,
)
from hettich_ka_5332_cabinet_drawers_generator import (
    HettichKa5332CabinetDrawersGenerator,
)


@dataclass(frozen=True, slots=True)
class HettichKa5332DrawerGenerationResult:
    """Report the saved drawer plan and project files written for it."""

    plan: HettichKa5332CabinetDrawerPlan
    written_paths: tuple[Path, ...]


class HettichKa5332CabinetDrawerGenerator:
    """Generate the wooden child only after exact source CAD resolves."""

    def __init__(
        self,
        step_loader=None,
    ) -> None:
        self.drawers = HettichKa5332CabinetDrawersGenerator(step_loader)

    def generate(
        self,
        project_root: Path,
        parent_assembly_id: str,
        layout: DrawerLayout,
        *,
        hardware_directory: Path,
    ) -> HettichKa5332DrawerGenerationResult:
        result = self.drawers.add(
            project_root,
            parent_assembly_id,
            layout,
            hardware_directory=hardware_directory,
        )
        plan = next(
            drawer
            for drawer in result.plan.drawers
            if drawer.drawer.assembly_id == layout.drawer_id
        )
        return HettichKa5332DrawerGenerationResult(plan, result.written_paths)


__all__ = [
    "HettichKa5332CabinetDrawerGenerator",
    "HettichKa5332DrawerGenerationResult",
]
