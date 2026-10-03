"""Scope: Check exact BOM, cut-list, and machining records for one closed tree."""

from __future__ import annotations

from pathlib import Path

from fabrication_readiness_report import FabricationReadinessCheck
from fabrication_record_validator import FabricationRecordValidator
from fabrication_record_value_checker import FabricationRecordValueChecker
from fabrication_tree_evidence import FabricationTreeEvidence


class FabricationPackRecordChecker:
    """Coordinate record parsing, exact path coverage, and physical values."""

    def __init__(self) -> None:
        self.records = FabricationRecordValidator()
        self.values = FabricationRecordValueChecker()

    def check(
        self,
        project_root: Path,
        evidence: FabricationTreeEvidence,
    ) -> tuple[FabricationReadinessCheck, ...]:
        part_paths = tuple(item.path for item in evidence.parts)
        hardware_paths = tuple(item.path for item in evidence.hardware)
        bom_path = project_root / "manufacturing/bom.json"
        bom_parts, bom_part_problems = self.records.json_index(
            bom_path,
            "manufactured_parts",
            part_paths,
        )
        bom_hardware, bom_hardware_problems = self.records.json_index(
            bom_path,
            "purchased_hardware",
            hardware_paths,
        )
        cut_rows, cut_problems = self.records.csv_index(
            project_root / "manufacturing/cut-list.csv",
            part_paths,
        )
        machining_rows, machining_problems = self.records.json_index(
            project_root / "manufacturing/machining.json",
            "parts",
            part_paths,
        )
        return (
            self._check(
                "pack.complete_bom",
                bom_part_problems
                + bom_hardware_problems
                + self.values.part_bom_problems(evidence, bom_parts)
                + self.values.hardware_bom_problems(evidence, bom_hardware),
            ),
            self._check(
                "pack.complete_cut_list",
                cut_problems
                + self.values.cut_list_problems(evidence, cut_rows, bom_parts),
            ),
            self._check(
                "pack.machining_declarations",
                machining_problems
                + self.values.machining_problems(evidence, machining_rows),
            ),
        )

    def _check(self, code, problems) -> FabricationReadinessCheck:
        unique = tuple(sorted(set(problems)))
        return FabricationReadinessCheck(code, not unique, unique)


__all__ = ["FabricationPackRecordChecker"]
