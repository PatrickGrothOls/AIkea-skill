"""Scope: Coordinate assembly taxonomy calculation, rendering, and safe writing."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from assembly_taxonomy import ProjectAssemblyTaxonomy
from assembly_taxonomy_renderer import AssemblyTaxonomyRenderer
from assembly_taxonomy_resolver import AssemblyTaxonomyResolver
from assembly_taxonomy_writer import AssemblyTaxonomyWriter
from generated_file_record import GeneratedFileRecord


class AssemblyTaxonomyGenerator:
    """Provide one deterministic entry point for local unit folder generation."""

    def __init__(self) -> None:
        asset_root = Path(__file__).resolve().parents[1] / "assets" / "project"
        self.resolver = AssemblyTaxonomyResolver()
        self.renderer = AssemblyTaxonomyRenderer(asset_root)
        self.writer = AssemblyTaxonomyWriter()

    def generate(
        self, project: dict[str, Any], project_root: Path
    ) -> ProjectAssemblyTaxonomy:
        taxonomy = self.resolver.resolve(project)
        files = self.renderer.render(taxonomy)
        replaceable = self.renderer.render_known_previous_files(taxonomy)
        recorded = GeneratedFileRecord.load(project_root)
        self.writer.write(project_root, files, replaceable, recorded)
        GeneratedFileRecord.from_rendered(files).save(project_root)
        return taxonomy
