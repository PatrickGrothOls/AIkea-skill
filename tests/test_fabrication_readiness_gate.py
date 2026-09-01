"""Scope: Verify readiness is blocked until the complete fabrication pack exists."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from types import SimpleNamespace

import cadquery as cq

from fabrication_readiness_gate import FabricationReadinessGate


class AssemblyTreeAssembly:
    """Match the generated walker's assembly visit contract."""


class AssemblyTreePart:
    """Match the generated walker's part visit contract."""


class TestFabricationReadinessGate:
    """Protect both refusal and successful completion of the full contract."""

    _PART_PATH = "wardrobe_01/left_side"

    def test_blocks_a_valid_tree_without_manufacturing_outputs(self, tmp_path) -> None:
        report = FabricationReadinessGate().evaluate(tmp_path, self._visits())

        failed = {check.code for check in report.checks if not check.passed}
        assert not report.is_ready
        assert "pack.part_step_and_drawings" in failed
        assert "pack.complete_bom" in failed
        assert "pack.complete_cut_list" in failed
        assert "pack.machining_declarations" in failed
        assert "validation.full_wardrobe_position" in failed
        assert "approval.current_closed_assembly" in failed

    def test_passes_only_with_complete_current_evidence(self, tmp_path) -> None:
        self._write_complete_pack(tmp_path)

        report = FabricationReadinessGate().evaluate(tmp_path, self._visits())

        assert report.is_ready
        assert report.as_dict()["status"] == "fabrication-ready"

    def _visits(self):
        built_part = SimpleNamespace(
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
        assembly = AssemblyTreeAssembly()
        assembly.path = ("wardrobe_01",)
        assembly.local_to_root = object()
        assembly.assembly = SimpleNamespace(
            parts=(built_part,),
            joints=(),
            cuts=(),
        )
        part = AssemblyTreePart()
        part.path = ("wardrobe_01", "part:left_side")
        part.local_to_root = object()
        part.part = built_part
        return assembly, part

    def _write_complete_pack(self, root: Path) -> None:
        parts = root / "manufacturing/parts"
        parts.mkdir(parents=True)
        slug = self._PART_PATH.replace("/", "__")
        built_part = self._visits()[1].part
        cq.exporters.export(built_part.solid, str(parts / f"{slug}.step"))
        cq.exporters.export(
            built_part.solid.faces(">Z"),
            str(parts / f"{slug}.dxf"),
        )
        self._json(
            root / "manufacturing/bom.json",
            {
                "schema_version": 1,
                "manufactured_parts": [
                    {
                        "path": self._PART_PATH,
                        "material": "plywood",
                        "thickness_mm": 18,
                        "quantity": 1,
                    }
                ],
                "purchased_hardware": [],
            },
        )
        (root / "manufacturing/cut-list.csv").write_text(
            "path,material,thickness_mm,quantity,blank_width_mm,blank_height_mm\n"
            f"{self._PART_PATH},plywood,18,1,500,2000\n",
            encoding="utf-8",
        )
        self._json(
            root / "manufacturing/machining.json",
            {
                "schema_version": 1,
                "parts": [{"path": self._PART_PATH, "operations": []}],
            },
        )
        self._json(
            root / "assemblies/full-wardrobe-position-check.json",
            {"status": "valid"},
        )
        model = root / "assemblies/full_wardrobe_review.glb"
        model.write_bytes(b"glb")
        self._json(
            root / "reviews/fabrication-assembly.json",
            {
                "review_type": "fabrication_assembly",
                "status": "approved",
                "artifact_sha256": sha256(model.read_bytes()).hexdigest(),
            },
        )

    def _json(self, path: Path, value: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")


__all__ = ["TestFabricationReadinessGate"]
