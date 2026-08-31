"""Scope: Render a compatibility builder for one registered cabinet feature."""

from __future__ import annotations


class CabinetFeatureBuilderWrapperRenderer:
    """Expose one feature on the historical named-builder boundary."""

    def render(self, assembly_id: str, feature_module: str) -> str:
        return (
            f'"""Scope: Build {assembly_id} with the {feature_module} feature."""\n\n'
            "from assemblies.assembly_feature import FeatureComposedAssemblyBuilder\n\n"
            "from .builder import BUILDER as BASE_BUILDER\n"
            f"from .{feature_module} import FEATURE\n\n\n"
            "BUILDER = FeatureComposedAssemblyBuilder(BASE_BUILDER, (FEATURE,))\n"
        )


__all__ = ["CabinetFeatureBuilderWrapperRenderer"]
