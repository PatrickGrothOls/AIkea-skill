"""Scope: Build one authentic minimal fabrication pack for readiness tests."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from types import SimpleNamespace

import cadquery as cq

from fabrication_closed_assembly_model import FabricationClosedAssemblyModel
from fabrication_position_test_record import FabricationPositionTestRecord


class AssemblyTreeAssembly:
    """Match the generated walker's assembly visit contract."""


class AssemblyTreePart:
    """Match the generated walker's part visit contract."""


class FabricationReadinessTestProject:
    """Provide one real part export and complete structured evidence pack."""

    PART_PATH = "wardrobe_01/cabinet_01/left_side"

    def visits(self):
        built_part = SimpleNamespace(
            spec=SimpleNamespace(
                part_id="left_side",
                role="side_panel",
                local_size_mm=(500.0, 2000.0, 18.0),
                outline_mm=(),
                material_id="plywood",
            ),
            solid=cq.Workplane("XY").box(
                500.0,
                2000.0,
                18.0,
                centered=(False, False, False),
            ),
        )
        wardrobe = AssemblyTreeAssembly()
        wardrobe.path = ("wardrobe_01",)
        wardrobe.local_to_root = self._identity_placement()
        wardrobe.assembly = SimpleNamespace(
            spec=SimpleNamespace(assembly_id="wardrobe_01", purpose="wardrobe"),
            parts=(),
            joints=(),
            cuts=(),
        )
        cabinet = AssemblyTreeAssembly()
        cabinet.path = ("wardrobe_01", "cabinet_01")
        cabinet.local_to_root = self._identity_placement()
        cabinet.assembly = SimpleNamespace(
            spec=SimpleNamespace(assembly_id="cabinet_01", purpose="tall_storage"),
            parts=(built_part,),
            joints=(),
            cuts=(),
        )
        part = AssemblyTreePart()
        part.path = ("wardrobe_01", "cabinet_01", "part:left_side")
        part.local_to_root = self._identity_placement()
        part.part = built_part
        return wardrobe, cabinet, part

    def write_complete_pack(self, root: Path) -> None:
        parts = root / "manufacturing/parts"
        parts.mkdir(parents=True)
        slug = self.PART_PATH.replace("/", "__")
        visits = self.visits()
        built_part = visits[-1].part
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
            FabricationPositionTestRecord().build(
                visits,
                self.PART_PATH,
                "side_panel",
            ),
        )
        model = root / "assemblies/full_wardrobe_review.glb"
        FabricationClosedAssemblyModel().write(visits, model)
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

    def _identity_placement(self):
        axes = SimpleNamespace(
            local_x_in_parent=SimpleNamespace(x=1.0, y=0.0, z=0.0),
            local_y_in_parent=SimpleNamespace(x=0.0, y=1.0, z=0.0),
            local_z_in_parent=SimpleNamespace(x=0.0, y=0.0, z=1.0),
        )
        return SimpleNamespace(
            origin_in_parent=SimpleNamespace(x_mm=0.0, y_mm=0.0, z_mm=0.0),
            axis_basis=axes,
        )


__all__ = ["FabricationReadinessTestProject"]
