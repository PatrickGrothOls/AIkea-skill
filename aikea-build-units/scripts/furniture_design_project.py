"""Scope: Install shared assembly contracts without choosing a furniture design."""

from pathlib import Path

from assembly_taxonomy_writer import AssemblyTaxonomyWriter


class FurnitureDesignProject:
    """Create only shared contracts, preserving every differing local file."""

    CONTRACTS = (
        "assembly_composition.py", "assembly_feature.py", "assembly_placement.py",
        "assembly_tree.py", "specification.py", "construction_specification.py",
        "construction_requirement.py", "contact_allowance.py", "panel_assembly.py",
    )

    def initialize(self, project_root: Path) -> tuple[Path, ...]:
        assets = Path(__file__).resolve().parents[1] / "assets/project"
        files = {
            Path("assemblies") / name: (assets / name).read_text()
            for name in self.CONTRACTS
        }
        if not (project_root / "assemblies/__init__.py").exists():
            files[Path("assemblies/__init__.py")] = (
                '"""Scope: Own this project\'s designed furniture assemblies."""\n'
            )
        return AssemblyTaxonomyWriter().write(project_root, files)
