"""Scope: Exercise real engine baking and reject changed geometry on a small independent assembly."""

import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'aikea-review-unit/scripts'))
import bpy
from blender_bake_job import BlenderBakeJob
from blender_export_verification import ExportGeometryVerification
from probe_blender_engine import BlenderEngineProbe


class TestBlenderBakeAcceptance(unittest.TestCase):
    def fixture(self, path):
        BlenderEngineProbe().run()
        for name, size, position, kind, color in (
            ('top', (800, 400, 16), (0, 0, 500), 'panel', (0.6, 0.4, 0.2, 1)),
            ('back', (780, 6, 450), (0, 190, 267), 'panel', (0.3, 0.2, 0.1, 1)),
            ('fitting', (4, 12, 4), (300, -100, 488), 'hardware', (0.2, 0.2, 0.2, 1))):
            bpy.ops.mesh.primitive_cube_add(size=1, location=position)
            obj = bpy.context.object
            obj.name = name
            obj.dimensions = size
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            obj['aikea'] = {'kind': kind, 'inspection_path': ['independent_fixture', name]}
            material = bpy.data.materials.new(name)
            material.use_nodes = True
            material.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = color
            material['aikea'] = {'material_id': name}
            obj.data.materials.append(material)
            if name == 'top':
                # This roundover belongs to the source fixture, before the presentation begins.
                bevel = obj.modifiers.new('physical source roundover', 'BEVEL')
                bevel.width = 0.4
                bevel.segments = 3
                bpy.ops.object.modifier_apply(modifier=bevel.name)
        bpy.ops.export_scene.gltf(filepath=str(path), export_format='GLB', export_extras=True)

    def test_bake_preserves_parts_and_rejects_tampering(self):
        with tempfile.TemporaryDirectory(prefix='aikea-bake-acceptance-') as directory:
            root = Path(directory)
            source = root / 'source.glb'
            self.fixture(source)
            config = {'source': str(source), 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                      'unit_scale': 0.001, 'atlas_size': 1024, 'threads': 2, 'samples': 1}
            (root / 'job.json').write_text(json.dumps(config))
            BlenderBakeJob(root).run()
            report = json.loads((root / 'presentation.json').read_text())
            self.assertEqual(report['status'], 'PASS')
            self.assertEqual(report['physical_parts'], 3)
            self.assertEqual(report['uncovered_triangle_centroids'], 0)
            geometry = json.loads((root / 'prepared-geometry.json').read_text())
            self.assertTrue(geometry['source_uvs_unchanged'])
            # The verifier's successful round trip is not enough: moved parts must fail.
            bpy.ops.wm.read_factory_settings(use_empty=True)
            bpy.ops.import_scene.gltf(filepath=str(root / 'assembled.glb'))
            obj = next(obj for obj in bpy.context.scene.objects if obj.type == 'MESH')
            obj.location.x += 10
            changed = root / 'changed.glb'
            bpy.ops.export_scene.gltf(filepath=str(changed), export_format='GLB', export_extras=True)
            with self.assertRaises(ValueError):
                ExportGeometryVerification().run(source, changed, root / 'bad-geometry.json', 0.001)
            # Reusing the job after its input changes must fail before rendering.
            source.write_bytes(source.read_bytes() + b'changed')
            with self.assertRaisesRegex(ValueError, 'Source GLB changed'):
                BlenderBakeJob(root).run()


if __name__ == '__main__':
    unittest.main()
