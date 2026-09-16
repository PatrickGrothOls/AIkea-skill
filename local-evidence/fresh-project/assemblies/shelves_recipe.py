"""Scope: Seat thirteen removable shelves on four supplier-specific grid pins each."""
from dataclasses import replace
import cadquery as cq
from assemblies.design_primitives import P
from assemblies.vilja_inputs import INPUTS as I


class ShelvesRecipe:
    def prepare(self,spec,index,hardware):
        parts=list(spec.parts);items=list(hardware)
        # Diameter is supplier-confirmed. 8mm insertion and 8mm bearing are
        # explicit visual assumptions, never inferred from the 13mm bore depth.
        pin=cq.Workplane('XY').circle(2.5).extrude(16)
        for n,row in enumerate(I.shelf_rows[index],1):
            name=f'shelf_{n:02d}'
            parts.append(P.panel(name,(I.opening_width-2,410,16),(17,2,row+2.5),role='shelf_panel'))
            for hand,x,zaxis in (('left',8,(1,0,0)),('right',I.cabinet_width-8,(-1,0,0))):
                for column,y in (('front',I.carcass_front+37),('rear',379)):
                    items.append(P.hardware(name+'_'+hand+'_'+column,'Røverkøb','16415 / LN 206.129.2',pin,
                        P.frame((x,y,row),(0,1,0),(0,0,1),zaxis) if hand=='left' else P.frame((x,y,row),(0,-1,0),(0,0,1),zaxis),hand+'_side'))
        requirements=spec.requirements+tuple(P.unresolved(p.part_id+'_support',('part:'+p.part_id,),
            'Four selected Ø5 pins on shared rows; supplier insertion/bearing dimensions and actual coated fit/load remain unverified.') for p in parts[len(spec.parts):])
        return replace(spec,parts=tuple(parts),purchased_hardware=tuple(h.spec for h in items),requirements=requirements),tuple(items)
