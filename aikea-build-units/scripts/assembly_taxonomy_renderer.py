"""Scope: Compose every file required by a resolved assembly taxonomy."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from assembly_module_renderer import AssemblyModuleRenderer
from assembly_spec_renderer import AssemblySpecRenderer
from assembly_taxonomy import (
    BaseAssemblyTaxonomy,
    LocalAssemblyTaxonomy,
    ProjectAssemblyTaxonomy,
)
from complete_assembly_builder_renderer import CompleteAssemblyBuilderRenderer
from wardrobe_assembly_renderer import WardrobeAssemblyRenderer


class AssemblyTaxonomyRenderer:
    """Render a complete project tree before any file is changed."""

    _PROJECT_CONTRACT_FILES = (
        "assembly_composition.py",
        "assembly_feature.py",
        "assembly_placement.py",
        "assembly_tree.py",
        "specification.py",
    )

    def __init__(self, asset_root: Path) -> None:
        self.asset_root = asset_root
        self.modules = AssemblyModuleRenderer()
        self.complete_builder = CompleteAssemblyBuilderRenderer()
        self.specs = AssemblySpecRenderer()
        self.wardrobe = WardrobeAssemblyRenderer()

    def render(self, taxonomy: ProjectAssemblyTaxonomy) -> dict[Path, str]:
        files = {
            Path("assemblies/__init__.py"): self.modules.package(
                "Contain generated local furniture assemblies"
            ),
        }
        files.update(self._project_contract_files())
        for assembly in taxonomy.assemblies:
            files.update(self._assembly_files(assembly))
        if taxonomy.wardrobe:
            files.update(self.wardrobe.render(taxonomy.wardrobe))
        return files

    def render_metadata_scaffold(
        self, taxonomy: ProjectAssemblyTaxonomy
    ) -> dict[Path, str]:
        files = {
            Path("assemblies/specification.py"): (
                self.asset_root / "metadata_plan_specification.py"
            ).read_text(encoding="utf-8"),
        }
        for assembly in taxonomy.assemblies:
            root = Path("assemblies") / assembly.assembly_id
            files[root / "builder.py"] = self.modules.metadata_assembly_builder(
                assembly
            )
            for part in assembly.parts:
                files[
                    root / "parts" / part.part_id / "builder.py"
                ] = self.modules.metadata_part_builder(assembly.assembly_id, part)
        return files

    def render_known_previous_files(
        self, taxonomy: ProjectAssemblyTaxonomy
    ) -> dict[Path, tuple[str, ...]]:
        previous_sets = (
            self.render_metadata_scaffold(taxonomy),
            self.render_without_adjustable_shelves(taxonomy),
        )
        paths = {path for files in previous_sets for path in files}
        return {
            path: tuple(files[path] for files in previous_sets if path in files)
            for path in paths
        }

    def render_without_adjustable_shelves(
        self, taxonomy: ProjectAssemblyTaxonomy
    ) -> dict[Path, str]:
        assemblies = tuple(
            replace(
                assembly,
                parts=tuple(
                    part for part in assembly.parts if part.role != "shelf_panel"
                ),
            )
            if isinstance(assembly, LocalAssemblyTaxonomy)
            else assembly
            for assembly in taxonomy.assemblies
        )
        return self.render(ProjectAssemblyTaxonomy(assemblies, taxonomy.wardrobe))

    def _assembly_files(
        self, assembly: LocalAssemblyTaxonomy | BaseAssemblyTaxonomy
    ) -> dict[Path, str]:
        root = Path("assemblies") / assembly.assembly_id
        files = {
            root / "__init__.py": self.modules.package(
                f"Contain the {assembly.assembly_id} local assembly"
            ),
            root / "spec.py": self.specs.render(assembly),
            root / "builder.py": self.modules.assembly_builder(assembly),
            root / "complete_builder.py": self.complete_builder.render(
                assembly.assembly_id
            ),
            root / "joints/__init__.py": self.modules.package(
                f"Contain joints owned by {assembly.assembly_id}"
            ),
            root / "joints/spec.py": self.modules.joints_spec(assembly.assembly_id),
            root / "parts/__init__.py": self.modules.package(
                f"Contain parts owned by {assembly.assembly_id}"
            ),
        }
        for part in assembly.parts:
            part_root = root / "parts" / part.part_id
            files[part_root / "__init__.py"] = self.modules.package(
                f"Contain the {part.part_id} manufactured part"
            )
            files[part_root / "spec.py"] = self.modules.part_spec(
                assembly.assembly_id, part
            )
            files[part_root / "builder.py"] = self.modules.part_builder(
                assembly.assembly_id, part
            )
        return files

    def _project_contract_files(self) -> dict[Path, str]:
        return {
            Path("assemblies") / filename: (
                self.asset_root / filename
            ).read_text(encoding="utf-8")
            for filename in self._PROJECT_CONTRACT_FILES
        }
