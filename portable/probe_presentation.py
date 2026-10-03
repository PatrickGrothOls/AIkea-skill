"""Scope: Prepare a synthetic material and exercise the real geometry-checked Blender bake."""

import hashlib
import json
from pathlib import Path
import sys

import bpy


class PresentationProbe:
    def run(self, directory, package):
        sys.path.insert(0, str(package / "skills/aikea-review-unit/scripts"))
        from blender_export_verification import ExportGeometryVerification
        from blender_bake_job import BlenderBakeJob
        from probe_blender_engine import BlenderEngineProbe
        BlenderEngineProbe().run()
        raw = directory / "probe.glb"
        bpy.ops.import_scene.gltf(filepath=str(raw))
        for obj in bpy.context.scene.objects:
            if obj.type != "MESH":
                continue
            uv = obj.data.uv_layers.new(name="ProbeMaterialUV")
            for polygon in obj.data.polygons:
                axis = max(range(3), key=lambda value: abs(polygon.normal[value]))
                axes = [value for value in range(3) if value != axis]
                for index in polygon.loop_indices:
                    point = obj.data.vertices[obj.data.loops[index].vertex_index].co
                    uv.data[index].uv = (point[axes[0]] / 200, point[axes[1]] / 200)
            for material in obj.data.materials:
                material.use_nodes = True
        prepared = directory / "material.glb"
        bpy.ops.export_scene.gltf(filepath=str(prepared), export_format="GLB",
                                  export_extras=True, export_animations=False,
                                  export_cameras=False, export_lights=False)
        ExportGeometryVerification().run(raw, prepared, directory / "material-proof.json", 0.001)
        output = directory / "presentation"
        output.mkdir()
        config = {"source": str(prepared), "source_sha256": hashlib.sha256(prepared.read_bytes()).hexdigest(),
                  "unit_scale": 0.001, "atlas_size": 4096, "threads": 1, "samples": 16}
        (output / "job.json").write_text(json.dumps(config))
        BlenderBakeJob(output).run()


if __name__ == "__main__":
    PresentationProbe().run(Path(sys.argv[1]), Path(sys.argv[2]))
