"""Scope: Verify Korrekt subtraction, rotated plate margins and split-deck ownership."""

from dataclasses import dataclass, replace
from math import pi

import cadquery as cq
import pytest

from assembly_composition_test_case import AssemblyCompositionTestCase
from korrekt_mounting_cutter import KorrektMountingCutter
from korrekt_mounting_machining import KorrektMountingMachining, KorrektMountingJoint
from panel_machining_feature import PanelMachiningFeature
from surface_hole_pattern import SurfaceHole
from surface_drilling_spec import SurfaceDrillingSpec
from part_cut import AssemblyCuts
from korrekt_plate_clearance import KorrektPlateClearance
from part_construction_error import PartConstructionError


@dataclass(frozen=True)
class DeckSpec:
    assembly_id: str
    parts: tuple
    purchased_hardware: tuple
    joints: tuple = ()
    child_assemblies: tuple = ()
    machining: tuple = ()
    requirements: tuple = ()

    def part(self, part_id):
        return next(part for part in self.parts if part.part_id == part_id)


class TestKorrektMountingGeometry(AssemblyCompositionTestCase):
    @pytest.mark.parametrize("thickness", [16, 18, 25])
    @pytest.mark.parametrize("rotation", [0, 90, 180])
    def test_five_complete_through_holes(self, generated_values, thickness, rotation):
        values, _ = generated_values
        built = self._deck(values, thickness, rotation)
        result = KorrektMountingMachining().apply(
            built, ("deck",), ("plate",), minimum_edge_margin_mm=10)
        solid = result.parts[0].solid.val()
        assert solid.isValid()
        assert 400 * 200 * thickness - solid.Volume() == pytest.approx(
            pi * (4 * 1.5**2 + 4**2) * thickness)
        bores = [face for face in solid.Faces() if face.geomType() == "CYLINDER"]
        assert len(bores) == 5
        assert all(face.BoundingBox().zlen == pytest.approx(thickness) for face in bores)
        cut = result.cuts[0]
        assert solid.intersect(cut.cutter.moved(cut.location)).Volume() < 1e-6
        assert result.joints[0].hardware_id == "plate"
        assert result.spec.purchased_hardware == built.spec.purchased_hardware

    def test_plate_overhang_fails_even_when_hole_centres_fit(self):
        cutter = KorrektMountingCutter()
        support = cq.Solid.makeBox(200, 200, 18)
        footprint = cutter.footprint().moved(cutter.placement((20, 100), 0, 0))
        with pytest.raises(PartConstructionError, match="footprint extends"):
            KorrektPlateClearance().check(support, footprint, 0)

    def test_margin_measures_the_offset_plate_not_the_leg_axis(self):
        cutter = KorrektMountingCutter()
        support = cq.Solid.makeBox(200, 200, 18)
        footprint = cutter.footprint().moved(cutter.placement((45, 100), 0, 0))
        checker = KorrektPlateClearance()
        assert checker.check(support, footprint, 0) == pytest.approx(5.49502)
        with pytest.raises(PartConstructionError, match="10 mm required"):
            checker.check(support, footprint, 10)

    def test_notched_panel_does_not_use_its_bounding_rectangle(self):
        cutter = KorrektMountingCutter()
        support = cq.Solid.makeBox(200, 200, 18).cut(
            cq.Solid.makeBox(40, 50, 18, cq.Vector(160, 75, 0)))
        footprint = cutter.footprint().moved(cutter.placement((120, 100), 0, 0))
        with pytest.raises(PartConstructionError, match="footprint extends"):
            KorrektPlateClearance().check(support, footprint, 0)

    def test_one_negative_crosses_both_half_lap_pieces(self, generated_values):
        values, _ = generated_values
        built = self._deck(values, 18, 0, split=True)
        result = KorrektMountingMachining().apply(
            built, ("left", "right"), ("plate",), minimum_edge_margin_mm=15)
        removed = sum(p.solid.val().Volume() for p in built.parts) - sum(
            p.solid.val().Volume() for p in result.parts)
        assert removed == pytest.approx(pi * (4 * 1.5**2 + 4**2) * 18)
        assert {cut.part_id for cut in result.cuts} == {"left", "right"}
        assert min(j.plate_edge_clearance_mm for j in result.joints) > 50
        with pytest.raises(PartConstructionError, match="already machined"):
            KorrektMountingMachining().apply(
                result, ("left", "right"), ("plate",), minimum_edge_margin_mm=15)

    def test_preserves_prior_hole_and_owned_child_and_hardware(self, generated_values):
        values, _ = generated_values
        built = self._deck(values, 18, 0)
        child_spec = values.CompositeAssemblySpec('service_01', 'service', ())
        child = values.BuiltAssembly(child_spec, (), ())
        child_ref = values.ChildAssemblySpec('service_01', 'service', values.IDENTITY_LOCAL_TO_PARENT)
        built = replace(built, spec=replace(built.spec, child_assemblies=(child_ref,)),
                        child_assemblies=(values.BuiltChildAssembly(child_ref, child),))
        frame = values.LocalToParentPlacement(values.Point3D(50, 50, 0), values.IDENTITY_AXIS_BASIS)
        hole = SurfaceDrillingSpec('service_hole', 'deck', frame, (SurfaceHole('access', 0, 0, 6, 18),))
        before = PanelMachiningFeature().apply(built, (hole,))
        result = KorrektMountingMachining().apply(before, ('deck',), ('plate',), minimum_edge_margin_mm=10)
        assert result.cuts[0] == before.cuts[0]
        assert result.spec.machining == before.spec.machining
        assert result.child_assemblies == before.child_assemblies
        assert result.purchased_hardware == before.purchased_hardware
        assert before.parts[0].solid.val().Volume()-result.parts[0].solid.val().Volume() == pytest.approx(pi*25*18)

    def test_unregistered_or_omitted_joint_cut_is_rejected(self, generated_values):
        values, _ = generated_values
        built = self._deck(values, 18, 0)
        joint = KorrektMountingJoint('mount', 'deck', 'plate', 60, 10)
        with pytest.raises(PartConstructionError, match='no machining tool'):
            PanelMachiningFeature().apply(built, joints=(joint,))
        with pytest.raises(PartConstructionError, match='account for every declared'):
            PanelMachiningFeature().apply(built, joints=(joint,), joint_builder=OmittedMountingCuts())

    def _deck(self, values, thickness, rotation, split=False):
        dimensions = (("left", 0, 210), ("right", 190, 210)) if split else (("deck", 0, 400),)
        parts = []
        for name, x, width in dimensions:
            placement = values.LocalToParentPlacement(values.Point3D(x, 0, 50),
                                                       values.IDENTITY_AXIS_BASIS)
            spec = values.PartSpec(name, "base_deck", (), placement,
                                   local_size_mm=(width, 200, thickness))
            solid = cq.Workplane("XY").box(width, 200, thickness, centered=(False, False, False))
            if split:
                origin = (190, 0, thickness / 2) if name == "left" else (0, 0, 0)
                solid = solid.cut(cq.Solid.makeBox(20, 200, thickness / 2, cq.Vector(*origin)))
            parts.append(values.BuiltPart(spec, solid))
        location = KorrektMountingCutter().placement((216, 100), 50, rotation)
        plane = cq.Plane.named("XY").rotated((0, 0, rotation))
        point = location.toTuple()[0]
        axes = values.AxisBasis(values.AxisDirection(*plane.xDir.toTuple()),
                                 values.AxisDirection(*plane.yDir.toTuple()), values.AxisDirection(0, 0, 1))
        hardware = values.PurchasedHardwareSpec("plate", "Hettich", "61854", "korrekt_61854",
            values.LocalToParentPlacement(values.Point3D(*point), axes))
        spec = DeckSpec("base", tuple(p.spec for p in parts), (hardware,))
        return values.BuiltAssembly(spec, tuple(parts), (), purchased_hardware=(
            values.BuiltPurchasedHardware(hardware, None),))


class OmittedMountingCuts:
    """Represent an extension that declares work but does not return its cut."""

    def build(self, assembly, joints):
        return AssemblyCuts(())
