"""Scope: Emit exact selected KA 5332 host fixings and declare matching prior holes."""

from dataclasses import replace

from drawer_part_locator import DrawerAxisBasis, DrawerAxisDirection, DrawerPartPlacement, DrawerPoint3D
from panel_machining_builder import PanelMachiningBuilder
from surface_drilling_reuse import SurfaceDrillingReuse
from surface_drilling_spec import SurfaceDrillingSpec
from surface_hole_pattern import SurfaceHole


class HettichKa5332HostDrillingRecipe:
    def build(self, parent, drawers):
        prior = PanelMachiningBuilder().build(parent).all
        requests = []
        for drawer in drawers:
            profile = drawer.runner
            row = drawer.hardware_mounting.system_32_row_height_mm
            for part_id in ("left_side", "right_side"):
                depth, height, thickness = parent.part(part_id).local_size_mm
                positions = tuple(value if part_id == "left_side" else depth-value
                                  for value in profile.cabinet_fixing_positions_from_front_mm)
                surface = DrawerPartPlacement(DrawerPoint3D(0, height, thickness), DrawerAxisBasis(
                    DrawerAxisDirection(1, 0, 0), DrawerAxisDirection(0, -1, 0), DrawerAxisDirection(0, 0, -1)))
                holes = tuple(SurfaceHole(f"fixing_{index}", x, height-row,
                                         profile.cabinet_hole_diameter_mm, profile.cabinet_hole_depth_mm)
                              for index, x in enumerate(positions, start=1))
                request = SurfaceDrillingSpec(f"{drawer.drawer.assembly_id}_{part_id}_fixings", part_id, surface, holes)
                requests.append(replace(request, reuse_machining_ids=SurfaceDrillingReuse().matching_operations(request, prior)))
        return tuple(requests)
