"""Scope: Derive the manufactured sheet parts for one structural base module."""

from __future__ import annotations

from assembly_taxonomy import PartTaxonomy


class BasePartTaxonomy:
    """Create one deck, two rails, and the calculated brace set for a module."""

    def build_module(
        self,
        module_index: int,
        module_width_mm: float,
        depth_mm: float,
        clear_depth_mm: float,
        support_height_mm: float,
        panel_thickness_mm: float,
        brace_positions_mm: tuple[float, ...],
    ) -> tuple[PartTaxonomy, ...]:
        suffix = f"{module_index:02d}"
        parts = [
            self._deck(
                f"deck_{suffix}",
                module_width_mm,
                depth_mm,
                panel_thickness_mm,
            ),
            self._rail(
                f"front_rail_{suffix}",
                module_width_mm,
                support_height_mm,
                panel_thickness_mm,
            ),
            self._rail(
                f"back_rail_{suffix}",
                module_width_mm,
                support_height_mm,
                panel_thickness_mm,
            ),
        ]
        parts.extend(
            self._brace(
                f"brace_{suffix}_{brace_index:02d}",
                clear_depth_mm,
                support_height_mm,
                panel_thickness_mm,
                position_mm,
            )
            for brace_index, position_mm in enumerate(
                brace_positions_mm,
                start=1,
            )
        )
        return tuple(parts)

    def _deck(
        self,
        part_id: str,
        width_mm: float,
        depth_mm: float,
        thickness_mm: float,
    ) -> PartTaxonomy:
        return PartTaxonomy(
            part_id,
            "base_deck",
            (("width", width_mm), ("depth", depth_mm), ("thickness", thickness_mm)),
            local_size_mm=(width_mm, depth_mm, thickness_mm),
            inside_face=">Z",
        )

    def _rail(
        self,
        part_id: str,
        length_mm: float,
        height_mm: float,
        thickness_mm: float,
    ) -> PartTaxonomy:
        return PartTaxonomy(
            part_id,
            "base_rail",
            (("length", length_mm), ("height", height_mm), ("thickness", thickness_mm)),
            local_size_mm=(length_mm, height_mm, thickness_mm),
            inside_face=">Z",
        )

    def _brace(
        self,
        part_id: str,
        length_mm: float,
        height_mm: float,
        thickness_mm: float,
        center_x_mm: float,
    ) -> PartTaxonomy:
        return PartTaxonomy(
            part_id,
            "base_brace",
            (
                ("length", length_mm),
                ("height", height_mm),
                ("thickness", thickness_mm),
                ("center_x", center_x_mm),
            ),
            local_size_mm=(length_mm, height_mm, thickness_mm),
            inside_face=">Z",
        )


__all__ = ["BasePartTaxonomy"]
