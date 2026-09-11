"""Scope: Check explicit root selection on an actual alternate assembly builder."""

import json

from count_physical_items import CountPhysicalItemsCommand


class TestInventoryAssemblySelection:
    def test_selects_authored_root_instead_of_assuming_wardrobe(self, tmp_path):
        from pathlib import Path
        import shutil

        templates = Path(__file__).resolve().parents[1] / "aikea-build-units/assets/project"
        assemblies = tmp_path / "assemblies"
        assemblies.mkdir()
        (assemblies / "__init__.py").write_text("")
        for name in ("specification.py", "assembly_composition.py", "assembly_placement.py", "assembly_tree.py", "construction_requirement.py"):
            shutil.copy2(templates / name, assemblies / name)
        root = assemblies / "furniture_legs_01"
        root.mkdir()
        (root / "__init__.py").write_text("")
        (root / "builder.py").write_text('''from assemblies.specification import BuiltAssembly, CompositeAssemblySpec
class Builder:
    def build(self):
        return BuiltAssembly(CompositeAssemblySpec("furniture_legs_01", "empty selection probe", ()), (), ())
BUILDER = Builder()
''')
        assert CountPhysicalItemsCommand().run(tmp_path, "furniture_legs_01") == 0
        report = json.loads((tmp_path / "manufacturing/item-counts.json").read_text())
        assert report["totals"]["manufactured_parts"] == 0
