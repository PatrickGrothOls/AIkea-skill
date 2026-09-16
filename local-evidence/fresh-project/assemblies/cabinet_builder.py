"""Scope: Compose one complete fresh cabinet through shared construction features."""
from dataclasses import replace
from pathlib import Path
from functools import lru_cache
import cadquery as cq
import json
from assemblies.carcass_recipe import CarcassRecipe
from assemblies.drawer_installation import DrawerInstallation
from assemblies.shelves_recipe import ShelvesRecipe
from assemblies.panel_assembly import PanelAssemblyBuilder
from assemblies.specification import BuiltPurchasedHardware
from assemblies.vilja_inputs import INPUTS as I
from assemblies.design_primitives import P
from door_host import DoorHost, DoorHostSpec
from door_hinge_side import DoorHingeSide
from grass_tiomos_155_plan import GrassTiomos155Planner
from grass_tiomos_155_machining import GrassTiomos155Machining
from grass_tiomos_155_hardware import GrassTiomos155Hardware
from grass_tiomos_155_loader import GrassTiomos155Loader
from panel_hardware_reservation import PanelHardwareReservation
from lighting_component_feature import LightingComponentFeature
from part_lighting_plan import PartLightingPlan
from lighting_run import LightingRun
from recessed_luminaire_profile import DOMUS_APEX_84_HI
from hettich_ka_4532_400_step_set import HettichKa4532FourHundredStepLoader
from korrekt_floor_access_feature import KorrektFloorAccessFeature
from assemblies.base_builder import BaseBuilder
from assemblies.connector_hardware import ConnectorHardware
from assemblies.fixing_hardware import FixingHardware
from assemblies.grass_fixing_hardware import GrassFixingHardware


class SourceLibrary:
    root=Path(__file__).resolve().parents[1]

    @classmethod
    @lru_cache(maxsize=1)
    def runners(cls):
        return HettichKa4532FourHundredStepLoader().load(cls.root/'hardware/hettich/ka-4532-silent-system/9114274/source').members

    @classmethod
    @lru_cache(maxsize=1)
    def hinges(cls):
        return GrassTiomos155Loader().load(cls.root/'hardware/grass')


class CabinetBuilder:
    def __init__(self,index):
        self.index=index

    def build(self):
        print(f'Building cabinet {self.index+1}: drawers and shared panels',flush=True)
        spec=CarcassRecipe().create(self.index)
        spec,children,hardware=DrawerInstallation().prepare(spec,self.index,SourceLibrary.runners())
        spec,hardware=ShelvesRecipe().prepare(spec,self.index,hardware)
        host=DoorHost(spec,DoorHostSpec('door_panel','left_side'),DoorHingeSide.LEFT)
        mass=json.loads((SourceLibrary.root/'reviews/door-proposal-mass.json').read_text())['doors'][self.index]
        plan=GrassTiomos155Planner().plan(host,mass['proposed_hinge_count'],
            mass['estimated_panel_and_finish_kg'],self._reservations(spec))
        requests=GrassTiomos155Machining().build(host,plan)
        hinges=GrassTiomos155Hardware().build(host,plan)
        sources=SourceLibrary.hinges()
        hardware+=tuple(BuiltPurchasedHardware(h,cq.Workplane(obj=sources.hinge if h.product_code=='F028122660' else sources.plate)) for h in hinges)
        qualifications=tuple(P.unresolved('grass_qualification_'+str(n),('part:door_panel',),issue)
            for n,issue in enumerate(plan.compatibility_issues))
        spec=replace(spec,machining=spec.machining+requests,purchased_hardware=tuple(h.spec for h in hardware),
            requirements=spec.requirements+qualifications)
        built=PanelAssemblyBuilder(spec,children=children,hardware=hardware).build()
        built=GrassFixingHardware().apply(built,host,plan)
        built=KorrektFloorAccessFeature('floor_panel',BaseBuilder.axes(self.index)).apply(built)
        for plan in self.lighting_plans(spec):
            built=LightingComponentFeature(plan).apply(built)
        print(f'Completed cabinet {self.index+1}: {len(built.parts)} host panels and {len(children)} drawers',flush=True)
        return FixingHardware().apply(ConnectorHardware().apply(built))

    def lighting_plans(self,spec):
        for part in spec.parts:
            if part.part_id=='right_side':
                run=LightingRun('right_light',(396,16),(396,part.local_size_mm[1]-20),4300,DOMUS_APEX_84_HI)
            elif part.role=='top_panel':
                run=LightingRun(part.part_id+'_light',(50,20-I.carcass_front),(part.local_size_mm[0]-50,20-I.carcass_front),4300,DOMUS_APEX_84_HI)
            else:
                continue
            yield PartLightingPlan(spec.assembly_id,part.part_id,part.inside_face,run)

    def _reservations(self,spec):
        records=[]
        for n,row in enumerate(I.shelf_rows[self.index]):
            records.append(PanelHardwareReservation(f'shelf_{n}','shelf','left_side',(row,),(2,412),(row-3,row+19)))
        for n,row in enumerate(I.drawer_rows[self.index]):
            records.append(PanelHardwareReservation(f'drawer_{n}','runner','left_side',(),(0,416),(row-37,row+47)))
        return tuple(records)
