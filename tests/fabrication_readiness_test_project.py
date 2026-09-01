"""Scope: Build one authentic minimal fabrication pack for readiness tests."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from types import SimpleNamespace

import cadquery as cq

from cadquery_glb_exporter import CadQueryGlbExporter
from unit_mockup import MockupPart


class AssemblyTreeAssembly:
    """Match the generated walker's assembly visit contract."""


class AssemblyTreePart:
    """Match the generated walker's part visit contract."""


class FabricationReadinessTestProject:
    """Provide one real part export and complete structured evidence pack."""

    PART_PATH = "wardrobe_01/left_side"

    def visits(self):
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

    def write_complete_pack(self, root: Path) -> None:
        parts = root / "manufacturing/parts"
        parts.mkdir(parents=True)
        slug = self.PART_PATH.replace("/", "__")
        built_part = self.visits()[1].part
        cq.exporters.export(built_part.solid, str(parts / f"{slug}.step"))
        cq.exporters.export(built_part.solid.faces(">Z"), str(parts / f"{slug}.dxf"))
        self.write_json(
            root / "manufacturing/bom.json",
            {
                "schema_version": 1,
                "manufactured_parts": [
                    {
                        "path": self.PART_PATH,
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
            f"{self.PART_PATH},plywood,18,1,500,2000\n",
            encoding="utf-8",
        )
        self.write_json(
            root / "manufacturing/machining.json",
            {
                "schema_version": 1,
                "parts": [{"path": self.PART_PATH, "operations": []}],
            },
        )
        self.write_json(
            root / "assemblies/full-wardrobe-position-check.json",
            {
                "schema_version": 1,
                "status": "valid",
                "assemblies": {"wardrobe_01": {}},
                "relationships": {},
                "checks": [{"name": "probe position", "passed": True}],
            },
        )
        model = root / "assemblies/full_wardrobe_review.glb"
        CadQueryGlbExporter().export(
            "wardrobe_01",
            (
                MockupPart(
                    "left_side",
                    built_part.solid,
                    cq.Location(),
                    (0.8, 0.7, 0.6, 1.0),
                ),
            ),
            model,
        )
        self.write_json(
            root / "reviews/fabrication-assembly.json",
            {
                "review_type": "fabrication_assembly",
                "status": "approved",
                "artifact": "assemblies/full_wardrobe_review.glb",
                "artifact_sha256": sha256(model.read_bytes()).hexdigest(),
                "decision_artifact_sha256": sha256(model.read_bytes()).hexdigest(),
            },
        )

    def write_json(self, path: Path, value: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")


__all__ = ["FabricationReadinessTestProject"]
