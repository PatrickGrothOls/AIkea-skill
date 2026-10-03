"""Scope: Check real edge-rounding volume and preservation of an existing bore."""

from math import pi
from types import SimpleNamespace as Value
import importlib

import cadquery as cq
import pytest

from panel_edge_finish import EdgeRound, PanelEdgeFinishSpec, PanelEdgeFinishCutBuilder
from furniture_design_project import FurnitureDesignProject
from generated_project_module_runtime import GeneratedProjectModuleRuntime
from panel_machining_feature import PanelMachiningFeature
from construction_result_validator import ConstructionResultValidator
from panel_setup_checker import PanelSetupChecker


class TestPanelEdgeFinish:
    def test_one_edge_roundover_matches_the_analytic_removed_volume(self):
        original = cq.Workplane("XY").box(100, 60, 18, centered=False)
        part = Value(spec=Value(part_id="front"), solid=original)
        request = PanelEdgeFinishSpec("soft_edge", "front", (EdgeRound("|X and >Z and <Y", 3),))
        cut, = PanelEdgeFinishCutBuilder((part,)).build(None, (request,)).all
        assert cut.cutter.Volume() == pytest.approx(100 * 3 ** 2 * (1 - pi / 4), abs=1e-5)
        assert request.process == "secondary_router_finish"
        assert request.participant_ids == ("front",)

    def test_existing_blind_bore_and_source_solid_survive_finishing(self):
        blank = cq.Workplane("XY").box(100, 60, 18, centered=False)
        bore = cq.Workplane("XY").center(50, 30).circle(4).extrude(10)
        original = blank.cut(bore)
        volume = original.val().Volume()
        part = Value(spec=Value(part_id="front"), solid=original)
        request = PanelEdgeFinishSpec("soft_edge", "front", (EdgeRound("|X and >Z and <Y", 3),))
        cut, = PanelEdgeFinishCutBuilder((part,)).build(None, (request,)).all
        finished = original.cut(cut.cutter)
        assert finished.val().isValid()
        assert finished.val().intersect(bore.val()).Volume() < 1e-6
        assert finished.val().Volume() == pytest.approx(volume - cut.cutter.Volume())
        assert original.val().Volume() == pytest.approx(volume)

    def test_shared_feature_keeps_the_finish_explicit_and_unqualified(self, tmp_path):
        FurnitureDesignProject().initialize(tmp_path)
        GeneratedProjectModuleRuntime().execute(tmp_path, self._check_shared_feature)

    def _check_shared_feature(self):
        values = importlib.import_module("assemblies.specification")
        panels = importlib.import_module("assemblies.panel_assembly")
        part = values.PartSpec("front", "front", (), values.IDENTITY_LOCAL_TO_PARENT,
                               local_size_mm=(100, 60, 18), material_id="prototype")
        built = panels.PanelAssemblyBuilder(panels.PanelAssemblySpec("unit_01", "test", (part,))).build()
        request = PanelEdgeFinishSpec("soft_edge", "front", (EdgeRound("|X and >Z and <Y", 3),))
        finished = PanelMachiningFeature().apply(
            built, joints=(request,), joint_builder=PanelEdgeFinishCutBuilder(built.parts),
        )
        assert finished.joints == (request,)
        assert len(finished.cuts) == 1
        assert ConstructionResultValidator().validate(finished) == (request,)
        assert PanelSetupChecker().check(finished)["status"] == "conflict_or_unsupported"
        assert finished.parts[0].solid.val().Volume() < built.parts[0].solid.val().Volume()
