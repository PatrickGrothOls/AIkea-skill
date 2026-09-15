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
            cs=ChildAssemblySpec(identity,child.spec.purpose,P.frame((53.7,2,bottom)))
            children.append(BuiltChildAssembly(cs,child))
            for hand,side_name,x,y,xaxis,zaxis in (
                    ('left','left_side',16,20,(0,1,0),(1,0,0)),
                    ('right','right_side',I.cabinet_width-16,416,(0,-1,0),(-1,0,0))):
                name=f'{identity}_{hand}_support'
                # 396 x80 x25 strip starts20mm back to clear the structural front.
                strip=P.panel(name,(396,80,25),(x,y if hand=='left' else 416,row-35),
                    (xaxis,(0,0,1),zaxis),material='birch_plywood_25')
                parts.append(strip)
                # One 2mm inset moves the entire unchanged runner pair and box.
                rail_x=(19,147,211) if hand=='left' else (416-39,416-167,416-231)
                operations.append(P.drill(name+'_rail_pilots',strip,tuple((d,35) for d in rail_x),3,13))
                fixing_depths=(65,305) if hand=='left' else (85,325);fixing_heights=(15,65)
                coords=tuple((d,h) for d in fixing_depths for h in fixing_heights)
                operations.append(P.drill(name+'_mounting_clearance',strip,coords,4.5,25))
                side=spec.part(side_name)
                operations.append(P.drill(name+'_side_pilots',side,tuple((d+(20 if hand=='left' else 0),row-35+h) for d,h in coords),3,13))
                native_origin=(41,13.5,row) if hand=='left' else (I.cabinet_width-41-201,13.5,row)
                purchase=HardwarePurchaseSpec(identity+'_runners','9114274','pair',hand+'-fixed',
                    ('left-fixed','left-moving','right-fixed','right-moving'),mounting_fasteners_included=False)
                hardware.append(P.hardware(identity+'_'+hand+'_fixed','Hettich','9114274',members[hand+'-fixed'],P.frame(native_origin),name,purchase))
        new=replace(spec,parts=tuple(parts),machining=tuple(operations),
            child_assemblies=tuple(c.spec for c in children),purchased_hardware=tuple(h.spec for h in hardware),
            requirements=spec.requirements+tuple(P.unresolved(p.part_id+'_attachment',('part:'+p.part_id,),
                'Runner Ø4x14 into 25mm birch strip; strip Ø4x35 through 25mm into 16mm MDF. Verify bearing, pullout and pilots on actual stock.') for p in parts[len(spec.parts):]))
        return new,tuple(children),tuple(hardware)
