"""Scope: Detect the observed black atlas without rejecting dim but finite lighting."""

import numpy as np
import pytest

from baked_lighting_signal import BakedLightingSignal


class TestBakedLightingSignal:
    @pytest.mark.parametrize('samples', [np.zeros((12, 3)), np.empty((0, 3)),
                                        np.array([[1, 1, float('nan')]]),
                                        np.array([[float('inf'), 1, 1]])])
    def test_empty_or_nonfinite_bake_fails(self, samples):
        assert BakedLightingSignal().measure(samples)['status'] == 'FAIL'

    def test_dim_material_and_unlit_hidden_faces_are_not_an_empty_bake(self):
        report = BakedLightingSignal().measure([[0, 0, 0], [0.002, 0.002, 0.002]])
        assert report['status'] == 'PASS'
        assert report['lit_triangle_centroids'] == 1
        assert report['sampled_triangle_centroids'] == 2
