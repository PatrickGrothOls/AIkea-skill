"""Scope: Provide explicit cabinet and exact-envelope KA 4532 test geometry."""

from types import SimpleNamespace


class HettichKa4532SpacerMountingTestSupport:
    """Build small assembly-frame fixtures without replacing product geometry."""

    def cabinet(self, left_x_mm: float = 0.0, right_x_mm: float = 595.0):
        parts = {
            "left_side": self._side_part(left_x_mm, 0.0, (1.0, 0.0, 0.0)),
            "right_side": self._side_part(
                right_x_mm,
                564.0,
                (-1.0, 0.0, 0.0),
            ),
        }
        return SimpleNamespace(
            assembly_id="tall_storage_01",
            width_mm=999.0,
            base_height_mm=100.0,
            inside_depth_mm=564.0,
            top=(SimpleNamespace(height_mm=800.0),),
            parts=tuple(parts.values()),
            part=parts.__getitem__,
        )

    def step_set(self):
        fixed_length_mm = 502.483917
        moving_length_mm = 505.04
        return SimpleNamespace(
            runner_source=SimpleNamespace(
                bounds_mm=SimpleNamespace(zmin=-22.85, zmax=22.85),
                asset=SimpleNamespace(sha256="runner-sha256"),
            ),
            spacer_source=SimpleNamespace(
                asset=SimpleNamespace(sha256="spacer-sha256")
            ),
            runner_left=SimpleNamespace(
                fixed_member=self._fixed_member(0.0, fixed_length_mm),
                moving_member=self._member(0.0, moving_length_mm),
            ),
            runner_right=SimpleNamespace(
                fixed_member=self._fixed_member(188.3, fixed_length_mm),
                moving_member=self._member(188.3, moving_length_mm),
            ),
            spacer_solid=self._box(0.0, 25.0, 486.0, 50.0, 0.0),
        )

    def _member(self, xmin, length_mm):
        return self._box(xmin, 12.7, length_mm, 45.7, -9.5)

    def _fixed_member(self, xmin, length_mm):
        import cadquery as cq

        member = self._member(xmin, length_mm)
        bounds = member.BoundingBox()
        for depth_mm in (25.5, 153.5, 249.5, 313.5):
            bore = cq.Solid.makeCylinder(
                3.2,
                bounds.xlen + 2.0,
                cq.Vector(bounds.xmin - 1.0, depth_mm, 0.0),
                cq.Vector(1.0, 0.0, 0.0),
            )
            member = member.cut(bore)
        return member

    def _box(self, xmin, width_mm, depth_mm, height_mm, ymin):
        import cadquery as cq

        solid = cq.Solid.makeBox(
            width_mm,
            depth_mm,
            height_mm,
            cq.Vector(xmin, 0.0, 0.0),
        )
        zmin = -22.85 if height_mm == 45.7 else 0.0
        return solid.located(cq.Location(cq.Vector(0.0, ymin, zmin)))

    def _side_part(self, x_mm, y_mm, local_z):
        local_x = (0.0, 1.0 if local_z[0] > 0.0 else -1.0, 0.0)
        return SimpleNamespace(
            part_id="left_side" if local_z[0] > 0.0 else "right_side",
            role="cabinet_side",
            dimensions_mm=(),
            local_size_mm=(564.0, 800.0, 18.0),
            inside_face=">Z",
            local_to_parent=SimpleNamespace(
                origin_in_parent=SimpleNamespace(x_mm=x_mm, y_mm=y_mm, z_mm=100.0),
                axis_basis=SimpleNamespace(
                    local_x_in_parent=self._direction(local_x),
                    local_y_in_parent=self._direction((0.0, 0.0, 1.0)),
                    local_z_in_parent=self._direction(local_z),
                ),
            ),
        )

    def _direction(self, values):
        return SimpleNamespace(x=values[0], y=values[1], z=values[2])


class HettichKa4532StepSetLoaderProbe:
    """Return recognizable exact-envelope geometry without vendor files in Git."""

    def __init__(self) -> None:
        self.hardware_roots = []

    def load(self, hardware_root):
        self.hardware_roots.append(hardware_root)
        return HettichKa4532SpacerMountingTestSupport().step_set()


__all__ = [
    "HettichKa4532SpacerMountingTestSupport",
    "HettichKa4532StepSetLoaderProbe",
]
