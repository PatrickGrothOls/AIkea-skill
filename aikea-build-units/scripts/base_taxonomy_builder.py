"""Scope: Derive one segmented structural base from a resolved cabinet run."""

from __future__ import annotations

from assembly_taxonomy import BaseAssemblyTaxonomy
from base_brace_planner import BaseBracePlanner
from base_construction_profile import BaseConstructionProfile, SHEET_BASE_320
from base_joint_taxonomy import BaseJointTaxonomy
from base_module_planner import BaseModulePlanner
from base_part_taxonomy import BasePartTaxonomy
from cnc_work_area import CNC_2500_X_2000_8MM, CncWorkArea


class BaseTaxonomyBuilder:
    """Coordinate CNC-sized base modules, their parts, and connection ownership."""

    def __init__(
        self,
        work_area: CncWorkArea = CNC_2500_X_2000_8MM,
        construction: BaseConstructionProfile = SHEET_BASE_320,
    ) -> None:
        self.module_planner = BaseModulePlanner(work_area)
        self.brace_planner = BaseBracePlanner()
        self.part_taxonomy = BasePartTaxonomy()
        self.joint_taxonomy = BaseJointTaxonomy()
        self.construction = construction

    def build(
        self,
        cabinet_spans_mm: tuple[tuple[float, float], ...],
        depth_mm: float,
        height_mm: float,
        panel_thickness_mm: float,
        plinth_front: str,
        plinth_recess_mm: float,
    ) -> BaseAssemblyTaxonomy:
        support_height_mm = height_mm - panel_thickness_mm
        clear_depth_mm = depth_mm - plinth_recess_mm - (2.0 * panel_thickness_mm)
        if support_height_mm <= 0 or clear_depth_mm <= 0:
            raise ValueError("base height and depth must exceed their panel allowances")
        modules = self.module_planner.plan(cabinet_spans_mm, depth_mm)
        parts = []
        joints = []
        for module_index, module in enumerate(modules, start=1):
            brace_positions_mm = self.brace_planner.positions_mm(
                module.width_mm,
                panel_thickness_mm,
                self.construction.maximum_brace_spacing_mm,
            )
            parts.extend(
                self.part_taxonomy.build_module(
                    module_index,
                    module.width_mm,
                    depth_mm,
                    clear_depth_mm,
                    support_height_mm,
                    panel_thickness_mm,
                    brace_positions_mm,
                )
            )
            joints.extend(
                self.joint_taxonomy.build_module(
                    module_index,
                    len(brace_positions_mm),
                )
            )
        joints.extend(self.joint_taxonomy.build_module_seams(len(modules)))
        global_left_mm = cabinet_spans_mm[0][0]
        global_right_mm = cabinet_spans_mm[-1][1]
        return BaseAssemblyTaxonomy(
            assembly_id="base_01",
            purpose="structural_base",
            global_left_mm=global_left_mm,
            global_right_mm=global_right_mm,
            width_mm=global_right_mm - global_left_mm,
            depth_mm=depth_mm,
            height_mm=height_mm,
            plinth_front=plinth_front,
            plinth_recess_mm=plinth_recess_mm,
            modules=modules,
            parts=tuple(parts),
            joints=tuple(joints),
        )


__all__ = ["BaseTaxonomyBuilder"]
