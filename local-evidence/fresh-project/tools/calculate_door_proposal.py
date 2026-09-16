"""Scope: Estimate intended full-width door masses without changing project geometry."""
from dataclasses import replace
from pathlib import Path
import json
import math
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from assemblies.vilja_inputs import INPUTS


class DoorProposalCalculator:
    density_kg_m3 = 750
    density_range_kg_m3 = (700, 800)
    finish_kg_m2_of_surface = 0.25

    def calculate(self):
        inputs = replace(INPUTS, cabinet_width=618.75, cabinet_pitch=618.75,
                         first_x=0, door_overlay=15)
        doors = []
        for index, count in enumerate((5, 5, 4, 3)):
            top = inputs.top(index)
            stations = ((0, inputs.ceiling(inputs.cabinet_x(index)+inputs.door_x)
                         -inputs.base_height-inputs.top_fit-2),
                        *((x-inputs.door_x, h-2) for x, h in top[1:-1]),
                        (inputs.door_width, inputs.ceiling(inputs.cabinet_x(index)
                         +inputs.door_x+inputs.door_width)-inputs.base_height-inputs.top_fit-2))
            outline = ((0, 0), (inputs.door_width, 0), *reversed(stations))
            edges = tuple(zip(outline, (*outline[1:], outline[0])))
            area = abs(sum(x1*y2-x2*y1 for (x1,y1),(x2,y2) in edges))/2/1e6
            integral = sum((x2-x1)*(y1+y2)/2 for (x1,y1),(x2,y2)
                           in zip(stations,stations[1:]))/1e6
            assert abs(area-integral) < 1e-12
            perimeter = sum(math.hypot(x2-x1,y2-y1) for (x1,y1),(x2,y2) in edges)/1000
            volume = area*inputs.door_stock/1000
            coated_area = 2*area+perimeter*inputs.door_stock/1000
            finish = coated_area*self.finish_kg_m2_of_surface
            doors.append(dict(door=index+1,width_mm=inputs.door_width,
                thickness_mm=inputs.door_stock,top_stations_mm=stations,
                area_m2=area,blank_volume_m3=volume,
                blank_mass_kg=volume*self.density_kg_m3,finish_allowance_kg=finish,
                estimated_panel_and_finish_kg=volume*self.density_kg_m3+finish,
                density_sensitivity_panel_and_finish_kg=[volume*d+finish for d in self.density_range_kg_m3],
                attached_moving_hardware_mass_kg=None,handle_mass_kg=None,
                proposed_hinge_count=count,hinge_centres_mm=None))
        return dict(status='provisional_mass_estimate_not_load_approval',
            unchanged_active_geometry=True,material='authored painted_mdf_18; single slab, no applied frame',
            assumptions=dict(density_kg_m3=self.density_kg_m3,density_range_kg_m3=self.density_range_kg_m3,
                finish_kg_m2_of_surface=self.finish_kg_m2_of_surface,
                finish_scope='both faces and all edges; unselected product assumption',
                machining='blank volume retained; no deduction for unfinalized drilling',
                hardware='moving hinge parts, screws and any handles not yet mass-qualified; not treated as zero'),
            hinge='GRASS F028122660 K3 with F058139748 3 mm plate',
            chart_reference_width_mm=600,width_difference_mm=16.75,width_difference_percent=16.75/600*100,
            hinge_count_basis='5/5/4/3 is a proposal matching EU reference height/weight regions; not wider-door qualification',
            hinges='left side; exact spacing remains unresolved against shelves, runners and panel fixings',
            source_chart='https://mediacenter.grass.eu/Katalog/EN/594/',doors=doors)


if __name__ == '__main__':
    result=DoorProposalCalculator().calculate()
    output=Path(__file__).resolve().parents[1]/'reviews/door-proposal-mass.json'
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
