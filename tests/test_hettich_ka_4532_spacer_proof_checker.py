"""Scope: Verify exact spacer drawer movement and collision evidence."""

from hettich_ka_4532_spacer_proof_test_support import (
    HettichKa4532SpacerProofTestSupport,
)
from hettich_ka_4532_spacer_proof_checker import HettichKa4532SpacerProofChecker


class TestHettichKa4532SpacerProofChecker:
    """Protect source identity, complete motion, and conservative conflicts."""

    def setup_method(self) -> None:
        self.support = HettichKa4532SpacerProofTestSupport()
        self.source = self.support.source()

    def test_accepts_clear_linear_travel_with_exact_articulation(self) -> None:
        report = self._check(self._parts(0.0), self._parts(-50.0))

        assert report.is_valid
        assert report.movement["declared_travel_mm"] == [0.0, -50.0, 0.0]
        assert report.collisions["closed_endpoint_pairs"] == []
        assert report.collisions["open_endpoint_pairs"] == []
        assert report.collisions["swept_envelope_pairs"] == []
        assert len(report.collisions["excluded_manufacturer_articulation_pairs"]) == 2

    def test_reports_a_conservative_swept_conflict(self) -> None:
        obstacle = self.support.part("obstacle", 40.0, -30.0)

        report = self._check(
            self._parts(0.0) + (obstacle,),
            self._parts(-50.0) + (obstacle,),
        )

        assert not report.is_valid
        assert report.collisions["closed_endpoint_pairs"] == []
        assert report.collisions["open_endpoint_pairs"] == []
        assert report.collisions["swept_envelope_pairs"] == [
            ["drawer_01__bottom", "obstacle"]
        ]

    def test_rejects_equal_volume_substitute_geometry(self) -> None:
        substitute = self.support.equal_volume_substitute()

        report = self._check(
            self.support.replace_spacer(self._parts(0.0), substitute),
            self.support.replace_spacer(self._parts(-50.0), substitute),
        )

        assert not report.is_valid
        assert not self._passed(report, "all six purchased items")

    def test_rejects_an_empty_drawer_subtree(self) -> None:
        report = self._check(self._parts(0.0)[:4], self._parts(-50.0)[:4])

        assert not report.is_valid
        assert not self._passed(report, "complete generated drawer subtree")

    def _parts(self, drawer_y_mm: float):
        return self.support.parts(drawer_y_mm, self.source)

    def _check(self, closed, opened):
        return HettichKa4532SpacerProofChecker().check(
            "cabinet_01",
            "drawer_01",
            50.0,
            closed,
            opened,
            {
                "runner": {
                    "item_number": "9114276",
                    "asset_id": "hettich-ka-4532-500-runner-pair",
                    "sha256": "runner-sha256",
                },
                "spacer": {
                    "item_number": "13952",
                    "asset_id": "hettich-13952-spacer-profile",
                    "sha256": "spacer-sha256",
                    "instances": 2,
                },
            },
            self.source,
            {"closed": {}, "open": {}},
            {
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
                        "cabinet_depth_axes_from_front_mm": [
                            37.0,
                            165.0,
                            261.0,
                            325.0,
                        ],
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
                                (37.0, 165.0, 261.0, 325.0),
                                (25.5, 153.5, 249.5, 313.5),
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
            },
            (
                {"side_part_id": "left_side"},
                {"side_part_id": "right_side"},
            ),
        )

    def _passed(self, report, name_fragment: str) -> bool:
        return next(
            check["passed"]
            for check in report.checks
            if name_fragment in check["name"]
        )
