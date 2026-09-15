"""Scope: Preserve supplied room facts and explicit fresh arrangement assumptions."""
from dataclasses import dataclass


@dataclass(frozen=True)
class ViljaInputs:
    width: float = 2475
    depth: float = 450
    left_height: float = 2374
    right_height: float = 724
    flat_run: float = 990
    base_height: float = 95
    carcass_stock: float = 16
    door_stock: float = 18
    back_stock: float = 16
    deck_stock: float = 15
    cabinet_width: float = 598
    cabinet_pitch: float = 602
    first_x: float = 35.5
    door_overlay: float = 17
    top_fit: float = 5
    shelf_rows: tuple = ((324,708,1092,1476,1860), (324,708,1092,1476), (164,484,804), (164,))
    drawer_counts: tuple = (2,2,1,1)
    operating_gap: float = 3

    @property
    def opening_width(self):
        return self.cabinet_width-2*self.carcass_stock

    @property
    def drawer_box_width(self):
        return self.opening_width-2*25-2*12.7

    @property
    def drawer_front_width(self):
        return self.opening_width-2*2

    @property
    def door_width(self):
        return self.opening_width+2*self.door_overlay

    @property
    def door_x(self):
        return self.carcass_stock-self.door_overlay

    @property
    def drawer_heights(self):
        # Equal shallow boxes fill the space beneath a genuine System32 cap.
        return tuple(((rows[0]+2.5-self.carcass_stock-(count+1)*self.operating_gap)/count,)*count
            for rows,count in zip(self.shelf_rows,self.drawer_counts))

    @property
    def drawer_rows(self):
        return tuple(tuple(self.carcass_stock+self.operating_gap+n*(heights[0]+self.operating_gap)+35
            for n in range(len(heights))) for heights in self.drawer_heights)

    def ceiling(self, x):
        return self.left_height-max(0,x-self.flat_run)*(self.left_height-self.right_height)/(self.width-self.flat_run)

    def cabinet_x(self, index):
        return self.first_x+index*self.cabinet_pitch

    def top(self, index):
        x=self.cabinet_x(index)
        stations=[0,self.cabinet_width]
        if x < self.flat_run < x+self.cabinet_width:
            stations.insert(1,self.flat_run-x)
        return tuple((s,self.ceiling(x+s)-self.base_height-self.top_fit) for s in stations)


INPUTS=ViljaInputs()
