"""Scope: Adapt saved per-part builders to the shared blank, machining and subtraction tools."""
from legacy_panel_input import LegacyPanelInput
from panel_blank_builder import PanelBlankBuilder
from panel_cut_applicator import PanelCutApplicator
from panel_machining_builder import PanelMachiningBuilder


class SheetPartBuilder:
    """Retain old implicit-grid behavior only at this compatibility entry point."""

    def build(self, part, cuts):
        spec = LegacyPanelInput(part)
        blank = PanelBlankBuilder().build(spec.panel)
        local = PanelMachiningBuilder().build(spec).all
        requests = {request.machining_id: request for request in spec.machining}
        return PanelCutApplicator().apply(spec.panel, blank, local+tuple(cuts), requests)


__all__ = ["SheetPartBuilder"]
