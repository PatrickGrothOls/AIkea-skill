"""Scope: Record source-backed GRASS F028122660/F058139748 installation datums."""
from dataclasses import dataclass


@dataclass(frozen=True)
class GrassTiomos155Profile:
    profile_id: str = 'grass-tiomos-155-plus-f028122660-f058139748'
    relationship: str = 'full_overlay'
    supported_overlay_mm: float = 15
    cup_diameter_mm: float = 35
    cup_depth_mm: float = 11.5
    cup_center_from_edge_mm: float = 23.5
    cup_fixing_line_from_edge_mm: float = 33
    cup_fixing_spacing_mm: float = 45
    plate_height_mm: float = 3
    plate_reference_line_mm: float = 37
    rear_door_gap_mm: float = 1.5
    native_cup_back_y_mm: float = -38.5
    native_plate_back_x_mm: float = -3
    plate_bounds_mm: tuple = (-3,10.5,-25.55,39.95,-24,24)
    plate_fixing_offsets_mm: tuple = ((0,-16),(0,16),(-17,0),(15,0))
    reference_width_mm: float = 600
    minimum_door_thickness_mm: float = 16
    maximum_door_thickness_mm: float = 28
    source_pages: tuple = (518,519,580,594)

    def require_host(self, host):
        d=host.dimensions
        if host.hinge_side.value != 'left':
            raise ValueError('GRASS installation currently verifies the left-hand source frame only')
        if abs(host.overlay_mm-self.supported_overlay_mm)>1e-6:
            raise ValueError('GRASS source configuration requires 15 mm overlay')
        if not self.minimum_door_thickness_mm <= d['thickness'] <= self.maximum_door_thickness_mm:
            raise ValueError('door thickness outside sourced GRASS range')
        if abs(host.support_front_mm-host.front_mm-self.rear_door_gap_mm)>1e-6:
            raise ValueError('GRASS native pair requires its 1.5 mm rear-door gap and 37 mm plate line')
        if d['thickness'] > 25:
            raise ValueError('thicker door requires separate gap and restrictor configuration')

    def source_origin(self, host, height_mm):
        # Match both native datums simultaneously: cup plane at door rear,
        # mounting line37mm from carcass front. This requires1.5mm rear gap.
        # The catalogue's minimum lateral reveal is NOT a rear-door clearance.
        return (host.inside_x_mm-self.native_plate_back_x_mm,
                host.support_front_mm+self.plate_reference_line_mm,height_mm)


GRASS_TIOMOS_155=GrassTiomos155Profile()
