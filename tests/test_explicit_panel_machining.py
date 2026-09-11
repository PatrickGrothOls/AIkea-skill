"""Scope: Verify explicit panel operations, rejection behavior, and inventory traceability."""

from dataclasses import replace
from math import pi

import pytest

from physical_item_counter import PhysicalItemCounter
from part_construction_error import PartConstructionError
from system_32_side_panel_grid import System32SidePanelGrid
from test_panel_assembly_design import TestPanelAssemblyDesign as PanelFixture


class TestExplicitPanelMachining:
    """Exercise the operation request at the construction boundary with real solids."""

    contracts = PanelFixture.contracts
    _load_contracts = PanelFixture._load_contracts

    def _spec(self, contracts):
        values, panels = contracts
        part = values.PartSpec(
            "board", "arbitrary", (), values.IDENTITY_LOCAL_TO_PARENT,
            local_size_mm=(400, 700, 16), inside_face=">Z", material_id="mdf",
        )
        request = panels.PartMachiningSpec("grid", "board", "system_32")
        return panels.PanelAssemblySpec("custom_01", "unregistered", (part,), machining=(request,))

    def test_explicit_grid_matches_existing_tool_and_keeps_cut_identity(self, contracts):
        values, panels = contracts
        spec = self._spec(contracts)
        plain = panels.PanelAssemblyBuilder(replace(spec, machining=())).build()
        built = panels.PanelAssemblyBuilder(spec).build()
        expected_holes = 2 * len(System32SidePanelGrid().row_heights_mm(700))
        difference = plain.parts[0].solid.val().Volume() - built.parts[0].solid.val().Volume()
        assert difference == pytest.approx(expected_holes * pi * 2.5**2 * 13)
        assert [(cut.joint_id, cut.part_id) for cut in built.cuts] == [("grid", "board")]
        from types import SimpleNamespace
        root = SimpleNamespace(path=("custom_01",), assembly=built)
        part = SimpleNamespace(path=("custom_01", "part:board"), part=built.parts[0])
        inventory = PhysicalItemCounter().count((root, part))
        assert inventory["totals"]["verified_cabineos"] == 0
        assert inventory["unresolved"] == []

    @pytest.mark.parametrize("defect", ["unknown", "target", "duplicate"])
    def test_rejects_unimplemented_or_invalid_requests(self, contracts, defect):
        _, panels = contracts
        spec = self._spec(contracts)
        requests = {
            "unknown": (panels.PartMachiningSpec("grid", "board", "magic"),),
            "target": (panels.PartMachiningSpec("grid", "missing", "system_32"),),
            "duplicate": spec.machining * 2,
        }
        with pytest.raises(PartConstructionError):
            panels.PanelAssemblyBuilder(replace(spec, machining=requests[defect])).build()

    @pytest.mark.parametrize("thickness,height,face", [(13, 700, ">Z"), (16, 100, ">Z"), (16, 700, "X")])
    def test_rejects_grid_that_cannot_fit(self, contracts, thickness, height, face):
        _, panels = contracts
        spec = self._spec(contracts)
        part = replace(spec.parts[0], local_size_mm=(400, height, thickness), inside_face=face)
        with pytest.raises(PartConstructionError):
            panels.PanelAssemblyBuilder(replace(spec, parts=(part,))).build()

    @pytest.mark.parametrize("value", [0, -1, float("nan"), float("inf")])
    def test_rejects_invalid_blank_dimensions(self, contracts, value):
        _, panels = contracts
        spec = self._spec(contracts)
        part = replace(spec.parts[0], local_size_mm=(value, 700, 16))
        with pytest.raises(PartConstructionError, match="positive finite"):
            panels.PanelAssemblyBuilder(replace(spec, parts=(part,), machining=())).build()

    @pytest.mark.parametrize("value", [float("nan"), float("inf"), -1])
    def test_grid_rejects_invalid_dimensions_before_iteration(self, value):
        with pytest.raises(PartConstructionError, match="positive finite"):
            System32SidePanelGrid().cutter(400, value, 16, ">Z")

    def test_rejects_grid_bores_clipped_by_a_slanted_outline(self, contracts):
        values, panels = contracts
        spec = self._spec(contracts)
        outline = tuple(values.BoundaryPoint(x, y) for x, y in ((0, 0), (400, 0), (400, 110), (0, 700)))
        part = replace(spec.parts[0], outline_mm=outline)
        with pytest.raises(PartConstructionError, match="local machining is clipped"):
            panels.PanelAssemblyBuilder(replace(spec, parts=(part,))).build()
