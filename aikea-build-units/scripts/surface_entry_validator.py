"""Scope: Require local machining openings to coincide with actual panel entry faces."""

import cadquery as cq

from panel_blank_builder import PanelBlankBuilder
from part_construction_error import PartConstructionError


class SurfaceEntryValidator:
    def require_on_surface(self, part, entries, location, operation_id):
        faces = cq.Compound.makeCompound(PanelBlankBuilder().build(part).val().Faces())
        for label, entry in entries:
            if entry.located(location).cut(faces).Area() > 1e-6:
                raise PartConstructionError(f"{operation_id}/{label}: machining must start on an entry face")
