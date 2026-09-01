"""Scope: Validate exact feature-owned manufacturing evidence recursively."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path

from fabrication_feature_scope_resolver import FabricationFeatureScopeResolver
from fabrication_readiness_report import FabricationReadinessCheck
from fabrication_record_validator import FabricationRecordValidator


class FabricationFeatureEvidenceChecker:
    """Bind each feature report to its declared owner-relative part scope."""

    def __init__(self) -> None:
        self.records = FabricationRecordValidator()
        self.scopes = FabricationFeatureScopeResolver()

    def check(self, root, tree, visits) -> FabricationReadinessCheck:
        part_hashes = self._part_step_hashes(root, tree)
        assembly_paths = tuple(
            self._path(item.path)
            for item in visits
            if type(item).__name__ == "AssemblyTreeAssembly"
        )
        problems = tuple(
            str(evidence_path.relative_to(root))
            for manifest_path in sorted((root / "assemblies").rglob("features.json"))
            for evidence_path in self._invalid_evidence_paths(
                root,
                manifest_path,
                assembly_paths,
                part_hashes,
            )
        )
        return FabricationReadinessCheck(
            "pack.feature_manufacturing_evidence",
            not problems,
            problems,
        )

    def _invalid_evidence_paths(
        self,
        root,
        manifest_path,
        assembly_paths: tuple[str, ...],
        part_hashes: dict[str, str],
    ) -> tuple[Path, ...]:
        scopes = self.scopes.resolve(root, manifest_path, assembly_paths)
        if scopes is None:
            return (manifest_path,)
        invalid = []
        for scope in scopes:
            data = self.records.read_json(scope.evidence_path)
            if not self._valid_evidence(
                data,
                scope.module,
                scope.expected_paths,
                part_hashes,
            ):
                invalid.append(scope.evidence_path)
        return tuple(invalid)

    def _valid_evidence(self, data, module, expected, part_hashes) -> bool:
        checks = data.get("checks") if data else None
        artifacts = data.get("part_artifacts") if data else None
        index = {
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
            and len(index) == len(artifacts)
            and set(index) == set(expected)
            and all(
                path in part_hashes
                and item.get("step_sha256") == part_hashes[path]
                for path, item in index.items()
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

    def _path(self, path: tuple[str, ...]) -> str:
        return "/".join(segment.split(":", 1)[-1] for segment in path)


__all__ = ["FabricationFeatureEvidenceChecker"]
