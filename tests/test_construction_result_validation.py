"""Scope: Detect plausible built trees with missing, forged or unapplied operations."""

from dataclasses import replace

import cadquery as cq
import pytest

from construction_result_validator import ConstructionResultValidator
from part_construction_error import PartConstructionError
from test_panel_assembly_design import TestPanelAssemblyDesign as PanelFixture


class TestConstructionResultValidation:
    contracts = PanelFixture.contracts
    _load_contracts = PanelFixture._load_contracts

    @pytest.fixture
    def corner(self, contracts):
        _, panels = contracts
        return panels.PanelAssemblyBuilder(PanelFixture()._corner(contracts)).build()

    def test_shared_builder_passes_independent_result_validation(self, corner):
        assert ConstructionResultValidator().validate(corner) == ()

    def test_raw_result_cannot_omit_a_declared_joint(self, corner):
        with pytest.raises(PartConstructionError, match="built joints differ"):
            ConstructionResultValidator().validate(replace(corner, joints=(), cuts=()))

    def test_raw_result_cannot_omit_one_receiver(self, corner):
        with pytest.raises(PartConstructionError, match="incomplete Cabineo occurrence"):
            ConstructionResultValidator().validate(replace(corner, cuts=corner.cuts[:-1]))

    def test_cut_metadata_without_subtraction_is_rejected(self, corner, contracts):
        _, panels = contracts
        plain = replace(corner.parts[0], solid=panels.PanelBlankBuilder().build(corner.parts[0].spec))
        with pytest.raises(PartConstructionError, match="machining is absent"):
            ConstructionResultValidator().validate(replace(corner, parts=(plain, corner.parts[1])))

    def test_plausible_smaller_hole_is_not_the_selected_connector(self, corner):
        tiny = cq.Workplane("XY").box(1, 1, 1).val()
        cuts = (replace(corner.cuts[0], cutter=tiny), *corner.cuts[1:])
        with pytest.raises(PartConstructionError, match="cutter differs"):
            ConstructionResultValidator().validate(replace(corner, cuts=cuts))

    def test_changed_dimensions_reject_stale_cut_geometry(self, corner):
        source = corner.spec.parts[0]
        changed = replace(source, local_size_mm=(600, 500, 18))
        spec = replace(corner.spec, parts=(changed, corner.spec.parts[1]))
        parts = (replace(corner.parts[0], spec=changed), corner.parts[1])
        with pytest.raises(PartConstructionError, match="cutter differs"):
            ConstructionResultValidator().validate(replace(corner, spec=spec, parts=parts))

    def test_local_request_requires_real_grid_and_correct_cut_identity(self, contracts):
        values, panels = contracts
        part = values.PartSpec("board", "custom", (), values.IDENTITY_LOCAL_TO_PARENT,
                               local_size_mm=(400, 700, 16), inside_face=">Z")
        request = values.PartMachiningSpec("grid", "board", "system_32")
        spec = panels.PanelAssemblySpec("unit_01", "custom", (part,), machining=(request,))
        built = panels.PanelAssemblyBuilder(spec).build()
        assert ConstructionResultValidator().validate(built) == ()
        with pytest.raises(PartConstructionError, match="cut occurrences differ"):
            ConstructionResultValidator().validate(replace(built, cuts=(replace(built.cuts[0], connector_index=9),)))

    def test_extra_feature_subtractions_preserve_previous_operation_evidence(self, corner):
        relieved = replace(corner.parts[0], solid=corner.parts[0].solid.cut(
            cq.Workplane("XY").box(10, 10, 5).translate((50, 50, 3))))
        assert ConstructionResultValidator().validate(replace(corner, parts=(relieved, corner.parts[1]))) == ()

    def test_raw_clipped_grid_cannot_bypass_shared_builder_rejection(self, contracts):
        from panel_machining_builder import PanelMachiningBuilder

        values, panels = contracts
        outline = tuple(values.BoundaryPoint(*point) for point in ((0, 0), (400, 0), (400, 110), (0, 700)))
        part = values.PartSpec("board", "custom", (), values.IDENTITY_LOCAL_TO_PARENT,
                               outline_mm=outline, local_size_mm=(400, 700, 16), inside_face=">Z")
        spec = panels.PanelAssemblySpec("unit_01", "custom", (part,),
                                       machining=(values.PartMachiningSpec("grid", "board", "system_32"),))
        cuts = PanelMachiningBuilder().build(spec).all
        solid = panels.PanelBlankBuilder().build(part).cut(cuts[0].cutter)
        raw = values.BuiltAssembly(spec, (values.BuiltPart(part, solid),), (), cuts)
        with pytest.raises(PartConstructionError, match="local machining is clipped"):
            ConstructionResultValidator().validate(raw)

    def test_two_requests_cannot_claim_the_same_removed_grid_material(self, contracts):
        from panel_machining_builder import PanelMachiningBuilder

        values, panels = contracts
        part = values.PartSpec("board", "custom", (), values.IDENTITY_LOCAL_TO_PARENT,
                               local_size_mm=(400, 700, 16), inside_face=">Z")
        requests = tuple(values.PartMachiningSpec(name, "board", "system_32") for name in ("first", "second"))
        spec = panels.PanelAssemblySpec("unit_01", "custom", (part,), machining=requests)
        cuts = PanelMachiningBuilder().build(spec).all
        solid = panels.PanelBlankBuilder().build(part).cut(cuts[0].cutter)
        raw = values.BuiltAssembly(spec, (values.BuiltPart(part, solid),), (), cuts)
        with pytest.raises(PartConstructionError, match="local machining is clipped"):
            ConstructionResultValidator().validate(raw)
