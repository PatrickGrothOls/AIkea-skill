"""Scope: Supply explicit synthetic placement markers for panel-pipeline integration tests.

Markers are NOT manufacturer geometry and these tests do not qualify hardware fit
or fabrication. Exact CAD checksum/article rejection remains covered separately
by test_korrekt_component_feature.py. No production provider is patched.
"""
import cadquery as cq
from project_hardware_geometry_resolver import ProjectHardwareGeometryResolver
from purchased_hardware_hydrator import PurchasedHardwareHydrator


class KorrektPlacementMarkerProvider:
    """Only stand in for the two external assets absent from isolated test projects."""
    ASSETS = {"hettich_korrekt_61854": ("61854", (-16, 0, -1)),
              "hettich_korrekt_70151": ("70151", (0, 0, -53))}

    def supports(self, asset_id):
        return asset_id in self.ASSETS

    def resolve(self, root, spec):
        article, center = self.ASSETS[spec.hardware_asset_id]
        assert spec.manufacturer == "Hettich" and spec.product_code == article
        return cq.Workplane("XY").box(0.5, 0.5, 0.5).translate(center)


class PanelReviewHydrationFixture:
    """Retain all declarations and real panel/pin geometry, injecting only vendor IO."""
    def hydrate(self, root, built, hidden=None):
        resolver = ProjectHardwareGeometryResolver((KorrektPlacementMarkerProvider(),))
        return PurchasedHardwareHydrator(resolver).hydrate(root, built, hidden)
