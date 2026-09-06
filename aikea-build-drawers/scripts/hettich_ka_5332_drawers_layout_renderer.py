"""Scope: Render every resolved KA 5332 drawer owned by one cabinet."""

from __future__ import annotations

import yaml

from hettich_ka_5332_cabinet_drawers_plan import (
    HettichKa5332CabinetDrawersPlan,
)
from hettich_ka_5332_drawer_layout_record import (
    HettichKa5332DrawerLayoutRecord,
)


class HettichKa5332DrawersLayoutRenderer:
    """Expose an arbitrary drawer collection as inspectable YAML."""

    def __init__(self) -> None:
        self.record = HettichKa5332DrawerLayoutRecord()

    def render(self, plan: HettichKa5332CabinetDrawersPlan) -> str:
        return yaml.safe_dump(
            {
                "schema_version": 2,
                "parent_assembly_id": plan.parent_assembly_id,
                "drawers": [self.record.build(drawer) for drawer in plan.drawers],
            },
            sort_keys=False,
        )


__all__ = ["HettichKa5332DrawersLayoutRenderer"]
