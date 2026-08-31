"""Scope: Compose an explicit ordered feature list onto one base assembly."""

from __future__ import annotations

from dataclasses import dataclass
import importlib
import json
from pathlib import Path
from typing import Any, Protocol


class AssemblyFeatureManifestError(ValueError):
    """Report an invalid generated cabinet-feature manifest."""


class AssemblyBuilder(Protocol):
    """Build one complete physical assembly."""

    def build(self) -> Any: ...


class AssemblyFeature(Protocol):
    """Apply one owned feature without discarding earlier assembly work."""

    def apply(self, assembly: Any) -> Any: ...


@dataclass(frozen=True)
class FeatureComposedAssemblyBuilder:
    """Apply explicit features in manifest order to one base builder result."""

    base_builder: AssemblyBuilder
    features: tuple[AssemblyFeature, ...]

    def build(self) -> Any:
        assembly = self.base_builder.build()
        for feature in self.features:
            assembly = feature.apply(assembly)
        return assembly


class AssemblyFeatureManifestLoader:
    """Load feature objects named by one cabinet-local JSON manifest."""

    def load(self, path: Path, package: str) -> tuple[AssemblyFeature, ...]:
        if not path.is_file():
            return ()
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or data.get("schema_version") != 1:
            raise AssemblyFeatureManifestError(f"unsupported feature manifest: {path}")
        features = data.get("features")
        if not isinstance(features, list):
            raise AssemblyFeatureManifestError(f"invalid feature manifest: {path}")
        ordered = sorted(features, key=lambda item: (item["order"], item["module"]))
        return tuple(
            importlib.import_module(f"{package}.{item['module']}").FEATURE
            for item in ordered
        )


__all__ = [
    "AssemblyFeature",
    "AssemblyFeatureManifestError",
    "AssemblyFeatureManifestLoader",
    "FeatureComposedAssemblyBuilder",
]
