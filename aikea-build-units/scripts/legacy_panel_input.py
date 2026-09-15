"""Scope: Translate old per-part metadata and implicit grid intent into explicit shared inputs."""
from types import SimpleNamespace

from part_construction_error import PartConstructionError


class LegacyPanelInput:
    """Confine historical role conventions to the saved-project compatibility boundary."""

    def __init__(self, part):
        dimensions = dict(part.dimensions_mm)
        outline = tuple(part.outline_mm) if part.role in ("back_panel", "door_panel") else ()
        if part.role == "door_panel" and not outline:
            width, left, right = (float(dimensions[name]) for name in ("width", "left_height", "right_height"))
            outline = tuple(SimpleNamespace(x_mm=x, height_mm=y) for x,y in (
                (0,0), (width,0), (width,right), (0,left)))
        if outline:
            size = (max(p.x_mm for p in outline)-min(p.x_mm for p in outline),
                    max(p.height_mm for p in outline)-min(p.height_mm for p in outline),
                    float(dimensions["thickness"]))
        elif part.role in ("side_panel", "top_panel"):
            fields = (("depth", "height", "thickness") if part.role == "side_panel"
                      else ("length", "depth", "thickness"))
            size = tuple(float(dimensions[name]) for name in fields)
        elif part.role in ("shelf_panel", "base_deck", "base_rail", "base_brace", "base_kickboard"):
            size = part.local_size_mm
        else:
            raise PartConstructionError(f"unsupported legacy part role: {part.role}")
        self.panel = SimpleNamespace(part_id=getattr(part, "part_id", "legacy_panel"),
            role=part.role, local_size_mm=size, outline_mm=outline,
            inside_face=getattr(part, "inside_face", ""))
        self.machining = ((SimpleNamespace(machining_id="legacy_system_32", part_id=self.panel.part_id,
                          operation_type="system_32"),) if part.role == "side_panel" else ())

    def part(self, part_id):
        if part_id != self.panel.part_id:
            raise PartConstructionError(f"unknown legacy part: {part_id}")
        return self.panel
