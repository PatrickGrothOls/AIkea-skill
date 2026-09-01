"""Scope: Build exact BOM, cut-list, machining, and tree records for tests."""

from __future__ import annotations

import json
from types import SimpleNamespace

from fabrication_tree_evidence import (
    FabricationHardwareEvidence,
    FabricationPartEvidence,
    FabricationTreeEvidence,
)


class FabricationPackRecordTestData:
    """Keep complete record fixtures separate from behavioral assertions."""

    PART_PATH = "wardrobe_01/side"
    HARDWARE_PATH = "wardrobe_01/hinge"

    def evidence(self, material_id="birch-plywood") -> FabricationTreeEvidence:
        spec = {"local_size_mm": (500.0, 2000.0, 18.0)}
        if material_id is not None:
            spec["material_id"] = material_id
        part = SimpleNamespace(spec=SimpleNamespace(**spec))
        hardware = SimpleNamespace(
            spec=SimpleNamespace(manufacturer="Riex", product_code="F000001")
        )
        return FabricationTreeEvidence(
            (FabricationPartEvidence(self.PART_PATH, part, ("side_joint",)),),
            (FabricationHardwareEvidence(self.HARDWARE_PATH, hardware),),
            (),
        )

    def write(self, root) -> None:
        manufacturing = root / "manufacturing"
        manufacturing.mkdir()
        (manufacturing / "bom.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "manufactured_parts": [
                        {
                            "path": self.PART_PATH,
                            "material": "birch-plywood",
                            "thickness_mm": 18,
                            "quantity": 1,
                        }
                    ],
                    "purchased_hardware": [
                        {
                            "path": self.HARDWARE_PATH,
                            "manufacturer": "Riex",
                            "product_code": "F000001",
                            "quantity": 1,
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        (manufacturing / "cut-list.csv").write_text(
            "path,material,thickness_mm,quantity,blank_width_mm,blank_height_mm\n"
            f"{self.PART_PATH},birch-plywood,18,1,500,2000\n",
            encoding="utf-8",
        )
        (manufacturing / "machining.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "parts": [
                        {
                            "path": self.PART_PATH,
                            "operations": [{"joint_id": "side_joint"}],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )


__all__ = ["FabricationPackRecordTestData"]
