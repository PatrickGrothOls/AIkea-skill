"""Scope: Resolve explicit local panel machining requests into traceable cutters."""

import cadquery as cq

from part_construction_error import PartConstructionError
from part_cut import AssemblyCuts, PartCut
from system_32_side_panel_grid import System32SidePanelGrid


class PanelMachiningBuilder:
    """Select operations by their request type, never the furniture or panel role."""

    def __init__(self):
        self.operations = {"system_32": self._system32}

    def build(self, spec):
        cuts = []
        for request in spec.machining:
            operation = self.operations.get(request.operation_type)
            if operation is None:
                raise PartConstructionError(
                    f"{request.machining_id}: no local machining tool for {request.operation_type}"
                )
            cutter = operation(spec.part(request.part_id))
            cuts.append(PartCut(request.machining_id, request.part_id, 1, cutter, cq.Location()))
        return AssemblyCuts(tuple(cuts))

    def _system32(self, part):
        depth, height, thickness = part.local_size_mm
        return System32SidePanelGrid().cutter(depth, height, thickness, part.inside_face)
