"""Scope: Reproduce independently measured KA 4532 and 13952 solid signatures."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NativeBoundsTestDouble:
    """Expose all native bounds used by runtime signature validation."""

    xmin: float
    xmax: float
    ymin: float
    ymax: float
    zmin: float
    zmax: float


@dataclass(frozen=True, slots=True)
class NativeSolidTestDouble:
    """Represent one exact or deliberately changed purchased solid."""

    name: str
    measurements: tuple[float, ...]

    def BoundingBox(self) -> NativeBoundsTestDouble:
        return NativeBoundsTestDouble(*self.measurements[:6])

    def Volume(self) -> float:
        return self.measurements[6]


class HettichKa4532StepSignatureTestSupport:
    """Build test solids from measurements captured from the approved STEP files."""

    _MEASUREMENTS = {
        "left-fixed": (
            -0.0000001, 8.777139874, -9.5, 492.983917012,
            -22.85009328, 22.85009328, 44121.466839636,
        ),
        "left-moving": (
            4.2, 12.5000001, -9.5, 495.54,
            -12.149518924, 12.149518924, 24166.280706188,
        ),
        "right-moving": (
            188.4999999, 196.8, -9.5, 495.54,
            -12.149518924, 12.149518924, 24166.280706188,
        ),
        "right-fixed": (
            192.222860126, 201.0000001, -9.5, 492.983917012,
            -22.85009328, 22.85009328, 44121.466875251,
        ),
        "spacer": (
            -0.0000001, 25.0000001, 0.0, 486.0,
            0.0, 50.0, 576658.608794442,
        ),
    }

    def solids(self) -> dict[str, NativeSolidTestDouble]:
        return {
            role: NativeSolidTestDouble(role, measurements)
            for role, measurements in self._MEASUREMENTS.items()
        }

    def changed(
        self,
        role: str,
        measurement_index: int,
        delta: float,
    ) -> NativeSolidTestDouble:
        values = list(self._MEASUREMENTS[role])
        values[measurement_index] += delta
        return NativeSolidTestDouble(role, tuple(values))


__all__ = [
    "HettichKa4532StepSignatureTestSupport",
    "NativeBoundsTestDouble",
    "NativeSolidTestDouble",
]
