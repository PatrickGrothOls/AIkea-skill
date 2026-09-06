"""Scope: Resolve manifest-owned feature modules to exact physical part paths."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from fabrication_record_validator import FabricationRecordValidator


@dataclass(frozen=True, slots=True)
class FabricationFeatureScope:
    """Bind one registered feature to its evidence file and expected parts."""

    module: str
    evidence_path: Path
    expected_paths: tuple[str, ...]


class FabricationFeatureScopeResolver:
    """Match one generated manifest to one unambiguous assembly-tree owner."""

    _ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*_[0-9]{2}$")

    def __init__(self) -> None:
        self.records = FabricationRecordValidator()

    def resolve(
        self,
        root: Path,
        manifest_path: Path,
        assembly_paths: tuple[str, ...],
    ) -> tuple[FabricationFeatureScope, ...] | None:
        manifest = self.records.read_json(manifest_path)
        features = manifest.get("features") if manifest else None
        owner = self._owner_path(root, manifest_path, assembly_paths)
        if (
            manifest is None
            or manifest.get("schema_version") != 1
            or not isinstance(features, list)
            or owner is None
        ):
            return None
        scopes = tuple(self._scope(manifest_path, owner, item) for item in features)
        return scopes if all(scopes) else None

    def _scope(self, manifest_path, owner, feature):
        if not isinstance(feature, dict) or not isinstance(feature.get("module"), str):
            return None
        relative_paths = feature.get("affected_manufactured_part_paths")
        if not isinstance(relative_paths, list) or any(
            not isinstance(path, str) or not path for path in relative_paths
        ):
            return None
        expected = tuple(f"{owner}/{path}" for path in relative_paths)
        if len(set(expected)) != len(expected):
            return None
        module = feature["module"]
        evidence_path = manifest_path.parent / "fabrication-evidence" / (
            module.replace(".", "-") + ".json"
        )
        return FabricationFeatureScope(module, evidence_path, expected)

    def _owner_path(self, root, manifest_path, assembly_paths) -> str | None:
        lineage = self._lineage(root / "assemblies", manifest_path)
        candidates = tuple(
            path
            for path in assembly_paths
            if lineage and self._lineage_matches(lineage, tuple(path.split("/")))
        )
        return candidates[0] if len(candidates) == 1 else None

    def _lineage_matches(
        self,
        lineage: tuple[str, ...],
        physical_path: tuple[str, ...],
    ) -> bool:
        valid_lineages = {physical_path}
        if len(physical_path) > 1:
            valid_lineages.add(physical_path[1:])
        return lineage in valid_lineages

    def _lineage(self, assemblies_root, manifest_path) -> tuple[str, ...]:
        lineage = []
        current = assemblies_root
        for segment in manifest_path.parent.relative_to(assemblies_root).parts:
            current /= segment
            if self._ID_PATTERN.fullmatch(segment) and (current / "spec.py").is_file():
                lineage.append(segment)
        return tuple(lineage)


__all__ = ["FabricationFeatureScope", "FabricationFeatureScopeResolver"]
