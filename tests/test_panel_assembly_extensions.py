"""Scope: Reject lost geometry or machining from injected panel construction tools."""

from dataclasses import replace
import importlib

import cadquery as cq
import pytest

from assembly_joint_machining_builder import AssemblyJointMachiningBuilder
from furniture_design_project import FurnitureDesignProject
from generated_project_module_runtime import GeneratedProjectModuleRuntime
from part_construction_error import PartConstructionError
from part_cut import AssemblyCuts
from test_panel_assembly_design import TestPanelAssemblyDesign as PanelDesignFixture


class SuppliedJointTool:
    """Return deliberately incomplete results at the custom machining boundary."""

    def __init__(self, cuts):
        self.cuts = cuts

    def build(self, _spec, _joints):
        return AssemblyCuts(self.cuts)


class SuppliedBlankTool:
    """Return authored multi-solid geometry without normalizing its Workplane."""

    def __init__(self, workplane):
        self.workplane = workplane

    def build(self, _part):
        return self.workplane


class TestPanelAssemblyExtensions:
    """Protect the generic extension boundary with actual cuts and solids."""

    @pytest.fixture
    def contracts(self, tmp_path):
        FurnitureDesignProject().initialize(tmp_path)
        return GeneratedProjectModuleRuntime().execute(tmp_path, self._load_contracts)

    def _load_contracts(self):
        return (
            importlib.import_module("assemblies.specification"),
            importlib.import_module("assemblies.panel_assembly"),
        )

    @pytest.mark.parametrize("defect", ["all_omitted", "receiver_omitted", "receiver_typo"])
    def test_rejects_missing_or_misspelled_custom_joint_participants(self, contracts, defect):
        _, panels = contracts
        spec = PanelDesignFixture()._corner(contracts)
        cuts = AssemblyJointMachiningBuilder(strict=True).build(spec, spec.joints).all
        bad_cuts = {
            "all_omitted": (),
            "receiver_omitted": tuple(cut for cut in cuts if cut.part_id == "seat"),
            "receiver_typo": tuple(
                replace(cut, part_id="suport") if cut.part_id == "support" else cut
                for cut in cuts
            ),
        }[defect]
        with pytest.raises(PartConstructionError, match="every declared joint participant"):
            panels.PanelAssemblyBuilder(spec, joint_builder=SuppliedJointTool(bad_cuts)).build()

    def test_rejects_duplicate_joint_identity_from_custom_tool(self, contracts):
        _, panels = contracts
        spec = PanelDesignFixture()._corner(contracts)
        cuts = AssemblyJointMachiningBuilder(strict=True).build(spec, spec.joints).all
        duplicated = replace(spec, joints=spec.joints * 2)
        with pytest.raises(PartConstructionError, match="joint IDs must be unique"):
            panels.PanelAssemblyBuilder(duplicated, joint_builder=SuppliedJointTool(cuts)).build()

    def test_rejects_one_missing_connector_even_when_both_panels_have_cuts(self, contracts):
        _, panels = contracts
        spec = PanelDesignFixture()._corner(contracts)
        cuts = AssemblyJointMachiningBuilder(strict=True).build(spec, spec.joints).all
        partial = tuple(cut for cut in cuts if not (cut.part_id == "support" and cut.connector_index == 2))
        with pytest.raises(PartConstructionError, match="incomplete Cabineo occurrence"):
            panels.PanelAssemblyBuilder(spec, joint_builder=SuppliedJointTool(partial)).build()

    def test_rejects_custom_blank_with_multiple_workplane_objects(self, contracts):
        _, panels = contracts
        spec = self._panel_spec(contracts)
        workplane = cq.Workplane("XY").newObject(self._separate_solids())
        with pytest.raises(PartConstructionError, match="return one Shape per Workplane"):
            panels.PanelAssemblyBuilder(spec, blank_builder=SuppliedBlankTool(workplane)).build()

    def test_preserves_every_solid_in_a_custom_compound_blank(self, contracts):
        _, panels = contracts
        spec = self._panel_spec(contracts)
        compound = cq.Compound.makeCompound(self._separate_solids())
        workplane = cq.Workplane("XY").newObject([compound])
        built = panels.PanelAssemblyBuilder(spec, blank_builder=SuppliedBlankTool(workplane)).build()
        actual = built.parts[0].solid.val()

        assert actual.isValid()
        assert len(actual.Solids()) == 2
        assert actual.Volume() == pytest.approx(2000.0)
        assert actual.BoundingBox().xmax == pytest.approx(30.0)

    def _panel_spec(self, contracts):
        values, panels = contracts
        part = values.PartSpec(
            "custom_board", "compound_component", (), values.IDENTITY_LOCAL_TO_PARENT,
            local_size_mm=(30.0, 10.0, 10.0),
        )
        return panels.PanelAssemblySpec("custom_01", "authored_component", (part,))

    def _separate_solids(self):
        return (
            cq.Solid.makeBox(10.0, 10.0, 10.0),
            cq.Solid.makeBox(10.0, 10.0, 10.0, cq.Vector(20.0, 0.0, 0.0)),
        )
