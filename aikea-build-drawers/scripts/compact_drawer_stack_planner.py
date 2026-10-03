"""Scope: Fill a floor-to-cap opening with proportioned drawers and operating gaps."""

from dataclasses import replace
from math import isfinite

from cabinet_drawer_plan import DrawerLayout


class CompactDrawerStackPlanner:
    """Resolve agent-proposed height proportions inside the actual shelf boundary."""

    def plan(self, layouts: tuple[DrawerLayout, ...], *, cap_underside_mm: float,
             gap_mm: float = 3.0,
             available_bottoms_mm: tuple[float, ...] | None = None) -> tuple[DrawerLayout, ...]:
        """Use heights as proportions; elevations are relative to the floor top.

        Caller supplies the actual cap underside after shelf-grid placement.
        Client-fixed heights belong in explicit layouts, not this sizing helper.
        """
        values = (cap_underside_mm, gap_mm, *(item.box_height_mm for item in layouts))
        if (not layouts or any(not isfinite(v) or v <= 0 for v in values)
                or gap_mm > 5 or len({item.drawer_id for item in layouts}) != len(layouts)):
            raise ValueError("require unique drawers, positive finite heights and a 0 < gap <= 5 mm")
        available = cap_underside_mm - gap_mm * (len(layouts) + 1)
        if available <= 0:
            raise ValueError("cap shelf leaves no drawer capacity after operating gaps")
        total = sum(item.box_height_mm for item in layouts)
        bottom = gap_mm
        bottoms = [bottom]
        proposed_heights = [available * layout.box_height_mm / total for layout in layouts]
        for index, height in enumerate(proposed_heights[:-1]):
            bottom += height + gap_mm
            if available_bottoms_mm is None:
                bottoms.append(bottom)
            else:
                candidates = [value for value in available_bottoms_mm
                              if bottoms[-1] + gap_mm < value < cap_underside_mm - gap_mm]
                remaining = len(layouts) - index - 2
                candidates = [value for value in candidates
                              if sum(later > value + gap_mm for later in candidates) >= remaining]
                if not candidates:
                    raise ValueError('no compatible mounting height remains within the stack')
                bottoms.append(min(candidates, key=lambda value: (abs(value-bottom), value)))
        boundaries = [*bottoms[1:], cap_underside_mm]
        planned = []
        for layout, bottom, upper in zip(layouts, bottoms, boundaries):
            height = upper - bottom - gap_mm
            planned.append(replace(layout, bottom_height_mm=bottom,
                                   box_height_mm=height, snap_to_system_32=False))
        return tuple(planned)
