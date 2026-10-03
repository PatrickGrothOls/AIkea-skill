"""Scope: Adapt the standard configurator's measured space into the common geometry check."""

import cadquery as cq

from assembly_run import AssemblyRunReader
from assembly_run_overall_project_adapter import AssemblyRunOverallProjectAdapter
from overall_wardrobe_inputs import OverallWardrobeInputReader


class ConfiguredReviewEnvelope:
    """Use saved site measurements, including a sloped boundary, rather than built part bounds."""

    def build(self, project):
        run = AssemblyRunReader().read(project)
        inputs = OverallWardrobeInputReader().read(AssemblyRunOverallProjectAdapter().adapt(project, run))
        space = inputs.space
        allowances = inputs.settings.fitted_dimensions.resolve_fitting_allowances(inputs.settings.fit_allowance_mm)
        width = space.minimum_width_mm - allowances.width_mm
        positions = sorted({0.0, width, *(point.distance_from_left_mm for point in space.top_boundary.measurements
                                        if 0 < point.distance_from_left_mm < width)})
        outline = [(0, 0), (width, 0),
                   *((x, space.top_boundary.height_at(x)) for x in reversed(positions))]
        # The recipe root starts at the carcass front and left base edge; measurements include doors and wall clearance.
        return cq.Workplane("XZ").polyline(outline).close().extrude(-space.minimum_depth_mm).translate(
            (-inputs.settings.left_clearance_mm, -inputs.settings.door_thickness_mm, 0))
