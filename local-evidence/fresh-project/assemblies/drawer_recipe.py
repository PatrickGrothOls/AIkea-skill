"""Scope: Build four-groove drawer boxes and their exact moving KA4532 members."""
from assemblies.design_primitives import P
from assemblies.vilja_inputs import INPUTS as I
from assemblies.panel_assembly import PanelAssemblySpec, PanelAssemblyBuilder
from assemblies.specification import CabineoJointSpec, HardwarePurchaseSpec
from assemblies.connector_hardware import ConnectorHardware
from assemblies.fixing_hardware import FixingHardware


class DrawerRecipe:
    width=I.drawer_box_width
    depth=400
    front_width=I.drawer_front_width

    def build(self,identity,height,members):
        w,d=self.width,self.depth
        parts=[P.panel('left_wall',(d-16,height,16),(0,16,0),axes=((0,1,0),(0,0,1),(1,0,0))),
               P.panel('right_wall',(d-16,height,16),(w,d,0),((0,-1,0),(0,0,1),(-1,0,0))),
               P.panel('front_wall',(self.front_width,height,16),((w-self.front_width)/2,16,0),((1,0,0),(0,0,1),(0,-1,0)),face='<Z',role='drawer_front'),
               P.panel('back_wall',(w-32,height,16),(16,d,0),((1,0,0),(0,0,1),(0,-1,0))),
               P.panel('captured_bottom',(w-16,d-16,6),(8,8,8.1),material='hdf_6')]
        joints=[];operations=[]
        for panel in parts[:4]:
            length=panel.local_size_mm[0]
            start=(0,11.1)
            if panel.part_id=='front_wall':
                length=w-16;start=((self.front_width-w)/2+8,11.1)
            operations.append(P.groove(panel.part_id+'_bottom_groove',panel,start,length,6.2,8))
        for side,front_edge,back_edge in (('left_wall','<X','<X'),('right_wall','>X','>X')):
            joints.append(CabineoJointSpec(side+'_front',side,'front_wall','>Z',front_edge,'explicit',connector_positions_mm=(50,height-35)))
            joints.append(CabineoJointSpec('back_'+side,'back_wall',side,'>Z',back_edge,'explicit',connector_positions_mm=(50,height-35)))
        for hand,part in zip(('left','right'),parts[:2]):
            # One-face pilot drilling exits neatly inside; Ø3 remains a pilot,
            # not a clearance hole. Stock/screw qualification stays recorded.
            xs=(21,149,275) if hand=='left' else (d-37,d-165,d-291)
            operations.append(P.drill(hand+'_runner_pilots',part,tuple((x,35) for x in xs),3,16))
        hardware=[]
        for hand,origin in (('left',(-12.7,11.5,35)),('right',(w+12.7-201,11.5,35))):
            purchase=HardwarePurchaseSpec(identity+'_runners','9114274','pair',hand+'-moving',
                ('left-fixed','left-moving','right-fixed','right-moving'),owner_levels_up=1,mounting_fasteners_included=False)
            hardware.append(P.hardware(hand+'_moving','Hettich','9114274',members[hand+'-moving'],P.frame(origin),hand+'_wall',purchase))
        requirements=tuple(P.unresolved(p.part_id+'_construction',('part:'+p.part_id,),
            'Verify captured-bottom fit, chosen MDF/HDF stock and joined drawer load.') for p in parts)
        spec=PanelAssemblySpec(identity,'complete wooden drawer',tuple(parts),tuple(joints),
            purchased_hardware=tuple(h.spec for h in hardware),machining=tuple(operations),requirements=requirements)
        return FixingHardware().moving_screws(ConnectorHardware().apply(PanelAssemblyBuilder(spec,hardware=tuple(hardware)).build()))
