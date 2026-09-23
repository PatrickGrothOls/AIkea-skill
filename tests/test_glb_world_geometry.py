"""Scope: Check glTF transform conventions independently of Blender's scene importer."""
import numpy as np
from types import SimpleNamespace
from glb_world_geometry import GlbWorldGeometry


class TestGlbWorldGeometry:
    def test_primitive_indices_do_not_wrap_at_part_wide_vertex_offsets(self):
        reader = GlbWorldGeometry.__new__(GlbWorldGeometry)
        positions = np.zeros((40000, 3), dtype=np.float32)
        arrays = {0: positions, 1: np.array([39997, 39998, 39999], dtype=np.uint16)}
        reader.glb = SimpleNamespace(original={'meshes': [{'primitives': [
            {'attributes': {'POSITION': 0}, 'indices': 1} for _ in range(3)]}]},
            array=arrays.__getitem__)
        reader.members = {'panel': ({'mesh': 0}, np.eye(4))}
        reader.unit_scale = 1
        points, triangles = reader.part('panel')
        assert points.shape == (120000, 3)
        assert triangles.tolist() == [[39997, 39998, 39999], [79997, 79998, 79999],
                                      [119997, 119998, 119999]]
        assert triangles.dtype == np.int64

    def test_trs_uses_quaternion_xyzw_and_scale_before_rotation(self):
        q = np.sqrt(.5)
        matrix = GlbWorldGeometry.matrix({'translation':[4,5,6], 'scale':[2,3,4],
                                         'rotation':[0,0,q,q]})
        assert np.allclose(matrix @ [1,0,0,1], [4,7,6,1])

    def test_column_major_matrix_and_nested_parent_compose(self):
        parent = GlbWorldGeometry.matrix({'matrix':[1,0,0,0,0,1,0,0,0,0,1,0,10,20,30,1]})
        child = GlbWorldGeometry.matrix({'translation':[1,2,3]})
        assert np.array_equal(parent @ child @ [0,0,0,1], [11,22,33,1])
