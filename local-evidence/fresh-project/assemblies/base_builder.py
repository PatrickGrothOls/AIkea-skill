"""Scope: Build a 95mm Korrekt foot base with real plates, deck holes and kickboards."""
from dataclasses import replace
from pathlib import Path
from assemblies.design_primitives import P
from assemblies.vilja_inputs import INPUTS as I
from assemblies.panel_assembly import PanelAssemblyBuilder,PanelAssemblySpec
from assemblies.specification import PurchasedHardwareSpec,HardwarePurchaseSpec
from korrekt_base_layout import KorrektBaseLayout
from korrekt_component_feature import KorrektComponentFeature,KorrektStation
from korrekt_mounting_cutter import KorrektMountingCutter
from base_module_planner import BaseModulePlanner
from cnc_work_area import CncWorkArea


class BaseBuilder:
    layout=KorrektBaseLayout(95,15)

    @classmethod
    def axes(cls,index):
        # Two decks stop1mm short of the shared seam. Keep the full mounting
        # plate15mm inside that actual edge; floor access follows these axes.
        return cls.layout.station_axes(1,I.cabinet_width-1,432,35)

    def build(self):
        parts=[];stations=[]
        # Long-axis sheet orientation fits two 1236.5  x 432 decks in 1220 x2440.
        # Cabinet-run boundaries locate the split; deck clearance is independent.
        spans=((0,I.cabinet_x(0)+I.cabinet_width),(I.cabinet_x(1),I.cabinet_x(1)+I.cabinet_width),
               (I.cabinet_x(2),I.cabinet_x(2)+I.cabinet_width),(I.cabinet_x(3),2475))
        modules=BaseModulePlanner(CncWorkArea('1220x2440-sheet-8mm-tool',2440,1220,8)).plan(spans,432)
        for index,module in enumerate(modules):
            start=module.start_x_mm+(1 if index else 0)
            end=module.end_x_mm-(1 if index<len(modules)-1 else 0)
            name=f'deck_{index+1:02d}'
            parts.append(P.panel(name,(end-start,432,15),(start,0,80),material='birch_plywood_15',role='base_deck'))
            parts.append(P.panel(f'kickboard_{index+1:02d}',(end-start,78,15),(start,35,1),
                ((1,0,0),(0,0,1),(0,-1,0)),material='painted_mdf_15',role='kickboard'))
        for index in range(4):
            x=I.cabinet_x(index);name=f'deck_{index//2+1:02d}'
            for n,(ax,ay) in enumerate(self.axes(index)):
                number=index*4+n+1
                origin=KorrektMountingCutter().placement((x+ax,ay),80,0).toTuple()[0]
                plate=self._purchase(f'plate_{number:02d}','61854',origin,name)
                foot=self._purchase(f'foot_{number:02d}','70151',(x+ax,ay,53.5),name)
                stations.append(KorrektStation(plate,foot))
        req=tuple(P.unresolved(p.part_id+'_attachment',('part:'+p.part_id,),
            'Verify deck load/stock and cabinet fastening; select removable kickboard clips and wall anti-tip anchors.') for p in parts)
        built=PanelAssemblyBuilder(PanelAssemblySpec('base_01','adjustable Korrekt base',tuple(parts),requirements=req)).build()
        feature=KorrektComponentFeature(tuple(p.part_id for p in parts if p.role=='base_deck'),tuple(stations),15)
        return feature.apply(built)

    def _purchase(self,name,article,origin,parent):
        return PurchasedHardwareSpec(name,'Hettich',article,'hettich_korrekt_'+article,P.frame(origin),
            purchase=HardwarePurchaseSpec(name,article,'piece','item',('item',),mounting_fasteners_included=False),mounting_part_id=parent)
