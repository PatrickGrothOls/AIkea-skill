"""Scope: Run the approved presentation stages and require geometry proof before delivery."""

import hashlib
import json
from pathlib import Path
import bpy
from blender_furniture_source import BlenderFurnitureSource
from blender_furniture_studio import BlenderFurnitureStudio
from lighting_atlas import LightingAtlas
from bake_uv_coverage import BakeUvCoverage
from panel_bake_pass import PanelBakePass
from blender_export_verification import ExportGeometryVerification


class BlenderBakeJob:
    def __init__(self, directory):
        self.directory = Path(directory)
        self.config = json.loads((self.directory / "job.json").read_text())

    def run(self):
        path = Path(self.config["source"])
        if hashlib.sha256(path.read_bytes()).hexdigest() != self.config["source_sha256"]:
            raise ValueError("Source GLB changed after this bake was requested")
        source = BlenderFurnitureSource(path, self.config["unit_scale"]).load()
        names = [obj.name for obj in source.parts]
        panel_names = [obj.name for obj in source.panels]
        studio = BlenderFurnitureStudio(source)
        studio.build()
        studio.prepare_viewport()
        bpy.ops.file.pack_all()
        bpy.ops.wm.save_as_mainfile(filepath=str(self.directory / "source-studio.blend"))
        atlas = LightingAtlas(source.panels, self.config["atlas_size"])
        atlas.prepare()
        BakeUvCoverage(source.panels, self.config["atlas_size"]).apply(self.directory / "uv-layout.json")
        source.verify(self.directory / "prepared-geometry.json")
        bpy.ops.wm.save_as_mainfile(filepath=str(self.directory / "bake-ready.blend"))
        bake = PanelBakePass(self.directory, self.config["threads"], self.config["samples"])
        bake.run(white=True)
        bake.run()
        # The baking mesh was temporary. Reload all original, separate physical parts.
        bpy.ops.wm.open_mainfile(filepath=str(self.directory / "bake-ready.blend"))
        source.parts = [bpy.data.objects[name] for name in names]
        source.panels = [bpy.data.objects[name] for name in panel_names]
        atlas.panels = source.panels
        atlas.image = bpy.data.images.load(str(self.directory / "assembled-lighting.png"))
        atlas.apply()
        source.verify(self.directory / "shaded-geometry.json")
        bpy.context.scene.render.engine = "BLENDER_EEVEE"
        bpy.ops.file.pack_all()
        bpy.ops.wm.save_as_mainfile(filepath=str(self.directory / "assembled.blend"))
        self.export(source)
        ExportGeometryVerification().run(path, self.directory / "assembled.glb",
                                         self.directory / "export-geometry.json", source.unit_scale)
        self.complete()

    def export(self, source):
        bpy.ops.object.select_all(action="DESELECT")
        roots = set()
        for obj in source.parts:
            obj.select_set(True)
            root = obj
            while root.parent:
                root = root.parent
                root.select_set(True)
            roots.add(root)
        for root in roots:
            root.scale /= source.unit_scale
        bpy.context.view_layer.update()
        bpy.ops.export_scene.gltf(filepath=str(self.directory / "assembled.glb"),
                                  export_format="GLB", use_selection=True, export_extras=True,
                                  export_animations=False, export_cameras=False, export_lights=False)

    def complete(self):
        names = ("prepared-geometry", "all-panel-coverage", "shaded-geometry", "export-geometry")
        reports = {name: json.loads((self.directory / f"{name}.json").read_text()) for name in names}
        if any(report["status"] != "PASS" for report in reports.values()):
            raise RuntimeError("A required bake check failed; do not deliver assembled.glb")
        model = self.directory / "assembled.glb"
        report = dict(self.config, status="PASS", blender_version=bpy.app.version_string,
                      assembled_model=model.name,
                      assembled_sha256=hashlib.sha256(model.read_bytes()).hexdigest(),
                      inspection_model=self.config["source"], presentation_state="assembled_only",
                      physical_parts=reports["export-geometry"]["physical_parts"],
                      uncovered_triangle_centroids=reports["all-panel-coverage"]["uncovered_centroids"],
                      maximum_vertex_error_mm=reports["export-geometry"]["maximum_vertex_error_mm"],
                      checks=[f"{name}.json" for name in names], manufacturing_authority=False)
        (self.directory / "presentation.json").write_text(json.dumps(report, indent=2))
        print("PRESENTATION_READY", model, flush=True)
