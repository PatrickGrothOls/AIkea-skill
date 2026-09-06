"""Scope: Mutate shared installed KA 4532 geometry in tests."""

from dataclasses import replace

import cadquery as cq

from hettich_ka_4532_spacer_proof_test_support import (
    HettichKa4532SpacerProofTestSupport,
)


class HettichKa4532InstalledGeometryTestSupport:
    """Own the common installed parts and rigid-placement mutations."""

    def __init__(self) -> None:
        proof_support = HettichKa4532SpacerProofTestSupport()
        self.source = proof_support.source()
        self.parts = {
            part.name: part for part in proof_support.parts(0.0, self.source)
        }

    def shifted_parts(
        self,
        names: tuple[str, ...],
        *,
        x_mm: float = 0.0,
        y_mm: float = 0.0,
        z_mm: float = 0.0,
    ) -> dict:
        shifted = dict(self.parts)
        translation = cq.Location(cq.Vector(x_mm, y_mm, z_mm))
        for name in names:
            part = shifted[name]
            shifted[name] = replace(part, location=translation * part.location)
        return shifted

    def tilted_location(self, origin: tuple[float, ...]) -> cq.Location:
        return cq.Location(
            cq.Plane(
                origin=origin,
                xDir=(0.984807753, 0.0, -0.173648178),
                normal=(0.173648178, 0.0, 0.984807753),
            )
        )


__all__ = ["HettichKa4532InstalledGeometryTestSupport"]
