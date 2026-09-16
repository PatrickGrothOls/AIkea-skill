"""Scope: Place exact GRASS purchased components with explicit panel ownership."""
from dataclasses import replace
from purchased_hardware_spec import PurchasedHardwareSpec,HardwarePurchaseSpec
from grass_tiomos_155_profile import GRASS_TIOMOS_155


class GrassTiomos155Hardware:
    def build(self, host, plan):
        profile=GRASS_TIOMOS_155
        profile.require_host(host);host.require_current_plan(plan,profile)
        items=[]
        for p in plan.placements:
            origin=profile.source_origin(host,host.support_bottom_mm+p.cabinet_height_mm)
            template=host.door.local_to_parent;basis=template.axis_basis
            axes=tuple(replace(a,x=v[0],y=v[1],z=v[2]) for a,v in zip(
                (basis.local_x_in_parent,basis.local_y_in_parent,basis.local_z_in_parent),
                ((1,0,0),(0,1,0),(0,0,1))))
            frame=replace(template,origin_in_parent=replace(template.origin_in_parent,
                x_mm=origin[0],y_mm=origin[1],z_mm=origin[2]),axis_basis=replace(basis,
                local_x_in_parent=axes[0],local_y_in_parent=axes[1],local_z_in_parent=axes[2]))
            for kind,code,owner in (('hinge','F028122660',host.door.part_id),
                                    ('plate','F058139748',host.support.part_id)):
                name=p.hinge_id+'_grass_'+kind
                items.append(PurchasedHardwareSpec(name,'GRASS',code,'grass-'+code.lower(),frame,
                    purchase=HardwarePurchaseSpec(name,code,'piece','item',('item',),
                        mounting_fasteners_included=False),mounting_part_id=owner))
        return tuple(items)
