"""Scope: Express exact GRASS cup/four-point plate axes as one-face drilling requests."""
from dataclasses import replace
from surface_drilling_spec import SurfaceDrillingSpec
from surface_hole_pattern import SurfaceHole
from grass_tiomos_155_profile import GRASS_TIOMOS_155


class GrassTiomos155Machining:
    def build(self, host, plan):
        profile=GRASS_TIOMOS_155
        profile.require_host(host);host.require_current_plan(plan,profile)
        requests=[]
        for placement in plan.placements:
            height=host.support_bottom_mm+placement.cabinet_height_mm
            origin=profile.source_origin(host,height)
            cup=(SurfaceHole('cup',23.5,placement.door_height_mm,35,11.5),)
            pilots=tuple(SurfaceHole(f'cup_screw_{i}',33,placement.door_height_mm+z,2.5,12)
                         for i,z in enumerate((-22.5,22.5),1))
            requests.append(self._request(placement.hinge_id+'_grass_cup',host.door,cup+pilots))
            coords=tuple(host.support_frame.to_local((host.inside_x_mm,origin[1]+y,height+z))
                         for y,z in profile.plate_fixing_offsets_mm)
            holes=tuple(SurfaceHole(f'plate_screw_{i}',x,y,2.5,12)
                        for i,(x,y,z) in enumerate(coords,1))
            requests.append(self._request(placement.hinge_id+'_grass_plate',host.support,holes))
        return tuple(requests)

    def _request(self, name, part, holes):
        top=part.inside_face=='>Z';w,h,t=part.local_size_mm
        holes=tuple(replace(hole,y_mm=h-hole.y_mm) for hole in holes) if top else holes
        origin=(0,h,t) if top else (0,0,0)
        axes=((1,0,0),(0,-1,0),(0,0,-1)) if top else ((1,0,0),(0,1,0),(0,0,1))
        frame=part.local_to_parent;basis=frame.axis_basis
        directions=tuple(replace(axis,x=v[0],y=v[1],z=v[2]) for axis,v in zip(
            (basis.local_x_in_parent,basis.local_y_in_parent,basis.local_z_in_parent),axes))
        local=replace(frame,origin_in_parent=replace(frame.origin_in_parent,
            x_mm=origin[0],y_mm=origin[1],z_mm=origin[2]),axis_basis=replace(basis,
            local_x_in_parent=directions[0],local_y_in_parent=directions[1],local_z_in_parent=directions[2]))
        return SurfaceDrillingSpec(name,part.part_id,local,holes)
