"""Scope: Verify fabrication records contain exact physical values and paths."""

from __future__ import annotations

import json
from types import SimpleNamespace

from fabrication_pack_record_checker import FabricationPackRecordChecker
from fabrication_tree_evidence import (
    FabricationHardwareEvidence,
    FabricationPartEvidence,
    FabricationTreeEvidence,
)


class TestFabricationPackRecordChecker:
    """Reject plausible-looking records that disagree with the closed tree."""

    _PART_PATH = "wardrobe_01/side"
    _HARDWARE_PATH = "wardrobe_01/hinge"

    def test_accepts_exact_records(self, tmp_path) -> None:
        self._write_records(tmp_path)

        checks = FabricationPackRecordChecker().check(tmp_path, self._evidence())

        assert all(check.passed for check in checks)

    def test_rejects_wrong_bom_cut_and_machining_values(self, tmp_path) -> None:
        self._write_records(tmp_path)
        bom_path = tmp_path / "manufacturing/bom.json"
        bom = json.loads(bom_path.read_text(encoding="utf-8"))
        bom["manufactured_parts"][0]["quantity"] = 2
        bom_path.write_text(json.dumps(bom), encoding="utf-8")
        cut_path = tmp_path / "manufacturing/cut-list.csv"
        cut_path.write_text(
            "path,material,thickness_mm,quantity,blank_width_mm,blank_height_mm\n"
            f"{self._PART_PATH},birch-plywood,18,1,400,2000\n",
            encoding="utf-8",
        )
        machining_path = tmp_path / "manufacturing/machining.json"
        machining_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "parts": [{"path": self._PART_PATH, "operations": []}],
                }
            ),
            encoding="utf-8",
        )

        checks = FabricationPackRecordChecker().check(tmp_path, self._evidence())

        assert {check.code for check in checks if not check.passed} == {
            "pack.complete_bom",
            "pack.complete_cut_list",
            "pack.machining_declarations",
        }

    def test_rejects_duplicate_and_unexpected_bom_paths(self, tmp_path) -> None:
        self._write_records(tmp_path)
        path = tmp_path / "manufacturing/bom.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["manufactured_parts"] *= 2
        data["manufactured_parts"].append(
            {
                "path": "wardrobe_01/unexpected",
                "material": "birch-plywood",
                "thickness_mm": 18,
                "quantity": 1,
            }
        )
        path.write_text(json.dumps(data), encoding="utf-8")

        checks = FabricationPackRecordChecker().check(tmp_path, self._evidence())

        bom = next(check for check in checks if check.code == "pack.complete_bom")
        assert not bom.passed
        assert any("duplicate" in problem for problem in bom.problems)
        assert any("unexpected" in problem for problem in bom.problems)

    def _evidence(self) -> FabricationTreeEvidence:
        part = SimpleNamespace(
            spec=SimpleNamespace(local_size_mm=(500.0, 2000.0, 18.0))
        )
        hardware = SimpleNamespace(
            spec=SimpleNamespace(manufacturer="Riex", product_code="F000001")
        )
        return FabricationTreeEvidence(
            (FabricationPartEvidence(self._PART_PATH, part, ("side_joint",)),),
            (FabricationHardwareEvidence(self._HARDWARE_PATH, hardware),),
            (),
        )

    def _write_records(self, root) -> None:
        manufacturing = root / "manufacturing"
        manufacturing.mkdir()
        (manufacturing / "bom.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "manufactured_parts": [
                        {
                            "path": self._PART_PATH,
                            "material": "birch-plywood",
                            "thickness_mm": 18,
                            "quantity": 1,
                        }
                    ],
                    "purchased_hardware": [
                        {
                            "path": self._HARDWARE_PATH,
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
            f"{self._PART_PATH},birch-plywood,18,1,500,2000\n",
            encoding="utf-8",
        )
        (manufacturing / "machining.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "parts": [
                        {
                            "path": self._PART_PATH,
                            "operations": [{"joint_id": "side_joint"}],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )


__all__ = ["TestFabricationPackRecordChecker"]
