"""Scope: Emit exact selected KA 5332 host fixings and declare matching prior holes."""

from dataclasses import replace

from drawer_part_locator import DrawerAxisBasis, DrawerAxisDirection, DrawerPartPlacement, DrawerPoint3D
from panel_machining_builder import PanelMachiningBuilder
from surface_drilling_reuse import SurfaceDrillingReuse
from surface_drilling_spec import SurfaceDrillingSpec
from surface_hole_pattern import SurfaceHole
from drawer_host import DrawerHost


class HettichKa5332HostDrillingRecipe:
    def build(self, parent, drawers):
        host = DrawerHost.resolve(parent)
        prior = PanelMachiningBuilder().build(host.assembly).all
        requests = []
        for drawer in drawers:
            profile = drawer.runner
            world_height = drawer.origin_in_parent_mm[2] + profile.runner_center_from_drawer_bottom_mm
            for side in ("left", "right"):
                part = host.part(side)
                _, height, thickness = part.local_size_mm
                top = part.inside_face == ">Z"
                origin, y_axis, z_axis = ((0, height, thickness), (0, -1, 0), (0, 0, -1)) if top else ((0, 0, 0), (0, 1, 0), (0, 0, 1))
                surface = DrawerPartPlacement(DrawerPoint3D(*origin), DrawerAxisBasis(
                    DrawerAxisDirection(1, 0, 0), DrawerAxisDirection(*y_axis), DrawerAxisDirection(*z_axis)))
                positions = tuple(host.frame(side).to_local((host.inside_x(side), host.spec.front_mm+value, world_height))
                                  for value in profile.cabinet_fixing_positions_from_front_mm)
                holes = tuple(SurfaceHole(f"fixing_{index}", x, height-y if top else y,
                                         profile.cabinet_hole_diameter_mm, profile.cabinet_hole_depth_mm)
                              for index, (x, y, _) in enumerate(positions, start=1))
                request = SurfaceDrillingSpec(f"{drawer.drawer.assembly_id}_{part.part_id}_fixings", part.part_id, surface, holes)
                requests.append(replace(request, reuse_machining_ids=SurfaceDrillingReuse().matching_operations(request, prior)))
        return tuple(requests)
