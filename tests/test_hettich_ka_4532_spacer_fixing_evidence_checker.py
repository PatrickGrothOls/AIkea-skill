"""Scope: Reject mutated KA 4532 machining-authority evidence."""

import pytest

from hettich_ka_4532_spacer_fixing_evidence_checker import (
    HettichKa4532SpacerFixingEvidenceChecker,
)
from hettich_ka_4532_fixing_evidence_test_support import (
    HettichKa4532FixingEvidenceTestSupport,
)
from hettich_ka_4532_spacer_proof_test_support import (
    HettichKa4532SpacerProofTestSupport,
)


class TestHettichKa4532SpacerFixingEvidenceChecker:
    """Bind the saved schema and official values to installed geometry."""

    def setup_method(self) -> None:
        support = HettichKa4532SpacerProofTestSupport()
        self.source = support.source()
        self.parts = {part.name: part for part in support.parts(0.0, self.source)}
        self.checker = HettichKa4532SpacerFixingEvidenceChecker()
        self.evidence = HettichKa4532FixingEvidenceTestSupport()

    def test_accepts_the_complete_verified_record(self) -> None:
        assert self._matches(self.evidence.build())

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
        machining = self.evidence.build()
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
        machining = self.evidence.build()
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
        machining = self.evidence.build()
        machining["resolved_authority"]["spacer_support_corridor"]["axes"][index][field] = "mutated"

        assert not self._matches(machining)

    @pytest.mark.parametrize("height_mm", (999.0, True))
    def test_rejects_coordinated_saved_height_mutation(self, height_mm) -> None:
        machining = self.evidence.build()
        for axis in machining["resolved_authority"]["spacer_support_corridor"]["axes"]:
            axis["cabinet_height_mm"] = height_mm

        assert not self._matches(machining)

    def _matches(self, machining: dict) -> bool:
        return self.checker.matches(
            machining, "cabinet_01", "drawer_01", self.parts, self.source
        )

    def _set(self, payload: dict, path: tuple[str, ...], value) -> None:
        self._owner(payload, path)[path[-1]] = value

    def _owner(self, payload: dict, path: tuple[str, ...]) -> dict:
        for key in path[:-1]:
            payload = payload[key]
        return payload


__all__ = ["TestHettichKa4532SpacerFixingEvidenceChecker"]
