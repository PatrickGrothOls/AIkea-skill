"""Scope: Verify template-free panel construction and paired physical machining."""

from dataclasses import replace
import importlib
from math import prod

import pytest

from assembly_taxonomy_writer import AssemblyTaxonomyConflict
from furniture_design_project import FurnitureDesignProject
from generated_project_module_runtime import GeneratedProjectModuleRuntime
from local_to_parent_location import LocalToParentLocation
from part_construction_error import PartConstructionError


class TestPanelAssemblyDesign:
    """Exercise invented panel roles and geometry without a cabinet template."""

    @pytest.fixture
    def contracts(self, tmp_path):
        FurnitureDesignProject().initialize(tmp_path)
        return GeneratedProjectModuleRuntime().execute(tmp_path, self._load_contracts)

    def _load_contracts(self):
        return (
            importlib.import_module("assemblies.specification"),
            importlib.import_module("assemblies.panel_assembly"),
        )

    @pytest.mark.parametrize("role", ["side_panel", "reading_nook_seat"])
    def test_semantic_roles_do_not_add_drilling(self, contracts, role):
        values, panels = contracts
        part = values.PartSpec(
            "board", role, (), values.IDENTITY_LOCAL_TO_PARENT,
            local_size_mm=(600.0, 400.0, 18.0),
        )
        spec = panels.PanelAssemblySpec("nook_01", "reading_nook", (part,))
        built = panels.PanelAssemblyBuilder(spec).build()
        solid = built.parts[0].solid.val()

        assert solid.isValid()
        assert solid.Volume() == pytest.approx(prod(part.local_size_mm))
        assert len(solid.Faces()) == 6
        assert built.cuts == ()

    def test_cabineo_cuts_both_panels_at_one_shared_corner(self, contracts):
        values, panels = contracts
        spec = self._corner(contracts)
        built = panels.PanelAssemblyBuilder(spec).build()
        locations = LocalToParentLocation()
        blanks = tuple(panels.PanelBlankBuilder().build(p).val() for p in spec.parts)
        placed = tuple(
            blank.located(locations.build(part.local_to_parent))
            for blank, part in zip(blanks, spec.parts)
        )
        assert placed[0].distance(placed[1]) == pytest.approx(0, abs=1e-6)
        assert placed[0].intersect(placed[1]).Volume() == pytest.approx(0, abs=1e-6)
        for part, blank in zip(built.parts, blanks):
            assert part.solid.val().isValid()
            assert 0 < part.solid.val().Volume() < blank.Volume()
        source = [cut for cut in built.cuts if cut.part_id == "seat"]
        target = [cut for cut in built.cuts if cut.part_id == "support"]
        assert len(source) == len(target) == 2
        for left, right in zip(source, target):
            assert left.cutter is right.cutter
            world = tuple(
                cut.cutter.located(locations.build(part.local_to_parent) * cut.location)
                for cut, part in zip((left, right), spec.parts)
            )
            assert world[0].cut(world[1]).Volume() == pytest.approx(0, abs=1e-6)
            assert world[1].cut(world[0]).Volume() == pytest.approx(0, abs=1e-6)

    def test_rejects_disconnected_receiver(self, contracts):
        _, panels = contracts
        with pytest.raises(PartConstructionError, match="does not machine participant support"):
            panels.PanelAssemblyBuilder(self._corner(contracts, support_x=900)).build()

    def test_rejects_joint_without_a_machining_tool(self, contracts):
        values, panels = contracts
        spec = self._corner(contracts)
        unknown = values.JointSpec("seam", ("seat", "support"), "connection", "magic")
        with pytest.raises(PartConstructionError, match="no machining tool for joint type magic"):
            panels.PanelAssemblyBuilder(replace(spec, joints=(unknown,))).build()

    def test_initializer_preserves_local_package_and_conflicting_contract(self, tmp_path):
        package = tmp_path / "assemblies"
        package.mkdir()
        initializer = package / "__init__.py"
        initializer.write_text('"""User-owned assembly package."""\n')
        FurnitureDesignProject().initialize(tmp_path)
        assert initializer.read_text() == '"""User-owned assembly package."""\n'
        contract = package / "specification.py"
        contract.write_text('"""User-owned specification."""\n')
        with pytest.raises(AssemblyTaxonomyConflict):
            FurnitureDesignProject().initialize(tmp_path)
        assert contract.read_text() == '"""User-owned specification."""\n'

    def _corner(self, contracts, support_x=600.0):
        values, panels = contracts
        seat = values.PartSpec(
            "seat", "reading_nook_seat", (), values.IDENTITY_LOCAL_TO_PARENT,
            local_size_mm=(600.0, 400.0, 18.0), inside_face=">Z",
        )
        support = values.PartSpec(
            "support", "vertical_support", (),
            values.LocalToParentPlacement(
                values.Point3D(support_x, 0.0, 0.0),
                values.AxisBasis(
                    values.AxisDirection(0.0, 1.0, 0.0),
                    values.AxisDirection(0.0, 0.0, 1.0),
                    values.AxisDirection(1.0, 0.0, 0.0),
                ),
            ),
            local_size_mm=(400.0, 600.0, 18.0), inside_face="<Z",
        )
        joint = values.CabineoJointSpec(
            "corner", "seat", "support", ">Z", ">X", "bounded_spacing",
        )
        return panels.PanelAssemblySpec("nook_01", "reading_nook", (seat, support), (joint,))
