"""Scope: Reject mutated KA 4532 machining-authority evidence."""

import pytest

from hettich_ka_4532_spacer_fixing_evidence_checker import (
    HettichKa4532SpacerFixingEvidenceChecker,
)
from hettich_ka_4532_spacer_proof_test_support import (
    HettichKa4532SpacerProofTestSupport,
)


class TestHettichKa4532SpacerFixingEvidenceChecker:
    """Bind the saved schema and official values to installed geometry."""

    _CABINET_DEPTHS = (37.0, 165.0, 261.0, 325.0)
    _RUNNER_DEPTHS = (25.5, 153.5, 249.5, 313.5)

    def setup_method(self) -> None:
        support = HettichKa4532SpacerProofTestSupport()
        self.source = support.source()
        self.parts = {part.name: part for part in support.parts(0.0, self.source)}
        self.checker = HettichKa4532SpacerFixingEvidenceChecker()

    def test_accepts_the_complete_verified_record(self) -> None:
        assert self._matches(self._machining())

    @pytest.mark.parametrize(
        ("path", "value"),
        (
            (("schema_version",), True),
            (("cabinet_id",), "other"),
            (("drawer_id",), "other"),
            (("reason",), "other"),
            (("resolved_authority", "rail_fixed_member_hole_pattern", "installation_document"), "other"),
            (("resolved_authority", "rail_fixed_member_hole_pattern", "installation_url"), "other"),
            (("resolved_authority", "rail_fixed_member_hole_pattern", "hole_diameter_mm"), 999.0),
            (("resolved_authority", "spacer_support_corridor", "asset_id"), "other"),
            (("resolved_authority", "spacer_support_corridor", "sha256"), "other"),
            (("resolved_authority", "spacer_support_corridor", "width_mm"), 0.0),
            (("resolved_authority", "spacer_support_corridor", "axes"), []),
            (("resolved_authority", "spacer_support_corridor", "axes"), "12345678"),
        ),
    )
    def test_rejects_mutated_authority(self, path: tuple[str, ...], value) -> None:
        machining = self._machining()
        self._set(machining, path, value)

        assert not self._matches(machining)

    @pytest.mark.parametrize(
        "path",
        (
            ("schema_version",),
            ("status",),
            ("manufacturing_authority",),
            ("cabinet_id",),
            ("drawer_id",),
            ("spacer_item_number",),
            ("reason",),
            ("missing_authority",),
            (("resolved_authority", "rail_fixed_member_hole_pattern", "installation_document")),
            (("resolved_authority", "rail_fixed_member_hole_pattern", "installation_url")),
            (("resolved_authority", "spacer_support_corridor", "asset_id")),
            (("resolved_authority", "spacer_support_corridor", "sha256")),
        ),
    )
    def test_rejects_deleted_authority(self, path: tuple[str, ...]) -> None:
        machining = self._machining()
        owner = self._owner(machining, path)
        del owner[path[-1]]

        assert not self._matches(machining)

    @pytest.mark.parametrize(
        ("index", "field"),
        (
            (0, "side"),
            (1, "cabinet_depth_from_front_mm"),
            (2, "runner_native_depth_mm"),
            (3, "spacer_native_depth_mm"),
            (4, "spacer_native_height_mm"),
        ),
    )
    def test_rejects_any_mutated_per_hand_axis(self, index: int, field: str) -> None:
        machining = self._machining()
        machining["resolved_authority"]["spacer_support_corridor"]["axes"][index][field] = "mutated"

        assert not self._matches(machining)

    @pytest.mark.parametrize("height_mm", (999.0, True))
    def test_rejects_coordinated_saved_height_mutation(self, height_mm) -> None:
        machining = self._machining()
        for axis in machining["resolved_authority"]["spacer_support_corridor"]["axes"]:
            axis["cabinet_height_mm"] = height_mm

        assert not self._matches(machining)

    def _matches(self, machining: dict) -> bool:
        return self.checker.matches(
            machining, "cabinet_01", "drawer_01", self.parts, self.source
        )

    def _machining(self) -> dict:
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
                    "cabinet_depth_axes_from_front_mm": list(self._CABINET_DEPTHS),
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

    def _set(self, payload: dict, path: tuple[str, ...], value) -> None:
        self._owner(payload, path)[path[-1]] = value

    def _owner(self, payload: dict, path: tuple[str, ...]) -> dict:
        for key in path[:-1]:
            payload = payload[key]
        return payload


__all__ = ["TestHettichKa4532SpacerFixingEvidenceChecker"]
