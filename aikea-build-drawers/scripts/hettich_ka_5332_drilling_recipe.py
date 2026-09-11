"""Scope: Convert the selected KA 5332 drawer fixing profile into explicit drilling requests."""

from drawer_part_locator import DrawerAxisBasis, DrawerAxisDirection, DrawerPartPlacement, DrawerPoint3D
from surface_drilling_spec import SurfaceDrillingSpec
from surface_hole_pattern import SurfaceHole


class HettichKa5332DrillingRecipe:
    """Keep the current manufacturer pattern and each hand in the saved construction input."""

    def drawer(self, box, profile):
        requests = []
        for part_id in ("left_side", "right_side"):
            length, height, thickness = box.part(part_id).local_size_mm
            positions = tuple(length-value if part_id == "left_side" else value
                              for value in profile.drawer_fixing_positions_from_front_mm)
            surface = DrawerPartPlacement(DrawerPoint3D(0, height, thickness), DrawerAxisBasis(
                DrawerAxisDirection(1, 0, 0), DrawerAxisDirection(0, -1, 0), DrawerAxisDirection(0, 0, -1)))
            holes = tuple(SurfaceHole(f"fixing_{index}", x, height-profile.runner_center_from_drawer_bottom_mm,
                                     profile.drawer_pilot_diameter_mm, profile.drawer_pilot_depth_mm)
                          for index, x in enumerate(positions, start=1))
            requests.append(SurfaceDrillingSpec(f"{part_id}_runner_fixings", part_id, surface, holes))
        return tuple(requests)
