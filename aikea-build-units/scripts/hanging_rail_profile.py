"""Scope: Keep Hettich SL 322 drawing datums and rail cut-stock geometry together."""
from dataclasses import dataclass
import cadquery as cq


@dataclass(frozen=True)
class HangingRailProfile:
    manufacturer: str = 'Hettich'
    support_article: str = '70664'
    rail_article: str = '9000894'
    stock_length_mm: float = 5000.0
    end_allowance_mm: float = 3.5
    screw_offsets_mm: tuple[float, ...] = (0.0, 9.5, 32.0)
    screw_diameter_mm: float = 4.0
    source_url: str = ('https://catalog.hettich.com/General/TA_2025/en_DE/'
                       'catalogs/TA_2025_en_DE/pdf/save/bk_974.pdf')

    def rail(self, length_mm):
        """30 x 15 x 0.6 mm oval tube; length follows the support's 7 mm deduction."""
        if not 0 < length_mm <= self.stock_length_mm:
            raise ValueError('Hanging rail must fit the selected 5000 mm stock length')
        return (cq.Workplane('YZ').slot2D(30, 15, angle=90)
                .slot2D(28.8, 13.8, angle=90).extrude(length_mm))

    def support_preview(self):
        """Dimensioned envelope only; never label this solid as exact manufacturer CAD."""
        plate = cq.Workplane('YZ', origin=(0, 0, 16)).slot2D(42.8, 18.6, angle=90).extrude(3)
        cradle = (cq.Workplane('YZ', origin=(3, 0, 11.4)).slot2D(33.4, 18.6, angle=90)
                  .slot2D(30.2, 15.2, angle=90).extrude(10))
        result = plate.union(cradle)
        for height in self.screw_offsets_mm:
            result = result.cut(cq.Workplane('YZ', origin=(-.1, 0, height)).circle(2).extrude(3.2))
        return result
