"""Scope: Verify explicit drilling through common construction on opposite and rotated surfaces."""

from dataclasses import replace
import importlib
from math import pi

import cadquery as cq
import pytest

from construction_result_validator import ConstructionResultValidator
from furniture_design_project import FurnitureDesignProject
from generated_project_module_runtime import GeneratedProjectModuleRuntime
from part_construction_error import PartConstructionError
from part_cut import PartCut
from surface_drilling_spec import SurfaceDrillingSpec
from surface_hole_pattern import SurfaceHole, SurfaceHolePattern


class TestSharedSurfaceDrilling:
    @pytest.fixture
    def contracts(self, tmp_path):
        FurnitureDesignProject().initialize(tmp_path)
        return GeneratedProjectModuleRuntime().execute(tmp_path, self._contracts)

    def _contracts(self):
        return (importlib.import_module("assemblies.specification"),
                importlib.import_module("assemblies.panel_assembly"))

    @pytest.mark.parametrize("top", [False, True])
    def test_exact_depth_from_either_surface_and_independent_output_check(self, contracts, top):
        values, panels = contracts
        surface = self._surface(values, top)
        holes = (SurfaceHole("fixing", 20, 30, 4, 8), SurfaceHole("locating", 60, 30, 6, 16))
        built = panels.PanelAssemblyBuilder(self._spec(values, panels, surface, holes)).build()
        expected = cq.Solid.makeBox(100, 100, 16)
        for x, y, radius, depth in ((20, 30, 2, 8), (60, 30, 3, 16)):
            start, direction = ((x, 100-y, 16), (0, 0, -1)) if top else ((x, y, 0), (0, 0, 1))
            expected = expected.cut(cq.Solid.makeCylinder(radius, depth, cq.Vector(*start), cq.Vector(*direction)))
        actual = built.parts[0].solid.val()
        assert actual.cut(expected).Volume() + expected.cut(actual).Volume() == pytest.approx(0, abs=1e-5)
        assert actual.Volume() == pytest.approx(160000-pi*(2**2*8+3**2*16))
        assert [(cut.joint_id, cut.part_id, cut.connector_index) for cut in built.cuts] == [("mounting", "panel", 1)]
        assert ConstructionResultValidator().validate(built) == ()

    def test_rotated_surface_retains_actual_cylinder_axis(self):
        plane = cq.Plane(origin=(100, 200, 300), xDir=(0, 1, 0), normal=(-1, 0, 0))
        actual = SurfaceHolePattern((SurfaceHole("axis", 10, 20, 8, 12),)).place(plane, 0)[0].cutter
        expected = cq.Solid.makeCylinder(4, 12, cq.Vector(100, 210, 280), cq.Vector(-1, 0, 0))
        assert actual.cut(expected).Volume() + expected.cut(actual).Volume() == pytest.approx(0, abs=1e-5)

    @pytest.mark.parametrize("hole,message", [(SurfaceHole("edge", 1, 20, 4, 8), "entry face"),
                                              (SurfaceHole("deep", 20, 20, 4, 17), "clipped")])
    def test_clipped_holes_are_rejected_by_shared_builder(self, contracts, hole, message):
        values, panels = contracts
        spec = self._spec(values, panels, self._surface(values), (hole,))
        with pytest.raises(PartConstructionError, match=message):
            panels.PanelAssemblyBuilder(spec).build()

    def test_buried_datum_fails_build_and_independent_raw_output_validation(self, contracts):
        values, panels = contracts
        surface = values.LocalToParentPlacement(values.Point3D(0, 0, 4), values.IDENTITY_AXIS_BASIS)
        spec = self._spec(values, panels, surface, (SurfaceHole("buried", 20, 30, 4, 8),))
        with pytest.raises(PartConstructionError, match="entry face"):
            panels.PanelAssemblyBuilder(spec).build()
        cutter = cq.Solid.makeCylinder(2, 8, cq.Vector(20, 30, 4))
        solid = cq.Workplane("XY").box(100, 100, 16, centered=False).cut(cutter)
        raw = values.BuiltAssembly(spec, (values.BuiltPart(spec.parts[0], solid),), (),
                                   (PartCut("mounting", "panel", 1, cutter, cq.Location()),))
        with pytest.raises(PartConstructionError, match="entry face"):
            ConstructionResultValidator().validate(raw)

    def test_edge_face_drilling_preserves_explicit_surface_axes(self, contracts):
        values, panels = contracts
        surface = values.LocalToParentPlacement(values.Point3D(0, 0, 0), values.AxisBasis(
            values.AxisDirection(0, 1, 0), values.AxisDirection(0, 0, 1), values.AxisDirection(1, 0, 0)))
        built = panels.PanelAssemblyBuilder(self._spec(values, panels, surface, (SurfaceHole("edge", 30, 8, 4, 12),))).build()
        expected = cq.Solid.makeBox(100, 100, 16).cut(cq.Solid.makeCylinder(2, 12, cq.Vector(0, 30, 8), cq.Vector(1, 0, 0)))
        actual = built.parts[0].solid.val()
        assert actual.cut(expected).Volume() + expected.cut(actual).Volume() == pytest.approx(0, abs=1e-5)
        assert ConstructionResultValidator().validate(built) == ()

    def test_cut_record_cannot_hide_absent_or_changed_drilling(self, contracts):
        values, panels = contracts
        spec = self._spec(values, panels, self._surface(values), (SurfaceHole("fixing", 20, 30, 4, 8),))
        built = panels.PanelAssemblyBuilder(spec).build()
        raw = replace(built, parts=(replace(built.parts[0], solid=cq.Workplane("XY").box(100, 100, 16, centered=False)),))
        with pytest.raises(PartConstructionError, match="machining is absent"):
            ConstructionResultValidator().validate(raw)
        changed = replace(spec.machining[0], holes=(SurfaceHole("fixing", 20, 30, 6, 8),))
        with pytest.raises(PartConstructionError, match="cutter differs"):
            ConstructionResultValidator().validate(replace(built, spec=replace(spec, machining=(changed,))))

    @pytest.mark.parametrize("holes", [(), (SurfaceHole("same", 20, 20, 4, 8), SurfaceHole("same", 50, 20, 4, 8))])
    def test_pattern_requires_nonempty_unique_hole_identities(self, holes):
        with pytest.raises(ValueError, match="distinct hole IDs"):
            SurfaceHolePattern(holes)

    @pytest.mark.parametrize("diameter,depth", [(0, 8), (4, -1), (float("nan"), 8)])
    def test_dimensioned_holes_reject_invalid_sizes(self, diameter, depth):
        with pytest.raises(ValueError, match="positive"):
            SurfaceHole("invalid", 20, 30, diameter, depth)

    def _spec(self, values, panels, surface, holes):
        part = values.PartSpec("panel", "custom mounting panel", (), values.IDENTITY_LOCAL_TO_PARENT,
                               local_size_mm=(100, 100, 16), material_id="mdf")
        request = SurfaceDrillingSpec("mounting", "panel", surface, holes)
        return panels.PanelAssemblySpec("mount_01", "custom mounting", (part,), machining=(request,))

    def _surface(self, values, top=False):
        if not top:
            return values.IDENTITY_LOCAL_TO_PARENT
        return values.LocalToParentPlacement(values.Point3D(0, 100, 16), values.AxisBasis(
            values.AxisDirection(1, 0, 0), values.AxisDirection(0, -1, 0), values.AxisDirection(0, 0, -1)))
