"""Scope: Save the unresolved 13952 fixing authority without guessing it."""

from __future__ import annotations

import json


class HettichKa4532SpacerMachiningAuthorityRenderer:
    """Keep the fabrication gate closed until the missing fixing is approved."""

    def render(self, plan) -> str:
        payload = {
            "schema_version": 1,
            "status": "blocked",
            "manufacturing_authority": False,
            "drawer_id": plan.drawer.assembly_id,
            "spacer_item_number": plan.hardware.spacer_item_number,
            "reason": plan.machining_authority,
            "missing_authority": [
                "spacer_to_cabinet_fixing_hole_subset",
                "spacer_to_cabinet_fastener_identity",
                "cabinet_pilot_diameter_mm",
                "cabinet_pilot_depth_mm",
            ],
        }
        return json.dumps(payload, indent=2) + "\n"


__all__ = ["HettichKa4532SpacerMachiningAuthorityRenderer"]
