"""Scope: Generate and save one exact KA 4532 spacer cabinet proof."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

import yaml

from complete_assembly_review_generator import CompleteAssemblyReviewGenerator
from hettich_ka_4532_spacer_proof_checker import (
    HettichKa4532SpacerProofChecker,
)
from hettich_ka_4532_spacer_proof_report import HettichKa4532SpacerProofReport
from hettich_ka_4532_spacer_step_set import HettichKa4532SpacerStepSetLoader


@dataclass(frozen=True, slots=True)
class HettichKa4532SpacerProofResult:
    """Expose both visual states and their saved physical evidence."""

    closed_glb_path: Path
    open_glb_path: Path
    report_path: Path
    report: HettichKa4532SpacerProofReport


class HettichKa4532SpacerProofGenerator:
    """Run the generic recursive review twice and compare its exact solids."""

    def __init__(self, review=None, checker=None, step_loader=None) -> None:
        self.review = review or CompleteAssemblyReviewGenerator()
        self.checker = checker or HettichKa4532SpacerProofChecker()
        self.steps = step_loader or HettichKa4532SpacerStepSetLoader()

    def generate(
        self,
        project_root: Path,
        assembly_id: str,
        output_directory: Path,
        feature_states: dict[str, str] | None = None,
    ) -> HettichKa4532SpacerProofResult:
        report_path = output_directory / "ka4532-spacer-movement-collision-check.json"
        HettichKa4532SpacerProofReport.invalidate(report_path)
        layout_path = project_root / "assemblies" / assembly_id / "drawer-layout.yaml"
        layout = yaml.safe_load(layout_path.read_text(encoding="utf-8"))
        drawer_id = layout["drawer"]["id"]
        selector = f"{assembly_id}/drawers"
        states = dict(feature_states or {})
        if selector in states:
            raise ValueError(f"proof owns drawer feature state: {selector}")
        closed = self.review.generate(
            project_root,
            assembly_id,
            output_directory / "closed.glb",
            {**states, selector: "closed"},
        )
        opened = self.review.generate(
            project_root,
            assembly_id,
            output_directory / "open.glb",
            {**states, selector: "open"},
        )
        machining_path = (
            project_root / "assemblies" / assembly_id / "drawers" / "machining-authority.json"
        )
        reservations_path = (
            project_root / "assemblies" / assembly_id / "hardware-reservations.json"
        )
        machining = self._json(machining_path)
        reservations = tuple(
            item
            for item in self._json(reservations_path)["reservations"]
            if item["hardware_kind"] == "drawer_runner_with_spacer"
            and item["owner_id"].startswith(f"{drawer_id}_")
        )
        step_set = self.steps.load(project_root / "hardware")
        report = self.checker.check(
            assembly_id,
            drawer_id,
            float(layout["drawer"]["box"]["side_length_mm"]),
            closed.rendered_parts,
            opened.rendered_parts,
            layout["purchased_set"],
            step_set,
            {
                "closed": self._review_artifact(closed),
                "open": self._review_artifact(opened),
                "hardware_reservations": str(reservations_path),
                "machining_authority": str(machining_path),
            },
            machining,
            reservations,
        )
        report.write(report_path)
        return HettichKa4532SpacerProofResult(
            closed.glb_path,
            opened.glb_path,
            report_path,
            report,
        )

    def _review_artifact(self, result: Any) -> dict[str, Any]:
        review = self._json(result.report_path)
        return {
            "glb": str(result.glb_path),
            "glb_sha256": review["artifact_sha256"],
            "review_report": str(result.report_path),
            "feature_states": review["feature_states"],
        }

    def _json(self, path: Path) -> dict[str, Any]:
        return json.loads(path.read_text(encoding="utf-8"))


__all__ = [
    "HettichKa4532SpacerProofGenerator",
    "HettichKa4532SpacerProofResult",
]
