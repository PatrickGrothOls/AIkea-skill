"""Scope: Create fresh carcass panels, paired Cabineo construction and shared grids."""
from math import hypot
from assemblies.design_primitives import P
from assemblies.vilja_inputs import INPUTS as I
from assemblies.specification import CabineoJointSpec, JointSpec, PartMachiningSpec
from assemblies.panel_assembly import PanelAssemblySpec


class CarcassRecipe:
    def create(self,index):
        top=I.top(index); width=I.cabinet_width;depth=416-I.carcass_front
        left_h,right_h=top[0][1],top[-1][1]
        door_top=((0,I.ceiling(I.cabinet_x(index)+I.door_x)-I.base_height-I.top_fit-2),
                  *((x-I.door_x,h-2) for x,h in top[1:-1]),
                  (I.door_width,I.ceiling(I.cabinet_x(index)+I.door_x+I.door_width)-I.base_height-I.top_fit-2))
        flat_left=top[0][1]==top[1][1];flat_right=top[-2][1]==top[-1][1]
        parts=[P.panel('left_side',(depth,left_h-(16 if flat_left else 0),16),(0,I.carcass_front,0),axes=((0,1,0),(0,0,1),(1,0,0)),role='side_panel'),
               P.panel('right_side',(depth,right_h-(16 if flat_right else 0),16),(width,416,0),((0,-1,0),(0,0,1),(-1,0,0)),role='side_panel'),
               P.panel('back_panel',(width,max(left_h,right_h),16),(0,432,0),((1,0,0),(0,0,1),(0,-1,0)),outline=((0,0),(width,0),*reversed(top)),role='back_panel'),
               P.panel('floor_panel',(width-32,depth,16),(16,I.carcass_front,0),role='floor_panel'),
               P.panel('door_panel',(I.door_width,max(h for x,h in door_top),18),(I.door_x,0,1),((1,0,0),(0,0,1),(0,-1,0)),face='<Z',role='door_panel',
                       outline=((0,0),(I.door_width,0),*reversed(door_top)),material='painted_mdf_18')]
        joints=[CabineoJointSpec('left_back','left_side','back_panel','>Z','>X','bounded_spacing'),
                CabineoJointSpec('right_back','right_side','back_panel','>Z','<X','bounded_spacing'),
                CabineoJointSpec('floor_left','floor_panel','left_side','>Z','<X','explicit',connector_positions_mm=(85,325)),
                CabineoJointSpec('floor_right','floor_panel','right_side','>Z','>X','explicit',connector_positions_mm=(85,325))]
        tops=[]
        for n,((x0,z0),(x1,z1)) in enumerate(zip(top,top[1:]),1):
            length=hypot(x1-x0,z1-z0);dx=(x1-x0)/length;dz=(z1-z0)/length
            name=f'top_panel_{n:02d}';tops.append(name)
            parts.append(P.panel(name,(length,depth,16),(x0+dz*16,I.carcass_front,z0-dx*16),((dx,0,dz),(0,1,0),(-dz,0,dx)),face='<Z',role='top_panel'))
            joints.append(CabineoJointSpec(f'{name}_back',name,'back_panel','<Z','>Y','bounded_spacing'))
        for side,top_name,flat in (('left_side',tops[0],flat_left),('right_side',tops[-1],flat_right)):
            joints.append(CabineoJointSpec(side+'_top',side,top_name,'>Z','>Y','explicit',connector_positions_mm=(85,325)) if flat else
                          JointSpec(side+'_top',(top_name,side),'angled_panel_seam','equal_thickness_miter'))
        joints.extend(JointSpec(a+'_'+b,(a,b),'top_boundary_seam','equal_thickness_miter') for a,b in zip(tops,tops[1:]))
        requirements=tuple(P.unresolved(p.part_id+'_installation',('part:'+p.part_id,),
            'Verify material, structural support, assembly and load; real joinery operations are retained.') for p in parts)
        machining=tuple(PartMachiningSpec(s+'_grid',s,'system_32') for s in ('left_side','right_side'))
        return PanelAssemblySpec(f'cabinet_{index+1:02d}','wardrobe bay',tuple(parts),tuple(joints),machining=machining,requirements=requirements)
