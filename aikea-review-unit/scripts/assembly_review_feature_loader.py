"""Scope: Resolve and import review features for one assembly-tree owner path."""

from __future__ import annotations

import importlib
import json
from pathlib import Path
import re

from assembly_feature_review import RegisteredAssemblyFeatureReview
from generated_project_module_runtime import GeneratedProjectModuleRuntime
from unit_mockup import UnitMockupInputError


class AssemblyReviewFeatureLoader:
    """Match feature manifests by generated assembly lineage, not leaf ID alone."""

    _ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*_[0-9]{2}$")

    def __init__(self, runtime: GeneratedProjectModuleRuntime | None = None) -> None:
        self.runtime = runtime or GeneratedProjectModuleRuntime()

    def load(
        self,
        project_root: Path,
        owner_path: tuple[str, ...],
    ) -> tuple[RegisteredAssemblyFeatureReview, ...]:
        manifest_path = self._resolve_manifest(project_root, owner_path)
        if manifest_path is None:
            return ()
        registrations = self._registrations(manifest_path)
        package = ".".join(manifest_path.parent.relative_to(project_root).parts)
        return self.runtime.execute(
            project_root,
            lambda: tuple(
                RegisteredAssemblyFeatureReview(
                    feature_id,
                    importlib.import_module(f"{package}.{module}").REVIEW,
                )
                for feature_id, module in registrations
            ),
        )

    def _resolve_manifest(
        self,
        project_root: Path,
        owner_path: tuple[str, ...],
    ) -> Path | None:
        assemblies_root = project_root / "assemblies"
        candidates = tuple(
            manifest
            for manifest in sorted(assemblies_root.rglob("features.json"))
            if self._matches_owner(assemblies_root, manifest, owner_path)
        )
        if not candidates:
            return None
        strongest_length = max(
            len(self._lineage(assemblies_root, path)) for path in candidates
        )
        strongest = tuple(
            path
            for path in candidates
            if len(self._lineage(assemblies_root, path)) == strongest_length
        )
        if len(strongest) != 1:
            raise UnitMockupInputError(
                [f"assembly review source is ambiguous: {'/'.join(owner_path)}"]
            )
        return strongest[0]

    def _matches_owner(
        self,
        assemblies_root: Path,
        manifest_path: Path,
        owner_path: tuple[str, ...],
    ) -> bool:
        lineage = self._lineage(assemblies_root, manifest_path)
        valid_lineages = {owner_path}
        if len(owner_path) > 1:
            valid_lineages.add(owner_path[1:])
        return bool(lineage and lineage in valid_lineages)

    def _lineage(
        self,
        assemblies_root: Path,
        manifest_path: Path,
    ) -> tuple[str, ...]:
        lineage = []
        current = assemblies_root
        for segment in manifest_path.parent.relative_to(assemblies_root).parts:
            current /= segment
            if self._ID_PATTERN.fullmatch(segment) and (current / "spec.py").is_file():
                lineage.append(segment)
        return tuple(lineage)

    def _registrations(self, path: Path) -> tuple[tuple[str, str], ...]:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise UnitMockupInputError([f"invalid feature manifest: {path}"]) from error
        if not isinstance(data, dict) or data.get("schema_version") != 1:
            raise UnitMockupInputError([f"unsupported feature manifest: {path}"])
        features = data.get("features")
        if not isinstance(features, list):
            raise UnitMockupInputError([f"invalid feature manifest: {path}"])
        return tuple(
            (item["module"].split(".", 1)[0], item["review_module"])
            for item in features
            if isinstance(item, dict) and item.get("review_module")
        )


__all__ = ["AssemblyReviewFeatureLoader"]
