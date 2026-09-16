"""Scope: Verify the complete proposed run's closed GRASS datums without replacing the viewer."""
from pathlib import Path
from dataclasses import replace
import json,sys
package=Path.cwd();root=package/'local-evidence/fresh-project'
sys.path[:0]=[str(package/(name+'/scripts')) for name in
    ('aikea-review-unit','aikea-build-units','aikea-build-drawers','aikea-build-doors','aikea-add-lighting','aikea')]+[str(root)]
import assemblies.carcass_recipe as recipe
from door_host import DoorHost,DoorHostSpec
from door_hinge_side import DoorHingeSide
from grass_tiomos_155_plan import GrassTiomos155Planner
from grass_tiomos_155_machining import GrassTiomos155Machining
from grass_tiomos_155_hardware import GrassTiomos155Hardware
from grass_tiomos_155_loader import GrassTiomos155Loader
from grass_tiomos_155_profile import GRASS_TIOMOS_155
from panel_hardware_reservation import PanelHardwareReservation
from OCP.OSD import OSD_Parallel,OSD_ThreadPool
OSD_Parallel.SetUseOcctThreads_s(True)
pool=OSD_ThreadPool.DefaultPool_s(1);pool.Init(1);pool.SetNbDefaultThreadsToLaunch(1)


class GrassInstallationCheck:
    def run(self):
        recipe.I=replace(recipe.I,cabinet_width=618.75,cabinet_pitch=618.75,first_x=0,door_overlay=15)
        masses=json.loads((root/'reviews/door-proposal-mass.json').read_text())['doors']
        sources=GrassTiomos155Loader().load(root/'hardware/grass')
        records=[]
        for index,mass in enumerate(masses):
            spec=recipe.CarcassRecipe().create(index)
            host=DoorHost(spec,DoorHostSpec('door_panel','left_side'),DoorHingeSide.LEFT)
            reservations=tuple(PanelHardwareReservation(f'shelf_{n}','shelf','left_side',(),(2,412),(z-3,z+19))
                for n,z in enumerate(recipe.I.shelf_rows[index]))+tuple(
                PanelHardwareReservation(f'drawer_{n}','runner','left_side',(),(0,416),(z-37,z+47))
                for n,z in enumerate(recipe.I.drawer_rows[index]))
            plan=GrassTiomos155Planner().plan(host,mass['proposed_hinge_count'],
                mass['estimated_panel_and_finish_kg'],reservations)
            machining=GrassTiomos155Machining().build(host,plan)
            hardware=GrassTiomos155Hardware().build(host,plan)
            for p in plan.placements:
                origin=GRASS_TIOMOS_155.source_origin(host,p.cabinet_height_mm)
                assert abs(origin[0]+5.5-(host.door_edge_x_mm+23.5))<1e-8
                assert abs(origin[1]-38.5-host.front_mm)<1e-8
            record=dict(assembly=spec.assembly_id,centres_mm=[p.cabinet_height_mm for p in plan.placements],
                machining_requests=len(machining),purchased_bodies=len(hardware),
                cup_depth_mm=11.5,cup_retained_stock_mm=6.5,plate_pilot_depth_mm=12,
                side_retained_stock_mm=4,qualifications=plan.compatibility_issues)
            records.append(record);print(json.dumps(record),flush=True)
        result=dict(status='closed_datum_and_pattern_preflight_only',records=records,
            native_pair_overlap_mm3=sources.hinge.intersect(sources.plate).Volume(),
            pair_overlap_qualification='Source representations overlap in their inferred assembled frame; clip engagement versus simplification remains unresolved. No clash-free mechanical approval.',
            open_motion='Manufacturer door flush at90 degrees is verified; complete moving-arm path is not.')
        (root/'reviews/grass-installation-preflight.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    GrassInstallationCheck().run()
