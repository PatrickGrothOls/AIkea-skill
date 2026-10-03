"""Scope: Derive CNC-sized decks and kickboards for the default Korrekt cabinet base."""
from assembly_taxonomy import BaseAssemblyTaxonomy, JointTaxonomy, PartTaxonomy
from base_module_planner import BaseModulePlanner
from cnc_work_area import CNC_2500_X_2000_8MM
from korrekt_base_layout import KorrektBaseLayout


class BaseTaxonomyBuilder:
    """Floor-standing cabinet recipes never substitute a rail-and-brace support frame."""

    def __init__(self, work_area=CNC_2500_X_2000_8MM):
        self.module_planner = BaseModulePlanner(work_area)

    def build(self, cabinet_spans_mm, depth_mm, height_mm, panel_thickness_mm,
              plinth_front, plinth_recess_mm):
        layout = KorrektBaseLayout(height_mm, panel_thickness_mm)
        layout.check_adjustment_range()
        modules = self.module_planner.plan(cabinet_spans_mm, depth_mm)
        parts, joints = [], []
        for index, module in enumerate(modules, 1):
            for identity, role, depth in (("deck", "base_deck", depth_mm),
                                          ("kickboard", "base_kickboard", layout.support_height_mm)):
                parts.append(PartTaxonomy(f"{identity}_{index:02d}", role,
                    (("width", module.width_mm), ("depth", depth), ("thickness", panel_thickness_mm)),
                    local_size_mm=(module.width_mm, depth, panel_thickness_mm), inside_face=">Z"))
            joints.append(JointTaxonomy(f"kickboard_{index:02d}_attachment",
                (f"deck_{index:02d}", f"kickboard_{index:02d}"), "select_korrekt_kickboard_clips"))
        joints.extend(JointTaxonomy(f"base_module_{i:02d}_to_{i+1:02d}",
            (f"deck_{i:02d}", f"deck_{i+1:02d}"), "base_module_seam") for i in range(1,len(modules)))
        left, right = cabinet_spans_mm[0][0], cabinet_spans_mm[-1][1]
        return BaseAssemblyTaxonomy("base_01", "structural_base", left, right, right-left,
            depth_mm, height_mm, plinth_front, plinth_recess_mm, modules, tuple(parts), tuple(joints))
