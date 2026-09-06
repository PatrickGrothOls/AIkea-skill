"""Scope: Build exact-source fixtures for KA 4532 proof tests."""

from __future__ import annotations

from types import SimpleNamespace

import cadquery as cq

from unit_mockup import MockupPart


class HettichKa4532SpacerProofTestSupport:
    """Create one recognizable source set and its two review states."""

    def source(self):
        return SimpleNamespace(
            runner_source=self._asset("runner-sha256"),
            spacer_source=self._asset("spacer-sha256"),
            runner_left=SimpleNamespace(
                fixed_member=self._runner_shape(),
                moving_member=self._moving_runner_shape(),
            ),
            runner_right=SimpleNamespace(
                fixed_member=self._runner_shape(),
                moving_member=self._moving_runner_shape(),
            ),
            spacer_solid=self._spacer_shape(),
        )

    def parts(self, drawer_y_mm: float, source) -> tuple[MockupPart, ...]:
        wood = tuple(
            self.part(f"drawer_01__{name}", x_mm, drawer_y_mm + y_offset_mm)
            for name, x_mm, y_offset_mm in (
                ("left_side", 37.7, 10.0),
                ("right_side", 57.3, 10.0),
                ("front", 60.0, 0.0),
                ("back", 50.0, 10.0),
                ("bottom", 40.0, 10.0),
            )
        )
        return (
            self.part("left_side", -2.0, 0.0),
            self.part("right_side", 97.0, 0.0),
            self.source_part(
                "drawer_01_spacer_left",
                source.spacer_solid,
                0.0,
                10.0,
                -2.0,
            ),
            self.source_part(
                "drawer_01_spacer_right",
                source.spacer_solid,
                location=self._right_spacer_location(),
            ),
            self.source_part(
                "drawer_01_runner_left_fixed",
                source.runner_left.fixed_member,
                25.0,
                11.5,
                23.0,
            ),
            self.source_part(
                "drawer_01_runner_right_fixed",
                source.runner_right.fixed_member,
                70.0,
                11.5,
                23.0,
            ),
            *wood,
            self.source_part(
                "drawer_01__drawer_01_runner_left_moving",
                source.runner_left.moving_member,
                25.0,
                drawer_y_mm,
                22.0,
            ),
            self.source_part(
                "drawer_01__drawer_01_runner_right_moving",
                source.runner_right.moving_member,
                70.0,
                drawer_y_mm,
                22.0,
            ),
        )

    def part(self, name: str, x_mm: float, y_mm: float) -> MockupPart:
        return MockupPart(
            name,
            cq.Workplane(obj=self._part_shape()),
            cq.Location(cq.Vector(x_mm, y_mm, 0.0)),
            (0.5, 0.5, 0.5, 1.0),
        )

    def source_part(
        self,
        name: str,
        shape,
        x_mm: float = 0.0,
        y_mm: float = 0.0,
        z_mm: float = 0.0,
        *,
        location=None,
    ) -> MockupPart:
        workplane = cq.Workplane(obj=shape)
        asset_id = (
            "hettich-13952-spacer-profile"
            if "spacer" in name
            else "hettich-ka-4532-500-runner-pair"
        )
        selector = next(
            (
                value
                for value in ("left-fixed", "right-fixed", "left-moving", "right-moving")
                if value.replace("-", "_") in name
            ),
            None,
        )
        return MockupPart(
            name,
            workplane,
            location or cq.Location(cq.Vector(x_mm, y_mm, z_mm)),
            (0.5, 0.5, 0.5, 1.0),
            asset_id,
            selector,
        )

    def replace_spacer(self, parts, substitute):
        original = next(part for part in parts if part.name == "drawer_01_spacer_right")
        replacement = MockupPart(
            "drawer_01_spacer_right",
            cq.Workplane(obj=substitute),
            original.location,
            (0.5, 0.5, 0.5, 1.0),
            "hettich-13952-spacer-profile",
            None,
        )
        return tuple(replacement if part.name == replacement.name else part for part in parts)

    def equal_volume_substitute(self):
        return cq.Workplane("XY").box(50.0, 243.0, 50.0, centered=False).val()

    def _part_shape(self):
        return cq.Workplane("XY").box(2.0, 10.0, 2.0, centered=False).val()

    def _runner_shape(self):
        return cq.Workplane("XY").box(2.0, 315.0, 2.0, centered=False).val()

    def _moving_runner_shape(self):
        return self._runner_shape().located(
            cq.Location(cq.Vector(0.0, -11.5, -1.0))
        )

    def _spacer_shape(self):
        return cq.Workplane("XY").box(25.0, 486.0, 50.0, centered=False).val()

    def _right_spacer_location(self):
        return cq.Location(
            cq.Plane(
                origin=(97.0, 10.0, 48.0),
                xDir=(-1.0, 0.0, 0.0),
                normal=(0.0, 0.0, -1.0),
            )
        )

    def _asset(self, sha256: str):
        return SimpleNamespace(asset=SimpleNamespace(sha256=sha256))


__all__ = ["HettichKa4532SpacerProofTestSupport"]
