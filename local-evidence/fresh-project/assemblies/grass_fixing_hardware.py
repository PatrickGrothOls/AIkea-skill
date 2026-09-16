"""Scope: Keep selected GRASS installation screws visible and counted without claiming exact CAD."""
from dataclasses import replace
import cadquery as cq
from assemblies.design_primitives import P
from grass_tiomos_155_profile import GRASS_TIOMOS_155


class GrassFixingHardware:
    def apply(self,built,host,plan):
        items=list(built.purchased_hardware)
        for placement in plan.placements:
            x,y,z=GRASS_TIOMOS_155.source_origin(host,placement.cabinet_height_mm)
            # Published Ø3.5x15 countersunk screw; simplified core/head only.
            # Cup flange top is3.15mm ahead of the door rear. Plate head seating
            # uses a provisional3mm stand-off and remains a fit qualification.
            targets=[(host.door.part_id,(x+15,host.front_mm+3.15,z+dz),(0,-1,0)) for dz in (-22.5,22.5)]
            targets += [(host.support.part_id,(host.inside_x_mm+3,y+dy,z+dz),(-1,0,0))
                for dy,dz in GRASS_TIOMOS_155.plate_fixing_offsets_mm]
            for n,(owner,head,direction) in enumerate(targets):
                axis=cq.Vector(*direction);point=cq.Vector(*head)
                head_solid=cq.Solid.makeCone(3.5,1.75,1.75,point,axis)
                core=cq.Solid.makeCylinder(1.4,13.25,point+axis.multiply(1.75),axis)
                items.append(P.hardware(placement.hinge_id+f'_grass_screw_{n+1:02d}',
                    'GRASS','F072135961 / Ø3.5×15',head_solid.fuse(core),P.frame(),owner))
        requirement=P.unresolved('grass_fastener_qualification',('part:door_panel','part:left_side'),
            'Selected GRASS F072135961 Ø3.5x15 Night screws have illustrative geometry. Verify head seating, pilot sizing and MDF holding; plate stand-off is provisional. Door penetration11.85mm, side12mm at represented seating.')
        return replace(built,spec=replace(built.spec,purchased_hardware=tuple(h.spec for h in items),
            requirements=built.spec.requirements+(requirement,)),purchased_hardware=tuple(items))
