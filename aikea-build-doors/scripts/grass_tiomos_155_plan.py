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
                         if spread.contains(z-offset,height))
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

    def reservation(self, host, center):
        p=GRASS_TIOMOS_155
        y=p.source_origin(host,center)[1]-host.support_front_mm
        return PanelHardwareReservation('grass_hinge','hinge_plate',host.support.part_id,(),
            (y-25.55,y+42.71394913),(center-31,center+31))
