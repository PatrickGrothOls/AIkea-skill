"""Scope: Reject empty or nonfinite lighting at actual baked panel triangle samples."""

import numpy as np


class BakedLightingSignal:
    """Detect an empty diffuse bake; this is not a beauty or photometric assessment."""

    def measure(self, rgb):
        luminance = np.asarray(rgb) @ np.array([0.2126, 0.7152, 0.0722])
        finite = bool(np.isfinite(luminance).all())
        lit = int(np.count_nonzero(luminance > 1e-6))
        maximum = float(luminance.max()) if len(luminance) and finite else 0.0
        return dict(status='PASS' if finite and lit else 'FAIL',
                    sampled_triangle_centroids=len(luminance),
                    lit_triangle_centroids=lit, maximum_luminance=maximum,
                    finite=finite)
