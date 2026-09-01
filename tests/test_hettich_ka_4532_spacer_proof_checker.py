"""Scope: Verify exact spacer drawer movement and collision evidence."""

from __future__ import annotations

import cadquery as cq

from hettich_ka_4532_spacer_proof_checker import (
    HettichKa4532SpacerProofChecker,
)
from unit_mockup import MockupPart


class TestHettichKa4532SpacerProofChecker:
    """Protect exact static hardware and complete drawer-subtree travel."""

    def test_accepts_clear_linear_travel_with_exact_articulation(self) -> None:
        report = self._check(self._parts(0.0), self._parts(-50.0))

        assert report.is_valid
        assert report.movement["declared_travel_mm"] == [0.0, -50.0, 0.0]
        assert report.collisions["closed_endpoint_pairs"] == []
        assert report.collisions["open_endpoint_pairs"] == []
        assert report.collisions["swept_envelope_pairs"] == []
        assert len(report.collisions["excluded_manufacturer_articulation_pairs"]) == 2

    def test_reports_a_conservative_swept_conflict(self) -> None:
        closed = self._parts(0.0) + (self._part("obstacle", 40.0, -30.0, 0.0),)
        opened = self._parts(-50.0) + (self._part("obstacle", 40.0, -30.0, 0.0),)

        report = self._check(closed, opened)

        assert not report.is_valid
        assert report.collisions["closed_endpoint_pairs"] == []
        assert report.collisions["open_endpoint_pairs"] == []
        assert report.collisions["swept_envelope_pairs"] == [
            ["drawer_01__bottom", "obstacle"]
        ]

    def _check(self, closed, opened):
        return HettichKa4532SpacerProofChecker().check(
            "cabinet_01",
            "drawer_01",
            50.0,
            closed,
            opened,
            {
                "runner": {"item_number": "9114276"},
                "spacer": {"item_number": "13952", "instances": 2},
            },
            {"closed": {}, "open": {}},
            {
                "manufacturing_authority": False,
                "missing_authority": [
                    "spacer_to_cabinet_fixing_hole_subset",
                    "spacer_to_cabinet_fastener_identity",
                    "cabinet_pilot_diameter_mm",
                    "cabinet_pilot_depth_mm",
                ],
            },
            (
                {"side_part_id": "left_side"},
                {"side_part_id": "right_side"},
            ),
        )

    def _parts(self, drawer_y_mm: float) -> tuple[MockupPart, ...]:
        return (
            self._part("drawer_01_spacer_left", 0.0, 20.0, 0.0),
            self._part("drawer_01_spacer_right", 95.0, 20.0, 0.0),
            self._part("drawer_01_runner_left_fixed", 10.0, 0.0, 0.0),
            self._part("drawer_01_runner_right_fixed", 88.0, 0.0, 0.0),
            self._part("drawer_01__bottom", 40.0, drawer_y_mm, 0.0),
            self._part(
                "drawer_01__drawer_01_runner_left_moving",
                10.0,
                drawer_y_mm,
                0.0,
            ),
            self._part(
                "drawer_01__drawer_01_runner_right_moving",
                88.0,
                drawer_y_mm,
                0.0,
            ),
        )

    def _part(self, name: str, x_mm: float, y_mm: float, z_mm: float) -> MockupPart:
        solid = cq.Workplane("XY").box(2.0, 10.0, 2.0, centered=False)
        return MockupPart(
            name,
            solid,
            cq.Location(cq.Vector(x_mm, y_mm, z_mm)),
            (0.5, 0.5, 0.5, 1.0),
        )
