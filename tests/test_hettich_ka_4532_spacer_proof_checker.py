"""Scope: Verify exact spacer drawer movement and collision evidence."""

from hettich_ka_4532_fixing_evidence_test_support import (
    HettichKa4532FixingEvidenceTestSupport,
)
from hettich_ka_4532_spacer_proof_test_support import (
    HettichKa4532SpacerProofTestSupport,
)
from hettich_ka_4532_spacer_proof_checker import HettichKa4532SpacerProofChecker


class TestHettichKa4532SpacerProofChecker:
    """Protect source identity, complete motion, and conservative conflicts."""

    def setup_method(self) -> None:
        self.support = HettichKa4532SpacerProofTestSupport()
        self.source = self.support.source()
        self.evidence = HettichKa4532FixingEvidenceTestSupport()

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
            self.evidence.build(),
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
