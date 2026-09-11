"""Scope: Verify exact declared hole reuse and rejection of partial or unowned overlaps."""

from dataclasses import asdict, replace
import importlib

import cadquery as cq
import pytest

from construction_result_validator import ConstructionResultValidator
from furniture_design_project import FurnitureDesignProject
from generated_project_module_runtime import GeneratedProjectModuleRuntime
from part_construction_error import PartConstructionError
from surface_drilling_source_renderer import SurfaceDrillingSourceRenderer
from surface_drilling_spec import SurfaceDrillingSpec
from surface_hole_pattern import SurfaceHole


class TestSurfaceDrillingReuse:
    @pytest.fixture
    def contracts(self, tmp_path):
        FurnitureDesignProject().initialize(tmp_path)
        return GeneratedProjectModuleRuntime().execute(tmp_path, self._contracts)

    def _contracts(self):
        return (importlib.import_module("assemblies.specification"),
                importlib.import_module("assemblies.panel_assembly"))

    def _spec(self, contracts):
        values, panels = contracts
        part = values.PartSpec("panel", "custom host", (), values.IDENTITY_LOCAL_TO_PARENT,
                               local_size_mm=(600, 600, 16), inside_face="<Z", material_id="mdf")
        grid = values.PartMachiningSpec("grid", "panel", "system_32")
        holes = tuple(SurfaceHole(f"fixing_{x}", x, 132, 5, 13) for x in (37, 128, 224, 352, 416))
        mounting = SurfaceDrillingSpec("mounting", "panel", values.IDENTITY_LOCAL_TO_PARENT, holes, ("grid",))
        return panels.PanelAssemblySpec("host_01", "custom parent", (part,), machining=(grid, mounting))

    def test_existing_grid_hole_is_reused_and_new_holes_match_independent_cylinders(self, contracts):
        _, panels = contracts
        spec = self._spec(contracts)
        base = panels.PanelAssemblyBuilder(replace(spec, machining=spec.machining[:1])).build()
        built = panels.PanelAssemblyBuilder(spec).build()
        expected = base.parts[0].solid.val()
        for x in (128, 224, 352, 416):
            expected = expected.cut(cq.Solid.makeCylinder(2.5, 13, cq.Vector(x, 132, 0)))
        actual = built.parts[0].solid.val()
        assert actual.cut(expected).Volume() + expected.cut(actual).Volume() == pytest.approx(0, abs=1e-5)
        assert len(built.cuts) == 2
        assert ConstructionResultValidator().validate(built) == ()

    def test_entire_pattern_can_reuse_existing_holes_without_double_removal(self, contracts):
        _, panels = contracts
        spec = self._spec(contracts)
        mounting = replace(spec.machining[1], holes=spec.machining[1].holes[:1])
        base = panels.PanelAssemblyBuilder(replace(spec, machining=spec.machining[:1])).build()
        built = panels.PanelAssemblyBuilder(replace(spec, machining=(spec.machining[0], mounting))).build()
        assert built.parts[0].solid.val().Volume() == pytest.approx(base.parts[0].solid.val().Volume())
        assert len(built.cuts) == 2
        assert ConstructionResultValidator().validate(built) == ()

    @pytest.mark.parametrize("references,message", [((), "clipped"), (("missing",), "earlier"),
                                                    (("mounting",), "earlier"), (("grid", "grid"), "invalid")])
    def test_reuse_must_name_a_unique_prior_operation(self, contracts, references, message):
        _, panels = contracts
        spec = self._spec(contracts)
        changed = replace(spec.machining[1], reuse_machining_ids=references)
        with pytest.raises(PartConstructionError, match=message):
            panels.PanelAssemblyBuilder(replace(spec, machining=(spec.machining[0], changed))).build()

    @pytest.mark.parametrize("x,diameter,depth", [(38, 5, 13), (37, 4, 13), (37, 6, 13), (37, 5, 12), (128, 5, 13)])
    def test_shifted_oversized_shallow_and_unused_holes_cannot_claim_reuse(self, contracts, x, diameter, depth):
        _, panels = contracts
        spec = self._spec(contracts)
        changed = replace(spec.machining[1], holes=(SurfaceHole("changed", x, 132, diameter, depth),))
        with pytest.raises(PartConstructionError, match="exactly matching"):
            panels.PanelAssemblyBuilder(replace(spec, machining=(spec.machining[0], changed))).build()

    def test_reuse_cannot_reference_another_panel(self, contracts):
        _, panels = contracts
        spec = self._spec(contracts)
        other = replace(spec.parts[0], part_id="other")
        grid = replace(spec.machining[0], part_id="other")
        with pytest.raises(PartConstructionError, match="same part"):
            panels.PanelAssemblyBuilder(replace(spec, parts=spec.parts+(other,), machining=(grid, spec.machining[1]))).build()

    def test_raw_builder_cannot_omit_reuse_declaration_or_dependency(self, contracts):
        _, panels = contracts
        spec = self._spec(contracts)
        built = panels.PanelAssemblyBuilder(spec).build()
        missing_reuse = replace(spec.machining[1], reuse_machining_ids=())
        with pytest.raises(PartConstructionError, match="clipped"):
            ConstructionResultValidator().validate(replace(built, spec=replace(spec, machining=(spec.machining[0], missing_reuse))))
        with pytest.raises(PartConstructionError, match="earlier"):
            ConstructionResultValidator().validate(replace(built, spec=replace(spec, machining=spec.machining[1:]), cuts=built.cuts[1:]))

    def test_one_reused_hole_does_not_allow_another_partial_collision(self, contracts):
        values, panels = contracts
        spec = self._spec(contracts)
        prior = SurfaceDrillingSpec("other_hole", "panel", values.IDENTITY_LOCAL_TO_PARENT,
                                    (SurfaceHole("offset", 129, 132, 5, 13),))
        changed = replace(spec, machining=(spec.machining[0], prior, spec.machining[1]))
        with pytest.raises(PartConstructionError, match="clipped"):
            panels.PanelAssemblyBuilder(changed).build()
        from panel_machining_builder import PanelMachiningBuilder
        cuts = PanelMachiningBuilder().build(changed).all
        solid = cq.Workplane("XY").box(600, 600, 16, centered=False)
        for cut in cuts:
            solid = solid.cut(cut.cutter.located(cut.location))
        raw = values.BuiltAssembly(changed, (values.BuiltPart(changed.parts[0], solid),), (), cuts)
        with pytest.raises(PartConstructionError, match="clipped"):
            ConstructionResultValidator().validate(raw)

    def test_editable_source_preserves_reuse_and_full_pattern(self, contracts):
        values, _ = contracts
        request = self._spec(contracts).machining[1]
        namespace = {name: getattr(values, name) for name in ("AxisDirection", "AxisBasis", "Point3D", "LocalToParentPlacement")}
        namespace.update(SurfaceDrillingSpec=SurfaceDrillingSpec, SurfaceHole=SurfaceHole)
        assert asdict(eval(SurfaceDrillingSourceRenderer().render(request), namespace)) == asdict(request)

    @pytest.mark.parametrize("new_x", [37, 38])
    def test_pattern_cannot_duplicate_or_enlarge_its_reused_hole(self, contracts, new_x):
        _, panels = contracts
        spec = self._spec(contracts)
        built = panels.PanelAssemblyBuilder(spec).build()
        mounting = replace(spec.machining[1], holes=(spec.machining[1].holes[0],
                           SurfaceHole("another_id", new_x, 132, 5, 13)))
        changed = replace(spec, machining=(spec.machining[0], mounting))
        with pytest.raises(ValueError, match="must not overlap"):
            panels.PanelAssemblyBuilder(changed).build()
        with pytest.raises(ValueError, match="must not overlap"):
            ConstructionResultValidator().validate(replace(built, spec=changed))
