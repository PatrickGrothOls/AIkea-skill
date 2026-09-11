"""Scope: Execute one authored furniture tree, check its solids and export its review."""

import argparse
import importlib
import json
from pathlib import Path
import re
import sys

BUILD_SCRIPTS = Path(__file__).resolve().parents[2] / "aikea-build-units/scripts"
sys.path.insert(0, str(BUILD_SCRIPTS))

from assembly_tree_review_geometry import AssemblyTreeReviewGeometry  # noqa: E402
from cadquery_glb_exporter import CadQueryGlbExporter  # noqa: E402
from furniture_geometry_check import FurnitureGeometryCheck  # noqa: E402
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader  # noqa: E402


class FurnitureDesignBuild:
    """Consume the same assembly contract for any project-authored furniture."""

    def __init__(self) -> None:
        self.loader = GeneratedAssemblyBuilderLoader()

    def build(self, project_root: Path, assembly_id: str, output: Path) -> dict:
        if not re.fullmatch(r"[a-z][a-z0-9_]*_[0-9]{2}", assembly_id):
            raise ValueError("use a stable assembly ID such as furniture_01")
        built, envelope = self.loader.runtime.execute(
            project_root, lambda: self._build_definition(assembly_id)
        )
        visits = self.loader.walk(project_root, built)
        paths = tuple(item.path for item in visits)
        if len(paths) != len(set(paths)):
            raise ValueError("assembly tree paths must be unique")
        parts = AssemblyTreeReviewGeometry().build(visits, {})
        report = FurnitureGeometryCheck().check(parts, envelope)
        report["assembly_id"] = assembly_id
        report["assembly_count"] = sum(
            type(item).__name__ == "AssemblyTreeAssembly" for item in visits
        )
        output.parent.mkdir(parents=True, exist_ok=True)
        report_path = output.with_suffix(".geometry-check.json")
        report_path.write_text(json.dumps(report, indent=2) + "\n")
        if not report["invalid_solids"]:
            CadQueryGlbExporter().export(assembly_id, parts, output)
            report["glb"] = str(output)
        report["geometry_check"] = str(report_path)
        return report

    def _build_definition(self, assembly_id: str):
        definition = importlib.import_module(f"assemblies.{assembly_id}.builder")
        return definition.BUILDER.build(), definition.ENVELOPE


class FurnitureDesignBuildCommand:
    """Expose project execution and evidence paths without imposing a design type."""

    def run(self) -> int:
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("project", type=Path)
        parser.add_argument("--assembly", default="furniture_01")
        parser.add_argument("--output", type=Path)
        args = parser.parse_args()
        project = args.project.resolve()
        output = args.output or project / "reviews" / f"{args.assembly}.glb"
        report = FurnitureDesignBuild().build(project, args.assembly, output.resolve())
        print(json.dumps(report, indent=2))
        return 0 if report["status"] == "valid" else 2


if __name__ == "__main__":
    raise SystemExit(FurnitureDesignBuildCommand().run())
