"""Scope: Bind full-wardrobe position evidence to the current closed tree."""

from __future__ import annotations

from assembly_tree_placement_fingerprint import AssemblyTreePlacementFingerprinter
from fabrication_position_record_validator import FabricationPositionRecordValidator
from fabrication_readiness_report import FabricationReadinessCheck
from fabrication_record_validator import FabricationRecordValidator


class FabricationPositionEvidenceChecker:
    """Require complete position structure and the exact current tree fingerprint."""

    def __init__(self) -> None:
        self.records = FabricationRecordValidator()
        self.fingerprints = AssemblyTreePlacementFingerprinter()
        self.position_record = FabricationPositionRecordValidator()

    def check(self, root, tree, visits) -> FabricationReadinessCheck:
        path = root / "assemblies/full-wardrobe-position-check.json"
        data = self.records.read_json(path)
        fingerprint = self.fingerprints.build(visits)
        checks = data.get("checks") if data else None
        valid = bool(
            data
            and data.get("schema_version") == 1
            and data.get("status") == "valid"
            and tree.root_child_ids
            and self.position_record.valid(data, tree)
            and self._valid_checks(checks)
            and data.get("closed_tree_placement_sha256") == fingerprint.sha256
            and data.get("closed_tree_item_count") == fingerprint.item_count
        )
        problems = () if valid else (str(path.relative_to(root)),)
        return FabricationReadinessCheck(
            "validation.full_wardrobe_position",
            valid,
            problems,
        )

    def _valid_checks(self, checks) -> bool:
        if not isinstance(checks, list) or not checks:
            return False
        names = tuple(
            check.get("name")
            for check in checks
            if isinstance(check, dict)
            and isinstance(check.get("name"), str)
            and check["name"].strip()
            and check.get("passed") is True
        )
        return len(names) == len(checks) and len(set(names)) == len(names)

__all__ = ["FabricationPositionEvidenceChecker"]
