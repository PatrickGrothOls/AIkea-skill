"""Scope: Save verified KA 4532 fixing axes and the remaining authority gap."""

from __future__ import annotations

import json


class HettichKa4532SpacerMachiningAuthorityRenderer:
    """Keep fabrication blocked only on the longer screw and cabinet pilot."""

    def render(self, plan) -> str:
        payload = {
            "schema_version": 1,
            "status": "blocked",
            "manufacturing_authority": False,
            "cabinet_id": plan.parent_assembly_id,
            "drawer_id": plan.drawer.assembly_id,
            "spacer_item_number": plan.hardware.spacer_item_number,
            "reason": plan.machining_authority,
            "resolved_authority": self._resolved_authority(plan),
            "missing_authority": [
                "longer_rail_through_spacer_screw_identity",
                "longer_rail_through_spacer_screw_length_mm",
                "cabinet_pilot_diameter_mm",
                "cabinet_pilot_depth_mm",
            ],
        }
        return json.dumps(payload, indent=2) + "\n"

    def _resolved_authority(self, plan) -> dict:
        alignment = plan.fixing_alignment
        return {
            "rail_fixed_member_hole_pattern": {
                "status": "verified_against_exact_runner_cad",
                "installation_document": alignment.installation_document,
                "installation_url": alignment.installation_url,
                "hole_diameter_mm": alignment.hole_diameter_mm,
                "cabinet_depth_axes_from_front_mm": list(
                    alignment.cabinet_depth_axes_mm
                ),
            },
            "spacer_support_corridor": {
                "status": "verified_against_exact_spacer_cad",
                "method": "new_fixing_path_through_solid_spacer_web",
                "preformed_spacer_openings_used": False,
                "width_mm": alignment.spacer_support_width_mm,
                "asset_id": plan.hardware.spacer_asset_id,
                "sha256": plan.hardware_step.spacer_source.asset.sha256,
                "axes": [self._axis(axis) for axis in alignment.axes],
            },
        }

    def _axis(self, axis) -> dict:
        return {
            "side": axis.side,
            "cabinet_depth_from_front_mm": axis.cabinet_depth_from_front_mm,
            "cabinet_height_mm": axis.cabinet_height_mm,
            "runner_native_depth_mm": axis.runner_native_depth_mm,
            "spacer_native_depth_mm": axis.spacer_native_depth_mm,
            "spacer_native_height_mm": axis.spacer_native_height_mm,
        }


__all__ = ["HettichKa4532SpacerMachiningAuthorityRenderer"]
