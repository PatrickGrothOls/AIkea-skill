"""Scope: Provide explicit cabinet-part frames and runner bounds for KA 4532 tests."""

from types import SimpleNamespace


class _RunnerMember:
    """Expose native member bounds through the CadQuery shape contract."""

    def __init__(self, xmin: float, xmax: float) -> None:
        self._bounds = SimpleNamespace(xmin=xmin, xmax=xmax, ymin=-9.5)

    def BoundingBox(self):
        return self._bounds


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
        return SimpleNamespace(
            runner_source=SimpleNamespace(
                bounds_mm=SimpleNamespace(zmin=-22.85, zmax=22.85),
                asset=SimpleNamespace(sha256="runner-sha256"),
            ),
            spacer_source=SimpleNamespace(
                asset=SimpleNamespace(sha256="spacer-sha256")
            ),
            runner_left=SimpleNamespace(
                fixed_member=self._member(0.0, 12.7),
                moving_member=self._member(0.0, 12.7),
            ),
            runner_right=SimpleNamespace(
                fixed_member=self._member(188.3, 201.0),
                moving_member=self._member(188.3, 201.0),
            ),
            spacer_solid=object(),
        )

    def _member(self, xmin, xmax):
        return _RunnerMember(xmin, xmax)

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


__all__ = ["HettichKa4532SpacerMountingTestSupport"]
