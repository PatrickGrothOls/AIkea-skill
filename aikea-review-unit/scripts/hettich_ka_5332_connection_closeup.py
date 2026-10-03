"""Scope: Crop one KA 5332 cabinet-to-drawer connection for visual approval."""

from __future__ import annotations

import cadquery as cq

from unit_mockup import MockupPart


class HettichKa5332ConnectionCloseup:
    """Keep one real runner hand and only the nearby portions of its wood."""

    _RUNNER_NAME_PREFIX = "ka_5332__left__"

    def build(
        self,
        parts: tuple[MockupPart, ...],
        *,
        drawer_front_mm: float,
        drawer_bottom_mm: float,
    ) -> tuple[MockupPart, ...]:
        front_region = cq.Solid.makeBox(
            90.0,
            160.0,
            260.0,
            cq.Vector(
                0.0,
                drawer_front_mm - 20.0,
                drawer_bottom_mm - 40.0,
            ),
        )
        full_depth_region = cq.Solid.makeBox(
            90.0,
            1000.0,
            260.0,
            cq.Vector(0.0, -400.0, drawer_bottom_mm - 40.0),
        )
        selected = tuple(
            part
            for part in parts
            if self._is_wood_part(part.name)
            or part.name.startswith(self._RUNNER_NAME_PREFIX)
        )
        drawer_present = any(
            part.name != "left_side" and part.name.endswith("__left_side")
            for part in selected
        )
        return tuple(
            self._crop_wood(
                part,
                front_region
                if part.name == "left_side" and drawer_present
                else full_depth_region,
            )
            if self._is_wood_part(part.name)
            else part
            for part in selected
        )

    def _is_wood_part(self, name: str) -> bool:
        return name == "left_side" or name.endswith("__left_side")

    def _crop_wood(self, part: MockupPart, region: cq.Shape) -> MockupPart:
        placed_shape = part.solid.val().located(part.location)
        return MockupPart(
            f"{part.name}__connection_cutaway",
            cq.Workplane(obj=placed_shape.intersect(region)),
            cq.Location(),
            part.color,
        )


__all__ = ["HettichKa5332ConnectionCloseup"]
