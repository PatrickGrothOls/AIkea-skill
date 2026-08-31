"""Scope: Check the fabrication pack, validation evidence, and current approval."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path

from fabrication_record_validator import FabricationRecordValidator
from fabrication_readiness_report import FabricationReadinessCheck


class FabricationArtifactChecker:
    """Require a complete conventional output pack for every tree item."""

    def __init__(self) -> None:
        self.records = FabricationRecordValidator()

    def check(
        self,
        project_root: Path,
        part_paths: tuple[str, ...],
        hardware_paths: tuple[str, ...],
    ) -> tuple[FabricationReadinessCheck, ...]:
        return (
            self._part_exports(project_root, part_paths),
            self._bom(project_root, part_paths, hardware_paths),
            self._cut_list(project_root, part_paths),
            self._machining(project_root, part_paths),
            self._feature_evidence(project_root),
            self._validation(project_root),
            self._visual_approval(project_root),
        )

    def _part_exports(self, root, part_paths) -> FabricationReadinessCheck:
        missing = tuple(
            str(path.relative_to(root))
            for part_path in part_paths
            for suffix in (".step", ".dxf")
            for path in (root / "manufacturing/parts" / f"{self._slug(part_path)}{suffix}",)
            if not self._nonempty(path)
        )
        return self._check("pack.part_step_and_drawings", missing)

    def _bom(self, root, part_paths, hardware_paths) -> FabricationReadinessCheck:
        path = root / "manufacturing/bom.json"
        problems = self.records.json_coverage(
            path,
            "manufactured_parts",
            part_paths,
            ("material", "thickness_mm", "quantity"),
        ) + self.records.json_coverage(
            path,
            "purchased_hardware",
            hardware_paths,
            ("manufacturer", "product_code", "quantity"),
        )
        return self._check("pack.complete_bom", problems)

    def _cut_list(self, root, part_paths) -> FabricationReadinessCheck:
        path = root / "manufacturing/cut-list.csv"
        problems = self.records.csv_coverage(
            path,
            part_paths,
            (
                "material",
                "thickness_mm",
                "quantity",
                "blank_width_mm",
                "blank_height_mm",
            ),
        )
        return self._check("pack.complete_cut_list", problems)

    def _machining(self, root, part_paths) -> FabricationReadinessCheck:
        path = root / "manufacturing/machining.json"
        problems = self.records.json_coverage(
            path,
            "parts",
            part_paths,
            ("operations",),
        )
        return self._check("pack.machining_declarations", problems)

    def _feature_evidence(self, root) -> FabricationReadinessCheck:
        problems = []
        for manifest_path in sorted((root / "assemblies").glob("*/features.json")):
            manifest = self.records.read_json(manifest_path)
            if manifest is None:
                problems.append(str(manifest_path.relative_to(root)))
                continue
            for feature in manifest.get("features", ()):
                module = feature.get("module", "")
                evidence_path = manifest_path.parent / "fabrication-evidence" / (
                    module.replace(".", "-") + ".json"
                )
                evidence = self.records.read_json(evidence_path)
                if not self._valid_evidence(evidence, module):
                    problems.append(str(evidence_path.relative_to(root)))
        return self._check("pack.feature_manufacturing_evidence", tuple(problems))

    def _validation(self, root) -> FabricationReadinessCheck:
        path = root / "assemblies/full-wardrobe-position-check.json"
        data = self.records.read_json(path)
        problems = () if data and data.get("status") == "valid" else (
            str(path.relative_to(root)),
        )
        return self._check("validation.full_wardrobe_position", problems)

    def _visual_approval(self, root) -> FabricationReadinessCheck:
        model = root / "assemblies/full_wardrobe_review.glb"
        record = root / "reviews/fabrication-assembly.json"
        data = self.records.read_json(record)
        approved = (
            self._nonempty(model)
            and data is not None
            and data.get("review_type") == "fabrication_assembly"
            and data.get("status") == "approved"
            and data.get("artifact_sha256") == sha256(model.read_bytes()).hexdigest()
        )
        return self._check(
            "approval.current_closed_assembly",
            () if approved else (str(record.relative_to(root)),),
        )

    def _valid_evidence(self, data, module) -> bool:
        checks = data.get("checks") if data else None
        return bool(
            data
            and data.get("schema_version") == 1
            and data.get("feature") == module
            and data.get("status") == "valid"
            and data.get("manufacturing_authority") is True
            and isinstance(checks, list)
            and checks
            and all(check.get("passed") for check in checks)
        )

    def _nonempty(self, path: Path) -> bool:
        return path.is_file() and path.stat().st_size > 0

    def _slug(self, path: str) -> str:
        return path.replace("/", "__")

    def _check(self, code, problems) -> FabricationReadinessCheck:
        return FabricationReadinessCheck(code, not problems, tuple(problems))


__all__ = ["FabricationArtifactChecker"]
