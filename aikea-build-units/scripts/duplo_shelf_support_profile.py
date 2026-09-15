"""Scope: Preserve the official Duplo 46642 drawing dimensions and preview evidence boundary."""
from dataclasses import dataclass
import cadquery as cq


@dataclass(frozen=True)
class DuploShelfSupportProfile:
    manufacturer: str = "Hettich"
    article: str = "46642"
    pin_diameter_mm: float = 5.0
    insertion_mm: float = 8.0
    bearing_length_mm: float = 8.0
    shelf_side_clearance_mm: float = 0.5
    source_url: str = "https://catalog.hettich.com/General/TA_2025/en_DE/catalogs/TA_2025_en_DE/pdf/save/bk_827.pdf"
    source_checked: str = "2026-09-15"

    def visual_geometry(self):
        """Dimension-based pin envelope; un-dimensioned collar detail is intentionally omitted."""
        return cq.Workplane("XY").circle(self.pin_diameter_mm/2).extrude(
            self.insertion_mm+self.bearing_length_mm+self.shelf_side_clearance_mm
        ).translate((0,0,-self.insertion_mm))
