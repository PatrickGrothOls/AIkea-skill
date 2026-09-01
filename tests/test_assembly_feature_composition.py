"""Scope: Verify explicit feature manifests drive one complete assembly builder."""

from __future__ import annotations

import importlib
import json
import sys

from assembly_composition_test_case import AssemblyCompositionTestCase
from cabinet_feature_manifest import CabinetFeatureManifest
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader


class TestAssemblyFeatureComposition(AssemblyCompositionTestCase):
    """Protect ordered generic composition independently of furniture features."""

    def test_composed_builder_applies_features_in_declared_order(
        self, generated_values
    ) -> None:
        _values, _ = generated_values
        feature_contract = importlib.import_module("assemblies.assembly_feature")
        events = []

        class BaseBuilder:
            def build(self):
                return ("base",)

        class Feature:
            def __init__(self, name):
                self.name = name

            def apply(self, assembly):
                events.append(self.name)
                return assembly + (self.name,)

        builder = feature_contract.FeatureComposedAssemblyBuilder(
            BaseBuilder(),
            (Feature("drawers"), Feature("doors"), Feature("lighting")),
        )

        assert builder.build() == ("base", "drawers", "doors", "lighting")
        assert events == ["drawers", "doors", "lighting"]

    def test_manifest_registration_is_stable_and_ordered(self, tmp_path) -> None:
        manifest = CabinetFeatureManifest()

        manifest.register(tmp_path, "cabinet_01", "lighting.feature", 30)
        manifest.register(tmp_path, "cabinet_01", "drawers.feature", 10)
        manifest.register(tmp_path, "cabinet_01", "door_hinges.feature", 20)
        manifest.register(tmp_path, "cabinet_01", "drawers.feature", 10)

        path = tmp_path / "assemblies/cabinet_01/features.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["features"] == [
            {
                "module": "drawers.feature",
                "order": 10,
                "affected_manufactured_part_paths": [],
            },
            {
                "module": "door_hinges.feature",
                "order": 20,
                "affected_manufactured_part_paths": [],
            },
            {
                "module": "lighting.feature",
                "order": 30,
                "affected_manufactured_part_paths": [],
            },
        ]

    def test_manifest_can_register_an_optional_review_adapter(self, tmp_path) -> None:
        manifest = CabinetFeatureManifest()

        manifest.register(
            tmp_path,
            "cabinet_01",
            "door_hinges.feature",
            20,
            review_module="door_hinges.review",
        )

        path = tmp_path / "assemblies/cabinet_01/features.json"
        assert json.loads(path.read_text())["features"] == [
            {
                "module": "door_hinges.feature",
                "order": 20,
                "review_module": "door_hinges.review",
                "affected_manufactured_part_paths": [],
            }
        ]

    def test_generated_assemblies_expose_complete_builder(self, generated_values) -> None:
        _values, project_root = generated_values

        assert (project_root / "assemblies/assembly_feature.py").is_file()
        source = (
            project_root / "assemblies/tall_storage_01/complete_builder.py"
        ).read_text(encoding="utf-8")
        assert "FeatureComposedAssemblyBuilder" in source
        assert "features.json" in source

    def test_review_loader_prefers_complete_builder_with_feature_runtime(
        self, tmp_path, monkeypatch
    ) -> None:
        project_root = tmp_path / "project"
        assembly_root = project_root / "assemblies/cabinet_01"
        runtime_root = tmp_path / "feature_runtime"
        assembly_root.mkdir(parents=True)
        runtime_root.mkdir()
        (project_root / "assemblies/__init__.py").write_text("", encoding="utf-8")
        (assembly_root / "__init__.py").write_text("", encoding="utf-8")
        (assembly_root / "builder.py").write_text(
            "class Builder:\n    def build(self): return 'base'\nBUILDER = Builder()\n",
            encoding="utf-8",
        )
        (assembly_root / "complete_builder.py").write_text(
            "from feature_runtime_probe import BUILDER\n",
            encoding="utf-8",
        )
        (runtime_root / "feature_runtime_probe.py").write_text(
            "class Builder:\n    def build(self): return 'complete'\nBUILDER = Builder()\n",
            encoding="utf-8",
        )
        loader = GeneratedAssemblyBuilderLoader()
        monkeypatch.setattr(
            loader.runtime,
            "_skill_runtime_paths",
            lambda: (str(runtime_root),),
        )
        try:
            assert loader.load_assembly(project_root, "cabinet_01") == "complete"
        finally:
            sys.modules.pop("feature_runtime_probe", None)
