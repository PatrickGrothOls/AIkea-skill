"""Scope: Validate saved feature and wardrobe-position fabrication evidence."""

from __future__ import annotations

from hashlib import sha256

from fabrication_readiness_report import FabricationReadinessCheck
from fabrication_record_validator import FabricationRecordValidator


class FabricationSavedEvidenceChecker:
    """Require recursive feature proofs and substantive full-position checks."""

    def __init__(self) -> None:
        self.records = FabricationRecordValidator()

    def check(self, root, tree) -> tuple[FabricationReadinessCheck, ...]:
        return self._feature_evidence(root, tree), self._position_evidence(root, tree)

    def _feature_evidence(self, root, tree) -> FabricationReadinessCheck:
        part_hashes = self._part_step_hashes(root, tree)
        problems = []
        for manifest_path in sorted((root / "assemblies").rglob("features.json")):
            manifest = self.records.read_json(manifest_path)
            features = manifest.get("features") if manifest else None
            if manifest is None or manifest.get("schema_version") != 1 or not isinstance(features, list):
                problems.append(str(manifest_path.relative_to(root)))
                continue
            for feature in features:
                module = feature.get("module") if isinstance(feature, dict) else None
                if not isinstance(module, str) or not module:
                    problems.append(str(manifest_path.relative_to(root)))
                    continue
                evidence_path = manifest_path.parent / "fabrication-evidence" / (
                    module.replace(".", "-") + ".json"
                )
                data = self.records.read_json(evidence_path)
                if not self._valid_feature_evidence(data, module, part_hashes):
                    problems.append(str(evidence_path.relative_to(root)))
        return self._check("pack.feature_manufacturing_evidence", tuple(problems))

    def _valid_feature_evidence(self, data, module, part_hashes) -> bool:
        checks = data.get("checks") if data else None
        artifacts = data.get("part_artifacts") if data else None
        artifact_index = {
            item.get("path"): item
            for item in artifacts or ()
            if isinstance(item, dict) and isinstance(item.get("path"), str)
        }
        return bool(
            data
            and data.get("schema_version") == 1
            and data.get("feature") == module
            and data.get("status") == "valid"
            and data.get("manufacturing_authority") is True
            and isinstance(checks, list)
            and checks
            and all(isinstance(check, dict) and check.get("passed") is True for check in checks)
            and isinstance(artifacts, list)
            and artifacts
            and len(artifact_index) == len(artifacts)
            and all(
                path in part_hashes
                and item.get("step_sha256") == part_hashes[path]
                for path, item in artifact_index.items()
            )
        )

    def _part_step_hashes(self, root, tree) -> dict[str, str]:
        hashes = {}
        for item in tree.parts:
            path = root / "manufacturing/parts" / f"{item.path.replace('/', '__')}.step"
            try:
                hashes[item.path] = sha256(path.read_bytes()).hexdigest()
            except OSError:
                continue
        return hashes

    def _position_evidence(self, root, tree) -> FabricationReadinessCheck:
        path = root / "assemblies/full-wardrobe-position-check.json"
        data = self.records.read_json(path)
        assemblies = data.get("assemblies") if data else None
        checks = data.get("checks") if data else None
        valid = bool(
            data
            and data.get("schema_version") == 1
            and data.get("status") == "valid"
            and isinstance(assemblies, dict)
            and assemblies
            and set(tree.root_child_ids).issubset(assemblies)
            and isinstance(data.get("relationships"), dict)
            and isinstance(checks, list)
            and checks
            and all(isinstance(check, dict) and check.get("passed") is True for check in checks)
        )
        return self._check(
            "validation.full_wardrobe_position",
            () if valid else (str(path.relative_to(root)),),
        )

    def _check(self, code, problems) -> FabricationReadinessCheck:
        return FabricationReadinessCheck(code, not problems, tuple(problems))


__all__ = ["FabricationSavedEvidenceChecker"]
