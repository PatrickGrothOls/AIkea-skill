"""Scope: Emit explicit NC70 cup and grid-mounted plate drilling for an existing door plan."""

from dataclasses import replace

from panel_machining_builder import PanelMachiningBuilder
from riex_nc70_cup_pattern import RiexNc70CupPattern
from surface_drilling_reuse import SurfaceDrillingReuse
from surface_drilling_spec import SurfaceDrillingSpec
from surface_hole_pattern import SurfaceHole
from system_32_side_panel_grid import System32SidePanelGrid


class RiexNc70MachiningRecipe:
    def build(self, assembly, plan, profile, pilot_diameter_mm=2.5, pilot_depth_mm=10.0):
        grid = System32SidePanelGrid().profile
        if (profile.plate_mounting_interface != "system_32_euroscrew_pair" or
                profile.plate_required_hole_diameter_mm != grid.hole_diameter_mm or
                profile.plate_required_hole_depth_mm > grid.hole_depth_mm or
                profile.plate_fixing_spacing_mm != grid.row_pitch_mm):
            raise ValueError("selected hinge plate does not match the configured System 32 interface")
        door, side = assembly.part("door_panel"), assembly.part(plan.hinge_side.side_part_id)
        pattern = RiexNc70CupPattern(profile, pilot_diameter_mm, pilot_depth_mm).build()
        prior = PanelMachiningBuilder().build(assembly).all
        requests = []
        left = plan.hinge_side.value == "left"
        cup_x = profile.cup_center_from_edge_mm if left else plan.door_width_mm-profile.cup_center_from_edge_mm
        for placement in plan.placements:
            rows = placement.cabinet_fixing_rows_mm
            if (len(rows) != 2 or abs(rows[1]-rows[0]-grid.row_pitch_mm) > 1e-6 or
                    abs(sum(rows)/2-placement.cabinet_height_mm) > 1e-6):
                raise ValueError("hinge plate rows must share the declared mounting center")
            surface = self._surface(door, (cup_x, placement.door_height_mm, 0),
                                    ((1, 0, 0), (0, 1, 0), (0, 0, 1)) if left else
                                    ((-1, 0, 0), (0, -1, 0), (0, 0, 1)))
            requests.append(SurfaceDrillingSpec(f"{placement.hinge_id}_door_cup", door.part_id, surface, pattern.holes))
            depth, height, thickness = side.local_size_mm
            top = side.inside_face == ">Z"
            if side.inside_face not in ("<Z", ">Z"):
                raise ValueError("hinge support must declare its inside broad face")
            surface = self._surface(side, (0, height, thickness) if top else (0, 0, 0),
                                    ((1, 0, 0), (0, -1, 0), (0, 0, -1)) if top else
                                    ((1, 0, 0), (0, 1, 0), (0, 0, 1)))
            x = profile.plate_line_from_front_mm if left else depth-profile.plate_line_from_front_mm
            holes = tuple(SurfaceHole(f"fixing_{index}", x, height-row if top else row,
                                     grid.hole_diameter_mm, grid.hole_depth_mm)
                          for index, row in enumerate(rows, 1))
            request = SurfaceDrillingSpec(f"{placement.hinge_id}_mounting_plate", side.part_id, surface, holes)
            requests.append(replace(request, reuse_machining_ids=SurfaceDrillingReuse().matching_operations(request, prior)))
        return tuple(requests)

    def _surface(self, part, origin, axes):
        frame = part.local_to_parent
        basis = frame.axis_basis
        directions = tuple(replace(axis, x=value[0], y=value[1], z=value[2])
                           for axis, value in zip((basis.local_x_in_parent, basis.local_y_in_parent, basis.local_z_in_parent), axes))
        return replace(frame, origin_in_parent=replace(frame.origin_in_parent, x_mm=origin[0], y_mm=origin[1], z_mm=origin[2]),
                       axis_basis=replace(basis, local_x_in_parent=directions[0], local_y_in_parent=directions[1], local_z_in_parent=directions[2]))
