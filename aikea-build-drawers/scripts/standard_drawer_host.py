"""Scope: Convert existing standard-cabinet metadata into the explicit drawer host contract."""

from drawer_host import DrawerHost, DrawerHostSpec


class StandardDrawerHost:
    def resolve(self, assembly):
        shelf_bottoms = (float(dict(part.dimensions_mm)["bottom_height"])
                         for part in assembly.parts if part.role == "shelf_panel")
        top = assembly.base_height_mm + min(shelf_bottoms, default=min(point.height_mm for point in assembly.top))
        return DrawerHost(assembly, DrawerHostSpec("left_side", "right_side", 0,
                          assembly.inside_depth_mm, assembly.base_height_mm, top))
