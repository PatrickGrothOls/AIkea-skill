"""Scope: Verify the authored CLI blocks export when geometry fits but CNC blanks do not."""

import json
from pathlib import Path
import subprocess
import sys

from furniture_design_project import FurnitureDesignProject


class TestFurnitureCncBuild:
    """Run the same public command an independently authored project uses."""

    def test_room_fit_does_not_allow_an_oversized_custom_panel(self, tmp_path):
        FurnitureDesignProject().initialize(tmp_path)
        folder = tmp_path / "assemblies/furniture_01"
        folder.mkdir()
        (folder / "__init__.py").write_text('"""Scope: Own test furniture."""\n')
        (folder / "builder.py").write_text(self.source())
        output = tmp_path / "reviews/furniture_01.glb"
        output.parent.mkdir()
        output.write_bytes(b"older artifact must not be reported as a new export")
        script = Path(__file__).resolve().parents[1] / "aikea-review-unit/scripts/build_furniture_design.py"
        command = subprocess.run([sys.executable, str(script), str(tmp_path)],
                                 capture_output=True, text=True)
        assert command.returncode == 2, command.stderr
        report = json.loads(command.stdout)
        assert report["status"] == "invalid"
        assert report["invalid_solids"] == report["outside_envelope"] == report["overlaps"] == []
        assert report["cnc_check"]["oversized_parts"][0]["blank_size_mm"] == [3940, 465, 18]
        assert "glb" not in report
        assert output.read_bytes() == b"older artifact must not be reported as a new export"
        saved = json.loads(output.with_suffix(".geometry-check.json").read_text())
        assert saved["cnc_check"]["status"] == "invalid"

    def source(self):
        return '''"""Scope: Model an oversized part directly, bypassing panel helpers."""
import cadquery as cq
from assemblies.specification import PartSpec, BuiltPart, BuiltAssembly, IDENTITY_LOCAL_TO_PARENT
from assemblies.panel_assembly import PanelAssemblySpec

class CustomBuilder:
    def build(self):
        spec = PartSpec("deck", "anything", (), IDENTITY_LOCAL_TO_PARENT,
                        local_size_mm=(100, 465, 18))
        solid = cq.Workplane("XY").box(3940, 465, 18, centered=False)
        return BuiltAssembly(PanelAssemblySpec("furniture_01", "custom", (spec,)),
                             (BuiltPart(spec, solid),), ())

BUILDER = CustomBuilder()
ENVELOPE = cq.Workplane("XY").box(4000, 500, 100, centered=False)
'''

    def test_direct_builder_cannot_hide_an_axis_with_short_dimensions(self, tmp_path):
        FurnitureDesignProject().initialize(tmp_path)
        folder = tmp_path / "assemblies/furniture_01"
        folder.mkdir()
        (folder / "__init__.py").write_text('"""Scope: Own test furniture."""\n')
        source = self.source().replace("(100, 465, 18)", "(100, 100)")
        source = source.replace("box(3940, 465, 18", "box(100, 100, 3000")
        source = source.replace("box(4000, 500, 100", "box(150, 150, 4000")
        (folder / "builder.py").write_text(source)
        script = Path(__file__).resolve().parents[1] / "aikea-review-unit/scripts/build_furniture_design.py"
        command = subprocess.run([sys.executable, str(script), str(tmp_path)],
                                 capture_output=True, text=True)
        assert command.returncode != 0
        assert "three finite positive dimensions" in command.stderr
        assert not (tmp_path / "reviews/furniture_01.glb").exists()
