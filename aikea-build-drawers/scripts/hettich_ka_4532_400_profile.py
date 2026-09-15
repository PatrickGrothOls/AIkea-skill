"""Scope: Record exact article 9114274 dimensions and its independently read fixing datums."""
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Ka4532FixingPattern:
    member: str
    diameter_mm: float
    native_depth_axes_mm: tuple[float, ...]
    front_depth_axes_mm: tuple[float, ...]
    slot_straight_lengths_mm: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class HettichKa4532FourHundredProfile:
    """Source/drawing authority only; stock pilots, spacers and installed fit remain separate."""

    article: str = "9114274"
    asset_id: str = "hettich-ka-4532-400-runner-pair"
    nominal_length_mm: float = 400
    minimum_cabinet_depth_mm: float = 404
    runner_height_mm: float = 46
    installed_width_per_side_mm: float = 12.7
    additional_width_tolerance_mm: float = .8
    load_class_kg: float = 35
    recommended_maximum_drawer_width_mm: float = 550
    native_front_mm: float = -9.5
    runner_setback_from_front_mm: float = 2
    installation_document: str = "Hettich MS 10547.00.000, pages 1 and 2, KA 4532/400 row"
    installation_url: str = "https://web2.hettich.com/hbh/addon/montage/MS_10547_00_Montageanleitung_KA4532-SiSy.pdf"
    checked_on: str = "2026-09-15"

    @property
    def native_to_front_offset_mm(self):
        return self.runner_setback_from_front_mm-self.native_front_mm

    @property
    def fixing_patterns(self):
        # The 400 mm drawing selects three axes on each member. The first two
        # drawer axes are centres of vertical 4.4 x 4 slots, the last is round.
        return (
            Ka4532FixingPattern("fixed", 6.4, (25.5, 153.5, 217.5), (37, 165, 229), (0, 0, 0)),
            Ka4532FixingPattern("moving", 4.4, (25.5, 153.5, 279.5), (37, 165, 291), (4, 4, 0)),
        )


HETTICH_KA_4532_400 = HettichKa4532FourHundredProfile()
