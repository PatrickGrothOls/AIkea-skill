"""Scope: Apply declared cuts to a current part while verifying removed and reused material."""

from part_construction_error import PartConstructionError
from surface_drilling_reuse import SurfaceDrillingReuse


class PanelCutApplicator:
    def apply(self, part, solid, cuts, requests, preceding=()):
        if len(solid.vals()) != 1:
            raise PartConstructionError(f"{part.part_id}: return one Shape per Workplane; use a compound for multiple solids")
        previous = list(preceding)
        for cut in cuts:
            cutter = cut.cutter.located(cut.location)
            reuse = (SurfaceDrillingReuse().resolve(requests[cut.joint_id], previous, requests.keys())
                     if cut.joint_id in requests else None)
            reused_volume = reuse.Volume() if reuse is not None else 0
            removed = solid.val().intersect(cutter).Volume()
            if removed + reused_volume <= 1e-6:
                raise PartConstructionError(f"{cut.joint_id}: cutter does not machine participant {part.part_id}")
            if cut.joint_id in requests and abs(cutter.Volume() - removed - reused_volume) > 1e-5:
                raise PartConstructionError(f"{cut.joint_id}: local machining is clipped by the panel or earlier cuts")
            solid = solid.cut(cutter)
            previous.append(cut)
        if not solid.val().isValid() or solid.val().Volume() <= 1e-6:
            raise PartConstructionError(f"{part.part_id}: machining left no valid material")
        return solid
