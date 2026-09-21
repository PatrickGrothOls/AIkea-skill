"""Scope: Fit a compact KA 5332 stack around the host's existing shelf-hole rows."""

from compact_drawer_stack_planner import CompactDrawerStackPlanner
from drawer_host import DrawerHost
from hettich_ka_5332_runner_catalog import HETTICH_KA_5332_RUNNER_CATALOG
from system_32_side_panel_grid import System32SidePanelGrid


class HettichKa5332CompactStackPlanner:
    """Reuse upper shelf rows without lifting the floor-adjacent first drawer."""

    def plan(self, cabinet, layouts, *, cap_underside_mm):
        host = DrawerHost.resolve(cabinet)
        runners = [HETTICH_KA_5332_RUNNER_CATALOG.select(item.box_depth_mm,
                   host.spec.inside_depth_mm) for item in layouts]
        offsets = {runner.runner_center_from_drawer_bottom_mm for runner in runners}
        if len(offsets) != 1:
            raise ValueError('compact stack requires one shared runner mounting datum')
        grid = System32SidePanelGrid()
        rows = [{round(host.frame(side).origin_mm[2] + row, 6)
                 for row in grid.row_heights_mm(host.part(side).local_size_mm[1])}
                for side in ('left', 'right')]
        offset = next(iter(offsets))
        bottoms = tuple(height - offset - host.spec.bottom_mm for height in sorted(rows[0] & rows[1]))
        return CompactDrawerStackPlanner().plan(layouts, cap_underside_mm=cap_underside_mm,
                                               available_bottoms_mm=bottoms)
