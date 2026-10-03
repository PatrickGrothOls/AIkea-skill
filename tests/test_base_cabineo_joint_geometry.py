"""Scope: Guard the intentional retirement of implicit base Cabineos and preserve actual mounting cuts."""
from math import pi
from importlib.util import find_spec
import unittest
from base_review_test_case import BaseReviewTestCase


@unittest.skipUnless(find_spec("cadquery"),"requires CadQuery")
class TestBaseCabineoJointGeometry(BaseReviewTestCase):
    def test_default_base_has_no_cabineo_brace_connections(self):
        built = self.generator.loader.load_assembly(self.project_root,"base_01")
        self.assertFalse(any(j.joint_type == "cabineo" for j in built.joints))
        self.assertFalse(any(p.spec.role in {"base_rail","base_brace"} for p in built.parts))
        mounting = [j for j in built.joints if j.joint_type == "korrekt_mounting"]
        self.assertEqual(len(mounting),16)
        self.assertTrue(all(j.plate_edge_clearance_mm >= 15-1e-6 for j in mounting))
        for part in built.parts:
            if part.spec.role != "base_deck":
                continue
            width,depth,thickness = part.spec.local_size_mm
            count = sum(c.part_id == part.spec.part_id for c in built.cuts)
            removed = width*depth*thickness-part.solid.val().Volume()
            self.assertAlmostEqual(removed,count*pi*(4*1.5**2+4**2)*thickness,places=4)
