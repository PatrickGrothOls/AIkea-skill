"""Scope: Verify GRASS provisional positioning and drilling independently of load/motion approval."""
from dataclasses import replace
from pathlib import Path
import tempfile
import unittest
from door_host_test_support import DoorHostTestSupport
from door_host import DoorHost
from grass_tiomos_155_profile import GRASS_TIOMOS_155
from grass_tiomos_155_plan import GrassTiomos155Planner
from grass_tiomos_155_machining import GrassTiomos155Machining
from hardware_placement import HardwarePlacement
from panel_hardware_reservation import PanelHardwareReservation
from system_32_side_panel_grid import System32SidePanelGrid


class TestGrassTiomos155Installation(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        old=DoorHostTestSupport().create(Path(self.temp.name),inset=0)
        p=old.door.local_to_parent
        door=replace(old.door,local_size_mm=(616.75,1000,18),
            local_to_parent=replace(p,origin_in_parent=replace(p.origin_in_parent,x_mm=103)))
        spec=replace(old.assembly,parts=(old.support,door))
        self.host=DoorHost(spec,old.spec,old.hinge_side)

    def test_provisional_width_keeps_unresolved_motion_and_load(self):
        plan=GrassTiomos155Planner().plan(self.host,3,9)
        self.assertEqual(plan.door_width_mm,616.75)
        self.assertFalse(plan.fabrication_ready)
        self.assertTrue(any('motion' in issue for issue in plan.compatibility_issues))

    def test_source_cup_plane_and_overlay_match_host(self):
        origin=GRASS_TIOMOS_155.source_origin(self.host,500)
        self.assertAlmostEqual(origin[0]+5.5,self.host.door_edge_x_mm+23.5)
        self.assertAlmostEqual(origin[1]-38.5,self.host.front_mm)
        self.assertAlmostEqual(origin[0]-3,self.host.inside_x_mm)

    def test_four_wood_pilots_do_not_consume_existing_five_mm_grid_holes(self):
        plan=GrassTiomos155Planner().plan(self.host,3,9)
        requests=GrassTiomos155Machining().build(self.host,plan)
        grid=System32SidePanelGrid()
        nodes=tuple((x,y) for x in grid.column_positions_mm(582) for y in grid.row_heights_mm(1000))
        for request in requests:
            if not request.machining_id.endswith('_grass_plate'):
                continue
            self.assertEqual(len(request.holes),4)
            placement=request.surface_to_part
            origin=placement.origin_in_parent;basis=placement.axis_basis
            frame=HardwarePlacement((origin.x_mm,origin.y_mm,origin.z_mm),
                *((a.x,a.y,a.z) for a in (basis.local_x_in_parent,basis.local_y_in_parent,basis.local_z_in_parent)))
            for hole in request.holes:
                x,y,z=frame.to_owner((hole.x_mm,hole.y_mm,0))
                self.assertGreater(min(((x-a)**2+(y-b)**2)**.5 for a,b in nodes),3.75)
                self.assertEqual(hole.depth_mm,12)

    def test_reservations_move_the_whole_hinge_without_moving_drawers(self):
        blocked=(PanelHardwareReservation('drawer','runner','post',(),(0,582),(0,180)),)
        plan=GrassTiomos155Planner().plan(self.host,3,9,blocked)
        self.assertGreaterEqual(min(p.cabinet_height_mm for p in plan.placements)-31,180)

    def test_wrong_overlay_is_not_treated_as_width_qualification(self):
        p=self.host.door.local_to_parent
        door=replace(self.host.door,local_to_parent=replace(p,
            origin_in_parent=replace(p.origin_in_parent,x_mm=101)))
        host=DoorHost(replace(self.host.assembly,parts=(self.host.support,door)),self.host.spec,self.host.hinge_side)
        with self.assertRaisesRegex(ValueError,'15 mm overlay'):
            GrassTiomos155Planner().plan(host,3,9)
