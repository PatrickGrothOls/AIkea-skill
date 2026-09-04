"""Scope: Define Hettich's official KA 4532/500 cabinet fixing pattern."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class HettichKa4532FixedMemberHolePattern:
    """Carry the official drawing dimensions and matching source-STEP axes."""

    installation_document: str
    installation_url: str
    hole_diameter_mm: float
    first_axis_from_cabinet_front_mm: float
    axis_spans_from_first_mm: tuple[float, ...]
    fixed_member_native_depth_axes_mm: tuple[float, ...]
    fixed_member_native_height_mm: float

    @property
    def cabinet_depth_axes_mm(self) -> tuple[float, ...]:
        """Resolve the chained drawing dimensions into cabinet-front axes."""
        return tuple(
            self.first_axis_from_cabinet_front_mm + span_mm
            for span_mm in self.axis_spans_from_first_mm
        )


HETTICH_KA_4532_500_FIXED_MEMBER_HOLES = HettichKa4532FixedMemberHolePattern(
    installation_document="Hettich MS 10547.00.000",
    installation_url=(
        "https://web2.hettich.com/hbh/addon/montage/"
        "MS_10547_00_Montageanleitung_KA4532-SiSy.pdf"
    ),
    hole_diameter_mm=6.4,
    first_axis_from_cabinet_front_mm=37.0,
    axis_spans_from_first_mm=(0.0, 128.0, 224.0, 288.0),
    fixed_member_native_depth_axes_mm=(25.5, 153.5, 249.5, 313.5),
    fixed_member_native_height_mm=0.0,
)


__all__ = [
    "HETTICH_KA_4532_500_FIXED_MEMBER_HOLES",
    "HettichKa4532FixedMemberHolePattern",
]
