"""Scope: Save editable hinge drilling and independent installation obligations."""

from riex_nc70_machining_recipe import RiexNc70MachiningRecipe
from surface_drilling_source_renderer import SurfaceDrillingSourceRenderer


class DoorMachiningSourceRenderer:
    def render(self, assembly, plan, profile):
        requests = RiexNc70MachiningRecipe().build(assembly, plan, profile)
        machining = "\n".join(f"    {SurfaceDrillingSourceRenderer().render(request)}," for request in requests)
        requirements = "\n".join(
            f"    ConstructionRequirementSpec({request.machining_id!r}, 'Verify declared hinge machining', "
            f"{('part:' + request.part_id,)!r}, {('machining:' + request.machining_id,)!r}, 'operations'),"
            for request in requests)
        subjects = (f'part:{plan.door_part_id}', f'part:{plan.support_part_id}',
                    *(f'hardware:{placement.hinge_id}_{item}' for placement in plan.placements for item in ('hinge', 'plate')))
        return ('"""Scope: Declare this door feature machining and required installation evidence."""\n\n'
                'from assemblies.specification import (AxisBasis, AxisDirection, LocalToParentPlacement, Point3D,\n'
                '    SurfaceDrillingSpec, ConstructionRequirementSpec)\n'
                'from surface_hole_pattern import SurfaceHole\n\n'
                f'DOOR_MACHINING = (\n{machining}\n)\n\n'
                f'DOOR_REQUIREMENTS = (\n{requirements}\n'
                f"    ConstructionRequirementSpec('door_hinge_installation', 'Verify exact hinges, attachment and opening movement', {subjects!r}, "
                "('feature:door_hinges.feature',), 'operations'),\n"
                "    ConstructionRequirementSpec('door_fixing_pilots', 'Confirm the selected cup fixing screws and pilot suitability', "
                f"{('part:' + plan.door_part_id,)!r}, basis='The retained 2.5 by 10 mm pilot choice is not manufacturer screw authority'),\n)\n")
