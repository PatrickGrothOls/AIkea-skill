"""Scope: Check glTF transform conventions independently of Blender's scene importer."""
import numpy as np
from glb_world_geometry import GlbWorldGeometry


class TestGlbWorldGeometry:
    def test_trs_uses_quaternion_xyzw_and_scale_before_rotation(self):
        q = np.sqrt(.5)
        matrix = GlbWorldGeometry.matrix({'translation':[4,5,6], 'scale':[2,3,4],
                                         'rotation':[0,0,q,q]})
        assert np.allclose(matrix @ [1,0,0,1], [4,7,6,1])

    def test_column_major_matrix_and_nested_parent_compose(self):
        parent = GlbWorldGeometry.matrix({'matrix':[1,0,0,0,0,1,0,0,0,0,1,0,10,20,30,1]})
        child = GlbWorldGeometry.matrix({'translation':[1,2,3]})
        assert np.array_equal(parent @ child @ [0,0,0,1], [11,22,33,1])
