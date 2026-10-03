"""Scope: Verify each 400 mm drawing fixing axis against its exact native member opening."""
from hettich_ka_4532_400_profile import HETTICH_KA_4532_400


class HettichKa4532FourHundredOpeningCheck:
    def verify(self, step_set):
        profile, openings = HETTICH_KA_4532_400, []
        for side in ("left", "right"):
            for pattern in profile.fixing_patterns:
                role = side+"-"+pattern.member
                solid = step_set.members[role]
                for depth, front, slot in zip(pattern.native_depth_axes_mm,
                        pattern.front_depth_axes_mm, pattern.slot_straight_lengths_mm, strict=True):
                    if abs(depth+profile.native_to_front_offset_mm-front) > 1e-6:
                        raise ValueError("400 mm native datum disagrees with its drawing axis")
                    volume = self.require_opening(solid, depth, pattern.diameter_mm, slot)
                    openings.append({"member": role, "native_depth_mm": depth,
                        "front_depth_mm": front, "diameter_mm": pattern.diameter_mm,
                        "slot_straight_length_mm": slot, "native_height_mm": 0,
                        "corridor_intersection_mm3": volume})
        return {"status": "PASS", "article": profile.article, "opening_count": len(openings),
            "native_to_front_offset_mm": profile.native_to_front_offset_mm,
            "native_front_installed_mm": profile.native_front_mm+profile.native_to_front_offset_mm,
            "openings": openings, "manufacturing_authority": False,
            "remaining": ["Selected screw articles and material-specific pilots", "Required hinge-clearance spacers and attachments",
                "Installed contact, full movement, loads and one-face drawer construction"]}

    def require_opening(self, solid, depth, diameter, slot):
        import cadquery as cq
        from OCP.BRepAdaptor import BRepAdaptor_Surface
        from OCP.GeomAbs import GeomAbs_Cylinder

        # Surface evidence prevents an empty corridor elsewhere from passing as a hole.
        expected_heights = (0,) if slot == 0 else (-slot/2, slot/2)
        found = set()
        for face in solid.Faces():
            surface = BRepAdaptor_Surface(face.wrapped)
            if surface.GetType() != GeomAbs_Cylinder:
                continue
            cylinder = surface.Cylinder()
            axis = cylinder.Axis()
            point = axis.Location()
            matches = (abs(abs(axis.Direction().X())-1) < 1e-6,
                       abs(cylinder.Radius()-diameter/2) < 1e-6, abs(point.Y()-depth) < 1e-6)
            if all(matches):
                found.update(height for height in expected_heights if abs(point.Z()-height) < 1e-6)
        if found != set(expected_heights):
            raise ValueError("9114274 opening lacks the drawing's cylindrical boundary")
        bounds = solid.BoundingBox()
        corridor = cq.Solid.makeCylinder(diameter/2, bounds.xlen+2,
            cq.Vector(bounds.xmin-1, depth, 0), cq.Vector(1, 0, 0))
        intersection = solid.intersect(corridor).Volume()
        if intersection > 1e-5:
            raise ValueError("9114274 member obstructs the drawing's fixing axis")
        return intersection
