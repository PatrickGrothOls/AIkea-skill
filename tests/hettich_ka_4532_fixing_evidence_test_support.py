"""Scope: Build canonical saved KA 4532 fixing evidence for tests."""


class HettichKa4532FixingEvidenceTestSupport:
    """Own the one canonical evidence fixture shared by proof tests."""

    _CABINET_DEPTHS = (37.0, 165.0, 261.0, 325.0)
    _RUNNER_DEPTHS = (25.5, 153.5, 249.5, 313.5)

    def build(self) -> dict:
        return {
            "schema_version": 1,
            "status": "blocked",
            "manufacturing_authority": False,
            "cabinet_id": "cabinet_01",
            "drawer_id": "drawer_01",
            "spacer_item_number": "13952",
            "reason": "blocked_missing_longer_screw_and_cabinet_pilot",
            "resolved_authority": {
                "rail_fixed_member_hole_pattern": {
                    "status": "verified_against_exact_runner_cad",
                    "installation_document": "Hettich MS 10547.00.000",
                    "installation_url": (
                        "https://web2.hettich.com/hbh/addon/montage/"
                        "MS_10547_00_Montageanleitung_KA4532-SiSy.pdf"
                    ),
                    "hole_diameter_mm": 6.4,
                    "cabinet_depth_axes_from_front_mm": list(
                        self._CABINET_DEPTHS
                    ),
                },
                "spacer_support_corridor": {
                    "status": "verified_against_exact_spacer_cad",
                    "method": "new_fixing_path_through_solid_spacer_web",
                    "preformed_spacer_openings_used": False,
                    "width_mm": 25.0,
                    "asset_id": "hettich-13952-spacer-profile",
                    "sha256": "spacer-sha256",
                    "axes": [
                        {
                            "side": side,
                            "cabinet_depth_from_front_mm": cabinet_depth,
                            "cabinet_height_mm": 23.0,
                            "runner_native_depth_mm": runner_depth,
                            "spacer_native_depth_mm": cabinet_depth - 10.0,
                            "spacer_native_height_mm": 25.0,
                        }
                        for side in ("left", "right")
                        for cabinet_depth, runner_depth in zip(
                            self._CABINET_DEPTHS, self._RUNNER_DEPTHS
                        )
                    ],
                },
            },
            "missing_authority": [
                "longer_rail_through_spacer_screw_identity",
                "longer_rail_through_spacer_screw_length_mm",
                "cabinet_pilot_diameter_mm",
                "cabinet_pilot_depth_mm",
            ],
        }


__all__ = ["HettichKa4532FixingEvidenceTestSupport"]
