"""Scope: Import the exact furniture and prove presentation does not change its meshes."""

import hashlib
import json
from pathlib import Path
import struct
import bpy
import numpy as np
from mathutils import Vector


class BlenderFurnitureSource:
    def __init__(self, path, unit_scale=0.001):
        self.path = Path(path)
        self.unit_scale = unit_scale

    def load(self):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.preferences.addon_enable(module='io_scene_gltf2')
        bpy.ops.import_scene.gltf(filepath=str(self.path))
        self.parts = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
        if not self.parts:
            raise ValueError('Input GLB contains no parts')
        keys = []
        for obj in self.parts:
            identity = obj.get('aikea', {})
            if identity.get('kind') not in {'panel', 'hardware'} or not identity.get('inspection_path'):
                raise ValueError(f'{obj.name}: source part identity is missing')
            keys.append('/'.join(identity['inspection_path']))
        if len(keys) != len(set(keys)):
            raise ValueError('Source part identities must be unique')
        self.panels = [obj for obj in self.parts if obj['aikea']['kind'] == 'panel']
        if not self.panels:
            raise ValueError('Input GLB contains no furniture panels')
        for obj in self.panels:
            if not obj.data.uv_layers or not obj.data.materials or any(
                    material is None or not material.use_nodes for material in obj.data.materials):
                raise ValueError(f'{obj.name}: assign source materials and UVs before baking')
        self.before = self.geometry()
        self.before_uvs = self.source_uvs()
        for obj in bpy.context.scene.objects:
            if obj.parent is None:
                obj.scale *= self.unit_scale
        bpy.context.view_layer.update()
        self.matrices = {obj.name:list(sum((list(row) for row in obj.matrix_world), [])) for obj in self.parts}
        points = [obj.matrix_world @ Vector(corner) for obj in self.parts for corner in obj.bound_box]
        self.minimum = Vector([min(p[i] for p in points) for i in range(3)])
        self.maximum = Vector([max(p[i] for p in points) for i in range(3)])
        self.center = (self.minimum + self.maximum) / 2
        print('FURNITURE_BOUNDS', list(self.minimum), list(self.maximum), flush=True)
        return self

    def geometry(self):
        result = {}
        for obj in self.parts:
            digest = hashlib.sha256()
            for vertex in obj.data.vertices:
                digest.update(struct.pack('<3f', *vertex.co))
            for polygon in obj.data.polygons:
                digest.update(struct.pack('<I', len(polygon.vertices)))
                digest.update(struct.pack('<' + 'I'*len(polygon.vertices), *polygon.vertices))
            result[obj.name] = {'vertices':len(obj.data.vertices), 'faces':len(obj.data.polygons),
                'sha256':digest.hexdigest(), 'modifiers':[m.type for m in obj.modifiers]}
        return result

    def source_uvs(self):
        result = {}
        for obj in self.panels:
            layers = []
            for layer in obj.data.uv_layers:
                if layer.name == 'BakedLightingUV':
                    continue
                points = np.empty(len(obj.data.loops)*2, dtype=np.float32)
                layer.data.foreach_get('uv', points)
                layers.append(hashlib.sha256(points.tobytes()).hexdigest())
            result[obj.name] = layers
        return result

    def verify(self, output):
        after = self.geometry()
        assert self.before == after
        assert self.before_uvs == self.source_uvs()
        assert all(not row['modifiers'] for row in after.values())
        current = {obj.name:list(sum((list(row) for row in obj.matrix_world), [])) for obj in self.parts}
        assert current == self.matrices
        report = {'status':'PASS', 'source':str(self.path),
            'source_sha256':hashlib.sha256(self.path.read_bytes()).hexdigest(),
            'physical_parts':len(self.parts), 'source_unit_metres':self.unit_scale,
            'no_mesh_changes':True, 'source_uvs_unchanged':True, 'no_modifiers':True, 'placements_unchanged_after_import':True,
            'part_meshes':after}
        Path(output).write_text(json.dumps(report, indent=2))
