"""Scope: Keep the old blank entry point as an adapter to common panel construction."""
from legacy_panel_input import LegacyPanelInput
from panel_blank_builder import PanelBlankBuilder
from part_construction_error import PartConstructionError


class PartBlankBuilder:
    def build(self, part):
        return PanelBlankBuilder().build(LegacyPanelInput(part).panel)


__all__ = ["PartBlankBuilder", "PartConstructionError"]
