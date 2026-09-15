"""Scope: Compare exported furniture triangles against the exact imported source in world space."""

import json
import bpy
import numpy as np
from mathutils.kdtree import KDTree


class ExportGeometryVerification:
    def parts(self, scale):
        result = {}
        for obj in bpy.context.scene.objects:
            identity = obj.get('aikea', {})
            if obj.type != 'MESH':
                continue
            if identity.get('kind') not in {'panel','hardware'} or not identity.get('inspection_path'):
                raise ValueError(f'{obj.name}: exported mesh has no source part identity')
            key = '/'.join(identity['inspection_path'])
            assert key not in result, key
            local = np.empty(len(obj.data.vertices)*3, dtype=np.float64)
            obj.data.vertices.foreach_get('co', local)
            matrix = np.array(obj.matrix_world, dtype=np.float64)
            points = (local.reshape((-1,3)) @ matrix[:3,:3].T + matrix[:3,3]) * scale
            obj.data.calc_loop_triangles()
            triangles = np.empty(len(obj.data.loop_triangles)*3, dtype=np.int32)
            obj.data.loop_triangles.foreach_get('vertices', triangles)
            result[key] = (points, triangles.reshape((-1,3)))
        return result

    def ordered(self, triangles):
        values = np.sort(triangles, axis=1)
        return values[np.lexsort(values.T[::-1])]

    def compare(self, key, before, after):
        vertices, inverse = np.unique(before[0], axis=0, return_inverse=True)
        tree = KDTree(len(vertices))
        for index, point in enumerate(vertices):
            tree.insert(point, index)
        tree.balance()
        found = [tree.find(point) for point in after[0]]
        distance = max(row[2] for row in found)
        assert distance < 0.000002, (key, distance)
        mapping = np.array([row[1] for row in found])
        assert np.array_equal(self.ordered(inverse[before[1]]), self.ordered(mapping[after[1]])), key
        return {'part':key, 'triangles':len(before[1]), 'maximum_vertex_error_mm':distance*1000}

    def run(self, source_path, model_path, report_path, unit_scale):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.import_scene.gltf(filepath=str(source_path))
        source = self.parts(unit_scale)
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.import_scene.gltf(filepath=str(model_path))
        exported = self.parts(unit_scale)
        assert set(source) == set(exported)
        rows = [self.compare(key, source[key], exported[key]) for key in source]
        materials = [material.name for material in bpy.data.materials if material.use_nodes]
        report = {'status':'PASS','physical_parts':len(source), 'triangle_connectivity':'identical',
            'maximum_vertex_error_mm':max(row['maximum_vertex_error_mm'] for row in rows),
            'materials':materials, 'parts':rows}
        report_path.write_text(json.dumps(report,indent=2))
        print(json.dumps({k:v for k,v in report.items() if k!='parts'},indent=2), flush=True)
