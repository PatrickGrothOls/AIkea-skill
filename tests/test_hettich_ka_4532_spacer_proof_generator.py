"""Scope: Verify the two-state KA 4532 proof orchestration contract."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import yaml

from hettich_ka_4532_spacer_proof_generator import (
    HettichKa4532SpacerProofGenerator,
)
from hettich_ka_4532_spacer_proof_report import HettichKa4532SpacerProofReport


class CompleteReviewProbe:
    """Save the minimum complete-review record for each requested state."""

    def __init__(self) -> None:
        self.calls = []

    def generate(self, project_root, assembly_id, output, states):
        self.calls.append((project_root, assembly_id, output, states))
        output.parent.mkdir(parents=True, exist_ok=True)
        report_path = output.with_suffix(".review.json")
        report_path.write_text(
            json.dumps(
                {
                    "artifact_sha256": f"sha-{output.stem}",
                    "feature_states": states,
                }
            ),
            encoding="utf-8",
        )
        return SimpleNamespace(
            glb_path=output,
            report_path=report_path,
            rendered_parts=(output.stem,),
        )


class ProofCheckerProbe:
    """Capture the exact inputs passed from generated project records."""

    def __init__(self) -> None:
        self.call = None

    def check(self, *arguments):
        self.call = arguments
        return HettichKa4532SpacerProofReport(
            "cabinet_01",
            "drawer_01",
            arguments[5],
            arguments[6],
            arguments[7],
            arguments[8],
            {},
            {},
            ({"name": "probe", "passed": True},),
        )


class TestHettichKa4532SpacerProofGenerator:
    """Keep exact proof generation on the generic recursive review path."""

    def test_compares_closed_and_open_with_the_same_door_state(self, tmp_path) -> None:
        self._project_files(tmp_path)
        review = CompleteReviewProbe()
        checker = ProofCheckerProbe()
        generator = HettichKa4532SpacerProofGenerator(review, checker)

        result = generator.generate(
            tmp_path,
            "cabinet_01",
            tmp_path / "review",
            {"cabinet_01/door_hinges": "open"},
        )

        assert [call[3] for call in review.calls] == [
            {"cabinet_01/door_hinges": "open", "cabinet_01/drawers": "closed"},
            {"cabinet_01/door_hinges": "open", "cabinet_01/drawers": "open"},
        ]
        assert checker.call[3] == ("closed",)
        assert checker.call[4] == ("open",)
        assert len(checker.call[8]) == 2
        assert result.report_path.is_file()

    def _project_files(self, root: Path) -> None:
        assembly = root / "assemblies" / "cabinet_01"
        drawers = assembly / "drawers"
        drawers.mkdir(parents=True)
        (assembly / "drawer-layout.yaml").write_text(
            yaml.safe_dump(
                {
                    "drawer": {"id": "drawer_01", "box": {"side_length_mm": 500.0}},
                    "purchased_set": {"spacer": {"item_number": "13952"}},
                }
            ),
            encoding="utf-8",
        )
        (drawers / "machining-authority.json").write_text(
            json.dumps(
                {"manufacturing_authority": False, "missing_authority": ["fixing"]}
            ),
            encoding="utf-8",
        )
        (assembly / "hardware-reservations.json").write_text(
            json.dumps(
                {
                    "reservations": [
                        {
                            "owner_id": "drawer_01_left",
                            "hardware_kind": "drawer_runner_with_spacer",
                            "side_part_id": "left_side",
                        },
                        {
                            "owner_id": "drawer_01_right",
                            "hardware_kind": "drawer_runner_with_spacer",
                            "side_part_id": "right_side",
                        },
                        {
                            "owner_id": "hinge_01",
                            "hardware_kind": "hinge_plate",
                            "side_part_id": "left_side",
                        },
                    ]
                }
            ),
            encoding="utf-8",
        )
