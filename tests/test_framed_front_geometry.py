"""Scope: Prove distinct front parts, glue contact and assembly-independent placement."""

from dataclasses import replace
from math import pi
import pytest
from framed_front_test_support import FramedFrontTestSupport
from local_to_parent_location import LocalToParentLocation
from construction_result_validator import ConstructionResultValidator
from construction_requirement_checker import ConstructionRequirementChecker
from part_construction_error import PartConstructionError


class TestFramedFrontGeometry(FramedFrontTestSupport):
    @pytest.mark.parametrize("radius", [0, 4])
    @pytest.mark.parametrize("size,layers", [((420, 720), (9, 7)), ((680, 1600), (15, 5))])
    def test_frame_and_backing_have_exact_contact(self, contracts, radius, size, layers):
        _, builders, _, _, _ = contracts
        spec = self.front(contracts, width_mm=size[0], height_mm=size[1],
                          backing_thickness_mm=layers[0], frame_thickness_mm=layers[1],
                          opening_corner_radius_mm=radius)
        built = builders.FramedFrontBuilder(spec).build()
        assert [part.spec.part_id for part in built.parts] == ["backing", "frame"]
        placed = tuple(part.solid.val().located(LocalToParentLocation().build(
            part.spec.local_to_parent)) for part in built.parts)
        backing, frame = placed
        opening_width, opening_height = spec.opening_size_mm
        area = size[0]*size[1]-opening_width*opening_height+(4-pi)*radius**2
        assert all(s.isValid() and len(s.Solids()) == 1 for s in placed)
        assert frame.Volume() == pytest.approx(area*layers[1])
        assert backing.Volume() == pytest.approx(size[0]*size[1]*layers[0])
        assert backing.intersect(frame).Volume() == pytest.approx(0, abs=1e-6)
        top = next(face for face in backing.Faces() if face.normalAt().z > 0.99)
        underside = next(face for face in frame.Faces() if face.normalAt().z < -0.99)
        assert top.intersect(underside).Area() == pytest.approx(area)
        assert frame.BoundingBox().zmin == pytest.approx(layers[0])
        assert frame.BoundingBox().zmax == pytest.approx(sum(layers))
        assert built.joints == ()
        assert len(built.cuts) == 1
        assert built.spec.machining[0].operation_type == "surface_pocket"
        assert [part.spec.material_id for part in built.parts] == ["mdf-back", "mdf-frame"]
        assert ConstructionResultValidator().validate(built) == ()

    def test_nested_leaf_placement_moves_both_parts(self, contracts):
        _, builders, values, tree, _ = contracts
        front = self.front(contracts)
        placement = values.LocalToParentPlacement(values.Point3D(80, 100, 200),
            values.AxisBasis(values.AxisDirection(0, 0, 1),
                             values.AxisDirection(0, 1, 0),
                             values.AxisDirection(-1, 0, 0)))
        child = builders.FramedFrontBuilder(front).child(placement)
        parent = values.CompositeAssemblySpec("cabinet_01", "test enclosure", (child.spec,))
        built = values.BuiltAssembly(parent, (), (), child_assemblies=(child,))
        parts = [item for item in tree.AssemblyTreeWalker().walk(built)
                 if isinstance(item, tree.AssemblyTreePart)]
        boxes = [item.part.solid.val().located(LocalToParentLocation().build(
            item.local_to_root)).BoundingBox() for item in parts]
        assert len(parts) == 2
        assert (min(b.xmin for b in boxes), max(b.xmax for b in boxes)) == pytest.approx((64, 80))
        assert all((b.ymin, b.ymax, b.zmin, b.zmax) == pytest.approx((100, 820, 200, 620))
                   for b in boxes)

    def test_unframed_custom_outline_still_uses_ordinary_primitives(self, contracts):
        _, _, values, _, panels = contracts
        outline = tuple(values.BoundaryPoint(*p) for p in ((0, 0), (400, 0), (400, 500), (0, 700)))
        part = values.PartSpec("sloped_leaf", "custom_door", (), values.IDENTITY_LOCAL_TO_PARENT,
                               outline_mm=outline, local_size_mm=(400, 700, 20))
        built = panels.PanelAssemblyBuilder(panels.PanelAssemblySpec(
            "custom_door_01", "unframed sloped door", (part,))).build()
        assert len(built.parts) == 1 and not built.joints
        assert built.parts[0].solid.val().Volume() == pytest.approx(400*600*20)

    def test_recipe_is_editable_and_attachment_stays_unresolved(self, contracts):
        _, builders, _, tree, panels = contracts
        recipe = builders.FramedFrontBuilder(self.front(contracts)).recipe()
        opening = replace(recipe.machining[0], length_mm=280)
        altered = panels.PanelAssemblyBuilder(replace(recipe, machining=(opening,))).build()
        assert altered.spec.machining == (opening,)
        assert ConstructionResultValidator().validate(altered) == ()
        checks = ConstructionRequirementChecker().check(tree.AssemblyTreeWalker().walk(altered))
        assert any(not check.passed and any("unresolved" in problem for problem in check.problems)
                   for check in checks)
        assert {r.requirement_id for r in altered.spec.requirements if r.disposition == "unresolved"} == {
            "frame_attachment", "front_mounting"}
        invalid = replace(altered, spec=replace(altered.spec, machining=recipe.machining))
        with pytest.raises(PartConstructionError, match="cutter differs"):
            ConstructionResultValidator().validate(invalid)
