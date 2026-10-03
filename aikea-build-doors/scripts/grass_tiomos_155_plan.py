"""Scope: Spread GRASS wood-screw plates around owned cabinet features without consuming grid holes."""
from door_hinge_plan import DoorHingePlan, DoorHingePlacement
from door_hinge_spread_policy import DoorHingeSpreadPolicy
from panel_hardware_reservation import PanelHardwareReservation
from system_32_side_panel_grid import System32SidePanelGrid
from grass_tiomos_155_profile import GRASS_TIOMOS_155


class GrassTiomos155Planner:
    def plan(self, host, count, mass_estimate_kg, reservations=()):
        profile=GRASS_TIOMOS_155
        profile.require_host(host)
        spread=DoorHingeSpreadPolicy()
        height=host.dimensions['left_height']
        offset=host.door_bottom_mm-host.support_bottom_mm
        # Centers on grid rows place the wood-screw pair HALF a pitch away
        # from existing5 mm holes. The plate's other pair is on different depths.
        candidates=tuple(z for z in System32SidePanelGrid().row_heights_mm(host.support.local_size_mm[1])
                         if spread.contains(z-offset,height) and self._clears_roof(host,z))
        chosen=[]
        occupied=list(reservations)+list(host.fixed_reservations)
        for target in spread.ideal_centers_mm(height,count):
            available=tuple(z for z in candidates if z not in chosen and
                not any(self.reservation(host,z).conflicts_with(r) for r in occupied))
            if not available:
                raise ValueError('GRASS plate has no clear position within the intended hinge spread')
            z=min(available,key=lambda z:(abs(z-offset-target),z))
            chosen.append(z);occupied.append(self.reservation(host,z))
        return DoorHingePlan(host.assembly_id,profile.profile_id,profile.relationship,
            host.hinge_side,host.dimensions['width'],height,host.dimensions['thickness'],
            mass_estimate_kg,host.overlay_mm,
            tuple(DoorHingePlacement(f'hinge_{i:02d}',z-offset,z,())
                  for i,z in enumerate(sorted(chosen),1)),
            ('Provisional reference-width choice: supplier/trial-fit load qualification pending',
             'Moving hinge-arm/open-position evidence pending; no full-motion approval',
             'Stock, finish, moving hardware mass and screw holding require qualification'),host.spec)

    def _clears_roof(self,host,center):
        # The side-edge margin alone misses roofs descending over the hinge arm.
        # A source-body bounding box below the actual inner roof plane gives a
        # conservative closed clearance; this is not an opening-envelope proof.
        left=host.inside_x_mm+3-13;right=host.inside_x_mm+3+53.953542539
        top=host.support_bottom_mm+center+31
        for part in host.assembly.parts:
            if part.role!='top_panel':continue
            frame=host._frame(part);origin=frame.origin_mm;normal=frame.local_z_in_owner
            end=frame.to_owner((part.local_size_mm[0],0,0))
            low=max(left,min(origin[0],end[0]));high=min(right,max(origin[0],end[0]))
            if low>high:continue
            ceiling=min(origin[2]-normal[0]*(x-origin[0])/normal[2] for x in (low,high))
            if top+2>ceiling:return False
        return True

    def reservation(self, host, center):
        p=GRASS_TIOMOS_155
        y=p.source_origin(host,center)[1]-host.support_front_mm
        return PanelHardwareReservation('grass_hinge','hinge_plate',host.support.part_id,(),
            (y-25.55,y+42.71394913),(center-31,center+31))
