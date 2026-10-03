"""Scope: Load unchanged, checksum-bound Hettich Korrekt STEP assets from project storage."""

from hashlib import sha256

import cadquery as cq

from korrekt_mounting_profile import KorrektMountingProfile
from project_hardware_geometry_resolver import ProjectHardwareGeometryError


class HettichKorrektGeometryProvider:
    SOURCES = {
        "hettich_korrekt_61854": ("61854", KorrektMountingProfile().source_step_sha256),
        "hettich_korrekt_70151": ("70151", "59273834cf1cf9ee68e7ed0840240caadbd82a97ba28f5eed787ff0e53164c06"),
    }

    def supports(self, asset_id):
        return asset_id in self.SOURCES

    def resolve(self, project_root, spec):
        code, expected = self.SOURCES[spec.hardware_asset_id]
        if spec.manufacturer != "Hettich" or spec.product_code != code:
            raise ProjectHardwareGeometryError("Korrekt asset and purchased article disagree")
        source = project_root / "hardware/hettich/korrekt" / code / "source" / (code+".stp")
        if not source.is_file() or sha256(source.read_bytes()).hexdigest() != expected:
            raise ProjectHardwareGeometryError(f"Missing or changed Korrekt source: {source}; verify the exact CAD download")
        shape = cq.importers.importStep(str(source))
        if not shape.val().isValid() or not shape.val().Solids():
            raise ProjectHardwareGeometryError(f"Invalid Korrekt source solid: {source}")
        return shape
