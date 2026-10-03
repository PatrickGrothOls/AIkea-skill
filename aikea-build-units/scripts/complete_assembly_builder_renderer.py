"""Scope: Render one manifest-composed entry point for an assembly."""

from __future__ import annotations


class CompleteAssemblyBuilderRenderer:
    """Keep generated feature discovery separate from the base part builder."""

    def render(self, assembly_id: str) -> str:
        return (
            f'"""Scope: Build {assembly_id} with every registered feature."""\n\n'
            "from pathlib import Path\n"
            "from assemblies.assembly_feature import (\n"
            "    AssemblyFeatureManifestLoader, FeatureComposedAssemblyBuilder,\n"
            ")\n\n"
            "from .builder import BUILDER as BASE_BUILDER\n\n\n"
            "FEATURES = AssemblyFeatureManifestLoader().load(\n"
            "    Path(__file__).with_name('features.json'),\n"
            "    __package__,\n"
            ")\n"
            "BUILDER = FeatureComposedAssemblyBuilder(BASE_BUILDER, FEATURES)\n"
        )


__all__ = ["CompleteAssemblyBuilderRenderer"]
