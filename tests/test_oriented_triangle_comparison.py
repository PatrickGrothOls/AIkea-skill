"""Scope: Reject real export changes while accepting reordered and nearly coincident triangle surfaces."""
import numpy as np
import pytest
from oriented_triangle_comparison import OrientedTriangleComparison


class TestOrientedTriangleComparison:
    def geometry(self, triangles):
        points = np.asarray(triangles, dtype=np.float64).reshape(-1,3)
        return points, np.arange(len(points)).reshape(-1,3)

    def faces(self):
        return np.array([[[1.5,0,0],[1.51,0,0],[1.5,.01,0]],
                         [[1.5,0,.01],[1.51,0,.01],[1.5,.01,.01]]])

    def test_reordered_cyclic_faces_and_float_export_rounding_pass(self):
        source = self.faces()
        exported = np.roll(source[::-1],1,axis=1) + .0000001
        report = OrientedTriangleComparison().compare('panel',self.geometry(source),self.geometry(exported))
        assert report['triangles'] == 2
        assert report['maximum_vertex_error_mm'] < .002

    def test_nearly_coincident_source_vertices_do_not_share_one_export_triangle(self):
        source = np.array([self.faces()[0],self.faces()[0]+[.00000001,0,0]])
        exported = source[::-1]+[.00000008,0,0]
        assert len(np.unique(source.reshape(-1,3),axis=0)) > len(np.unique(source.astype(np.float32).reshape(-1,3),axis=0))
        OrientedTriangleComparison().compare('hinge',self.geometry(source),self.geometry(exported))

    @pytest.mark.parametrize('change',['winding','position','count','duplicate'])
    def test_geometry_changes_fail(self, change):
        source = self.faces()
        exported = source.copy()
        if change == 'winding':
            exported[0] = exported[0,[0,2,1]]
        elif change == 'position':
            exported[0,0,0] += .00001
        elif change == 'count':
            exported = exported[:1]
        else:
            exported[1] = exported[0]
        with pytest.raises(ValueError):
            OrientedTriangleComparison().compare('part',self.geometry(source),self.geometry(exported))

    def test_ambiguous_candidates_use_a_bijection_instead_of_a_greedy_choice(self):
        result = OrientedTriangleComparison().match([[0,1],[0]])
        assert result == {0:1,1:0}
