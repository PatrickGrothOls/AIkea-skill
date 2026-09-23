"""Scope: Prove a CAD-colour panel lights after import and a metallic-only diffuse bake fails."""

import hashlib
import json
from pathlib import Path
import sys

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'aikea-review-unit/scripts'))
from blender_bake_job import BlenderBakeJob


class CadPanelBakeAcceptance:
    def run(self, raw, root):
        root.mkdir(parents=True, exist_ok=True)
        results = {}
        for mode, metallic in [('nonmetal', 0.0), ('metallic', 1.0)]:
            bpy.ops.wm.read_factory_settings(use_empty=True)
            bpy.ops.import_scene.gltf(filepath=str(raw))
            for obj in bpy.context.scene.objects:
                if obj.type != 'MESH':
                    continue
                for material in obj.data.materials:
                    bsdf = material.node_tree.nodes.get('Principled BSDF')
                    assert bsdf.inputs['Metallic'].default_value == 0.0
                    bsdf.inputs['Metallic'].default_value = metallic
                uv = obj.data.uv_layers.new(name='SourceUV')
                for polygon in obj.data.polygons:
                    normal_axis = max(range(3), key=lambda axis: abs(polygon.normal[axis]))
                    axes = [axis for axis in range(3) if axis != normal_axis]
                    for index in polygon.loop_indices:
                        point = obj.data.vertices[obj.data.loops[index].vertex_index].co
                        uv.data[index].uv = (point[axes[0]] / 200, point[axes[1]] / 200)
            source = root / f'{mode}.glb'
            bpy.ops.export_scene.gltf(filepath=str(source), export_format='GLB', export_extras=True)
            output = root / mode
            output.mkdir()
            config = dict(source=str(source), source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                          unit_scale=0.001, atlas_size=1024, threads=1, samples=1)
            (output / 'job.json').write_text(json.dumps(config))
            if mode == 'metallic':
                # Known reproduced failure: a metallic source has no diffuse lighting signal.
                try:
                    BlenderBakeJob(output).run()
                except ValueError as error:
                    assert 'Empty or invalid panel lighting bake' in str(error), str(error)
                else:
                    raise AssertionError('Empty diffuse bake was accepted')
                assert not (output / 'presentation.json').exists()
            else:
                BlenderBakeJob(output).run()
                assert json.loads((output / 'presentation.json').read_text())['status'] == 'PASS'
            signal = json.loads((output / 'lighting-signal.json').read_text())
            results[mode] = signal
        (root / 'acceptance.json').write_text(json.dumps(results, indent=2))
        print('CAD_PANEL_BAKE_ACCEPTANCE_PASS', json.dumps(results), flush=True)


if __name__ == '__main__':
    arguments = sys.argv[sys.argv.index('--') + 1:]
    CadPanelBakeAcceptance().run(Path(arguments[0]), Path(arguments[1]))
