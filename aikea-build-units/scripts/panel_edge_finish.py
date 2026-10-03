"""Scope: Describe secondary edge rounding and return its actual shared part cuts."""

from dataclasses import dataclass

import cadquery as cq

from part_cut import AssemblyCuts, PartCut


@dataclass(frozen=True)
class EdgeRound:
    """Select edges on the current shape, then apply a constant-radius roundover."""

    selector: str
    radius_mm: float


@dataclass(frozen=True)
class PanelEdgeFinishSpec:
    """An explicit secondary finishing operation, requiring separate qualification."""

    joint_id: str
    part_id: str
    rounds: tuple[EdgeRound, ...]
    joint_type: str = "secondary_edge_rounding"
    process: str = "secondary_router_finish"

    @property
    def participant_ids(self):
        return (self.part_id,)


class PanelEdgeFinishCutBuilder:
    """Use existing machined solids; never replace joinery with an uncut blank."""

    def __init__(self, parts):
        self.parts = {part.spec.part_id: part.solid for part in parts}

    def build(self, _spec, requests):
        cuts = []
        current = dict(self.parts)
        for request in requests:
            original = current[request.part_id]
            finished = original
            for rounding in request.rounds:
                finished = finished.edges(rounding.selector).fillet(rounding.radius_mm)
            removed = original.val().cut(finished.val())
            cuts.append(PartCut(request.joint_id, request.part_id, 1, removed, cq.Location()))
            current[request.part_id] = finished
        return AssemblyCuts(tuple(cuts))
