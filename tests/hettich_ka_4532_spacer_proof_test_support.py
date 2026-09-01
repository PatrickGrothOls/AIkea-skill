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
                fixed_member=self._shape(),
                moving_member=self._shape(),
            ),
            runner_right=SimpleNamespace(
                fixed_member=self._shape(),
                moving_member=self._shape(),
            ),
            spacer_solid=self._shape(),
        )

    def parts(self, drawer_y_mm: float, source) -> tuple[MockupPart, ...]:
        wood = tuple(
            self.part(f"drawer_01__{name}", x_mm, drawer_y_mm)
            for name, x_mm in (
                ("left_side", 30.0),
                ("right_side", 50.0),
                ("front", 60.0),
                ("back", 70.0),
                ("bottom", 40.0),
            )
        )
        return (
            self.source_part("drawer_01_spacer_left", source.spacer_solid, 0.0, 20.0),
            self.source_part("drawer_01_spacer_right", source.spacer_solid, 95.0, 20.0),
            self.source_part(
                "drawer_01_runner_left_fixed",
                source.runner_left.fixed_member,
                10.0,
                0.0,
            ),
            self.source_part(
                "drawer_01_runner_right_fixed",
                source.runner_right.fixed_member,
                88.0,
                0.0,
            ),
            *wood,
            self.source_part(
                "drawer_01__drawer_01_runner_left_moving",
                source.runner_left.moving_member,
                10.0,
                drawer_y_mm,
            ),
            self.source_part(
                "drawer_01__drawer_01_runner_right_moving",
                source.runner_right.moving_member,
                88.0,
                drawer_y_mm,
            ),
        )

    def part(self, name: str, x_mm: float, y_mm: float) -> MockupPart:
        return MockupPart(
            name,
            cq.Workplane(obj=self._shape()),
            cq.Location(cq.Vector(x_mm, y_mm, 0.0)),
            (0.5, 0.5, 0.5, 1.0),
        )

    def source_part(self, name: str, shape, x_mm: float, y_mm: float) -> MockupPart:
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
            cq.Location(cq.Vector(x_mm, y_mm, 0.0)),
            (0.5, 0.5, 0.5, 1.0),
            asset_id,
            selector,
        )

    def replace_spacer(self, parts, substitute):
        replacement = MockupPart(
            "drawer_01_spacer_right",
            cq.Workplane(obj=substitute),
            cq.Location(cq.Vector(95.0, 20.0, 0.0)),
            (0.5, 0.5, 0.5, 1.0),
            "hettich-13952-spacer-profile",
            None,
        )
        return tuple(replacement if part.name == replacement.name else part for part in parts)

    def equal_volume_substitute(self):
        return cq.Workplane("XY").box(4.0, 5.0, 2.0, centered=False).val()

    def _shape(self):
        return cq.Workplane("XY").box(2.0, 10.0, 2.0, centered=False).val()

    def _asset(self, sha256: str):
        return SimpleNamespace(asset=SimpleNamespace(sha256=sha256))


__all__ = ["HettichKa4532SpacerProofTestSupport"]
