"""Scope: Validate installed CAD versions and export a small labelled test panel."""

import importlib.metadata
import json
from pathlib import Path
import sys

import cadquery as cq


class CadProbe:
    def run(self, output, package):
        versions = {name: importlib.metadata.version(name)
                    for name in ("cadquery", "vtk", "PyYAML")}
        expected = {"cadquery": "2.7.0", "vtk": "9.3.1", "PyYAML": "6.0.2"}
        if versions != expected:
            raise ValueError(f"Unexpected CAD runtime: {versions}")
        sys.path.insert(0, str(package / "skills/aikea-review-unit/scripts"))
        from cadquery_glb_exporter import CadQueryGlbExporter
        from unit_mockup import MockupPart
        panel = cq.Workplane("XY").box(200, 100, 16)
        if not panel.val().isValid() or abs(panel.val().Volume() - 320000) > 1e-6:
            raise ValueError("CAD solid validity/volume probe failed")
        cq.exporters.export(panel, str(output / "probe.step"))
        imported = cq.importers.importStep(str(output / "probe.step")).val()
        if not imported.isValid() or abs(imported.Volume() - 320000) > 1e-6:
            raise ValueError("STEP round trip failed")
        part = MockupPart("test_panel", panel, cq.Location(), (0.6, 0.5, 0.3, 1),
                         inspection_path=("setup_probe", "test_panel"), review_kind="panel")
        CadQueryGlbExporter().export("setup_probe", (part,), output / "probe.glb")
        (output / "cad.json").write_text(json.dumps({"status": "PASS", "versions": versions,
                                                    "volume_mm3": imported.Volume()}))


if __name__ == "__main__":
    CadProbe().run(Path(sys.argv[1]), Path(sys.argv[2]))
