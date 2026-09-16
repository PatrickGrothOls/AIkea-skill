"""Scope: Attach narrow drawer supports, cabinet pilots and exact fixed runner members."""
from dataclasses import replace
from assemblies.design_primitives import P
from assemblies.drawer_recipe import DrawerRecipe
from assemblies.vilja_inputs import INPUTS as I
from assemblies.specification import ChildAssemblySpec, BuiltChildAssembly, HardwarePurchaseSpec
from assemblies.panel_assembly import PanelAssemblyBuilder


class DrawerInstallation:
    def prepare(self,spec,index,members):
        parts=list(spec.parts);operations=list(spec.machining);children=[];hardware=[]
        for n,(row,height) in enumerate(zip(I.drawer_rows[index],I.drawer_heights[index]),1):
            identity=f'drawer_{n:02d}';bottom=row-35
            child=DrawerRecipe().build(identity,height,members)
            cs=ChildAssemblySpec(identity,child.spec.purpose,P.frame((I.drawer_box_x,2,bottom)))
            children.append(BuiltChildAssembly(cs,child))
            for hand,side_name,x,y,xaxis,zaxis in (
                    ('left','left_side',16,20,(0,1,0),(1,0,0)),
                    ('right','right_side',I.cabinet_width-16,416,(0,-1,0),(-1,0,0))):
                name=f'{identity}_{hand}_support'
                # Closed diagnostic: left hardware and right front-wall joinery
                # determine different compact offsets; visible fronts stay centered.
                thickness=I.support_offsets[0 if hand=='left' else 1]
                strip=P.panel(name,(396,80,thickness),(x,y if hand=='left' else 416,row-35),
                    (xaxis,(0,0,1),zaxis),material='calibrated_birch_support')
                parts.append(strip)
                # The pair remains2mm behind the door rear, now0.5mm behind the carcass front.
                rail_x=(19,147,211) if hand=='left' else (416-39,416-167,416-231)
                operations.append(P.drill(name+'_rail_pilots',strip,tuple((d,35) for d in rail_x),3,13))
                fixing_depths=(65,305) if hand=='left' else (85,325);fixing_heights=(15,65)
                coords=tuple((d,h) for d in fixing_depths for h in fixing_heights)
                operations.append(P.drill(name+'_mounting_clearance',strip,coords,4.5,thickness))
                side=spec.part(side_name)
                operations.append(P.drill(name+'_side_pilots',side,tuple((d+(20-I.carcass_front if hand=='left' else 0),row-35+h) for d,h in coords),3,14))
                native_origin=(16+thickness,13.5,row) if hand=='left' else (I.cabinet_width-16-thickness-201,13.5,row)
                purchase=HardwarePurchaseSpec(identity+'_runners','9114274','pair',hand+'-fixed',
                    ('left-fixed','left-moving','right-fixed','right-moving'),mounting_fasteners_included=False)
                hardware.append(P.hardware(identity+'_'+hand+'_fixed','Hettich','9114274',members[hand+'-fixed'],P.frame(native_origin),name,purchase))
        new=replace(spec,parts=tuple(parts),machining=tuple(operations),
            child_assemblies=tuple(c.spec for c in children),purchased_hardware=tuple(h.spec for h in hardware),
            requirements=spec.requirements+tuple(P.unresolved(p.part_id+'_attachment',('part:'+p.part_id,),
                'Closed diagnostic: calibrated birch support stock/lamination remains unselected. Runner Ø4x14; support screws Ø4x60 left (13.7mm penetration) and Ø4x50 right (8.7mm). Stock, engagement/load and full motion require qualification.') for p in parts[len(spec.parts):]))
        return new,tuple(children),tuple(hardware)
