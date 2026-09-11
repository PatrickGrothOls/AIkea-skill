"""Scope: Serialize an explicit drilling request into editable generated Python inputs."""


class SurfaceDrillingSourceRenderer:
    def render(self, request):
        placement = request.surface_to_part
        origin, axes = placement.origin_in_parent, placement.axis_basis
        point = (origin.x_mm, origin.y_mm, origin.z_mm)
        directions = ", ".join(f"AxisDirection{(axis.x, axis.y, axis.z)!r}"
                               for axis in (axes.local_x_in_parent, axes.local_y_in_parent, axes.local_z_in_parent))
        frame = f"LocalToParentPlacement(Point3D{point!r}, AxisBasis({directions}))"
        return f"SurfaceDrillingSpec({request.machining_id!r}, {request.part_id!r}, {frame}, {request.holes!r})"
