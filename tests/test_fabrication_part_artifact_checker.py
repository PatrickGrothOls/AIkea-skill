"""Scope: Verify fabrication exports match authoritative built part geometry."""

from __future__ import annotations

from types import SimpleNamespace

import cadquery as cq

from fabrication_part_artifact_checker import FabricationPartArtifactChecker
from fabrication_tree_evidence import FabricationPartEvidence


class TestFabricationPartArtifactChecker:
    """Refuse placeholder and stale CAD while accepting a real round trip."""

    _PATH = "wardrobe_01/left_side"

    def test_accepts_matching_step_and_dxf_geometry(self, tmp_path) -> None:
        evidence = self._evidence()
        self._write_matching_exports(tmp_path, evidence)

        check = FabricationPartArtifactChecker().check(tmp_path, (evidence,))

        assert check.passed

    def test_rejects_placeholder_part_exports(self, tmp_path) -> None:
        evidence = self._evidence()
        step_path, dxf_path = self._paths(tmp_path)
        step_path.parent.mkdir(parents=True)
        step_path.write_bytes(b"step")
        dxf_path.write_bytes(b"dxf")

        check = FabricationPartArtifactChecker().check(tmp_path, (evidence,))

        assert not check.passed
        assert len(check.problems) == 2

    def test_rejects_a_stale_step_with_different_geometry(self, tmp_path) -> None:
        evidence = self._evidence()
        self._write_matching_exports(tmp_path, evidence)
        step_path, _ = self._paths(tmp_path)
        cq.exporters.export(
            cq.Workplane("XY").box(400.0, 2000.0, 18.0, centered=False),
            str(step_path),
        )

        check = FabricationPartArtifactChecker().check(tmp_path, (evidence,))

        assert not check.passed
        assert "differs from built geometry" in check.problems[0]

    def test_rejects_a_same_bounds_dxf_with_the_wrong_outline(self, tmp_path) -> None:
        evidence = self._evidence()
        self._write_matching_exports(tmp_path, evidence)
        _step_path, dxf_path = self._paths(tmp_path)
        wrong = (
            cq.Workplane("XY")
            .polyline(((0.0, 0.0), (500.0, 0.0), (500.0, 2000.0)))
            .close()
            .extrude(1.0)
        )
        cq.exporters.export(wrong.faces(">Z"), str(dxf_path))

        check = FabricationPartArtifactChecker().check(tmp_path, (evidence,))

        assert not check.passed
        assert "DXF footprint differs" in check.problems[0]

    def test_rejects_a_dxf_with_an_unexpected_internal_hole(self, tmp_path) -> None:
        evidence = self._evidence()
        self._write_matching_exports(tmp_path, evidence)
        _step_path, dxf_path = self._paths(tmp_path)
        wrong = (
            cq.Workplane("XY")
            .box(500.0, 2000.0, 1.0, centered=(False, False, False))
            .faces(">Z")
            .workplane()
            .center(-250.0, -1000.0)
            .circle(25.0)
            .cutThruAll()
        )
        cq.exporters.export(wrong.faces(">Z"), str(dxf_path))

        check = FabricationPartArtifactChecker().check(tmp_path, (evidence,))

        assert not check.passed
        assert "DXF footprint differs" in check.problems[0]

    def _evidence(self) -> FabricationPartEvidence:
        part = SimpleNamespace(
            spec=SimpleNamespace(
                part_id="left_side",
                local_size_mm=(500.0, 2000.0, 18.0),
            ),
            solid=cq.Workplane("XY").box(
                500.0,
                2000.0,
                18.0,
                centered=(False, False, False),
            ),
        )
        return FabricationPartEvidence(self._PATH, part, ())

    def _write_matching_exports(self, root, evidence) -> None:
        step_path, dxf_path = self._paths(root)
        step_path.parent.mkdir(parents=True)
        cq.exporters.export(evidence.part.solid, str(step_path))
        cq.exporters.export(evidence.part.solid.faces(">Z"), str(dxf_path))

    def _paths(self, root):
        base = root / "manufacturing/parts" / self._PATH.replace("/", "__")
        return base.with_suffix(".step"), base.with_suffix(".dxf")


__all__ = ["TestFabricationPartArtifactChecker"]
