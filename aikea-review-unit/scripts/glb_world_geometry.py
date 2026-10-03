"""Scope: Read identified static GLB parts as world-space triangles without invoking a renderer."""
import numpy as np
from static_glb_buffers import StaticGlbBuffers


class GlbWorldGeometry:
    def __init__(self, path, unit_scale):
        self.glb = StaticGlbBuffers(path)
        self.unit_scale = unit_scale
        self.members = {}
        doc = self.glb.original
        pending = [(index,np.eye(4)) for index in doc['scenes'][doc['scene']]['nodes']]
        while pending:
            index, parent = pending.pop()
            node = doc['nodes'][index]
            world = parent @ self.matrix(node)
            pending.extend((child,world) for child in node.get('children', []))
            if 'mesh' not in node:
                continue
            identity = node.get('extras', {}).get('aikea', {})
            if identity.get('kind') not in {'panel','hardware'} or not identity.get('inspection_path'):
                raise ValueError(f'{node.get("name")}: mesh has no source part identity')
            key = '/'.join(identity['inspection_path'])
            if key in self.members:
                raise ValueError(f'{key}: duplicate part identity')
            self.members[key] = node, world

    def part(self, key):
        node, world = self.members[key]
        points, triangles, offset = [], [], 0
        for primitive in self.glb.original['meshes'][node['mesh']]['primitives']:
            if primitive.get('mode',4) != 4 or 'targets' in primitive:
                raise ValueError(f'{key}: expected static triangle primitives')
            local = self.glb.array(primitive['attributes']['POSITION']).astype(np.float64)
            indices = (self.glb.array(primitive['indices']).reshape(-1) if 'indices' in primitive
                       else np.arange(len(local)))
            points.append((local @ world[:3,:3].T + world[:3,3])*self.unit_scale)
            # Primitive-local uint16 indices must not wrap or overflow at a part-wide offset.
            triangles.append(indices.astype(np.int64).reshape(-1,3)+offset)
            offset += len(local)
        return np.concatenate(points), np.concatenate(triangles)

    @staticmethod
    def matrix(node):
        if 'matrix' in node:
            return np.array(node['matrix']).reshape(4,4).T
        x,y,z,w = node.get('rotation', [0,0,0,1])
        rotation = np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],
                             [2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],
                             [2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])
        matrix = np.eye(4)
        matrix[:3,:3] = rotation @ np.diag(node.get('scale',[1,1,1]))
        matrix[:3,3] = node.get('translation',[0,0,0])
        return matrix
