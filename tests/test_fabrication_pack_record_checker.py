"""Scope: Verify fabrication records contain exact physical values and paths."""

from __future__ import annotations

import json

from fabrication_pack_record_checker import FabricationPackRecordChecker
from fabrication_pack_record_test_data import FabricationPackRecordTestData
from fabrication_tree_evidence import FabricationTreeEvidence


class TestFabricationPackRecordChecker:
    """Reject plausible-looking records that disagree with the closed tree."""

    data = FabricationPackRecordTestData()

    def test_accepts_exact_records(self, tmp_path) -> None:
        self.data.write(tmp_path)

        checks = FabricationPackRecordChecker().check(tmp_path, self.data.evidence())

        assert all(check.passed for check in checks)

    def test_rejects_wrong_bom_cut_and_machining_values(self, tmp_path) -> None:
        self.data.write(tmp_path)
        bom_path = tmp_path / "manufacturing/bom.json"
        bom = json.loads(bom_path.read_text(encoding="utf-8"))
        bom["manufactured_parts"][0]["quantity"] = 2
        bom_path.write_text(json.dumps(bom), encoding="utf-8")
        cut_path = tmp_path / "manufacturing/cut-list.csv"
        cut_path.write_text(
            "path,material,thickness_mm,quantity,blank_width_mm,blank_height_mm\n"
            f"{self.data.PART_PATH},birch-plywood,18,1,400,2000\n",
            encoding="utf-8",
        )
        machining_path = tmp_path / "manufacturing/machining.json"
        machining_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "parts": [{"path": self.data.PART_PATH, "operations": []}],
                }
            ),
            encoding="utf-8",
        )

        checks = FabricationPackRecordChecker().check(tmp_path, self.data.evidence())

        assert {check.code for check in checks if not check.passed} == {
            "pack.complete_bom",
            "pack.complete_cut_list",
            "pack.machining_declarations",
        }

    def test_rejects_duplicate_and_unexpected_bom_paths(self, tmp_path) -> None:
        self.data.write(tmp_path)
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

        checks = FabricationPackRecordChecker().check(tmp_path, self.data.evidence())

        bom = next(check for check in checks if check.code == "pack.complete_bom")
        assert not bom.passed
        assert any("duplicate" in problem for problem in bom.problems)
        assert any("unexpected" in problem for problem in bom.problems)

    def test_rejects_material_not_bound_to_the_part_spec(self, tmp_path) -> None:
        self.data.write(tmp_path)
        evidence = self.data.evidence(material_id="oak-veneered-board")

        checks = FabricationPackRecordChecker().check(tmp_path, evidence)

        assert {check.code for check in checks if not check.passed} == {
            "pack.complete_bom",
            "pack.complete_cut_list",
        }

    def test_rejects_parts_without_an_authoritative_material_id(self, tmp_path) -> None:
        self.data.write(tmp_path)

        checks = FabricationPackRecordChecker().check(
            tmp_path,
            self.data.evidence(material_id=None),
        )

        assert {check.code for check in checks if not check.passed} == {
            "pack.complete_bom",
            "pack.complete_cut_list",
        }

    def test_rejects_duplicate_paths_in_the_physical_tree(self, tmp_path) -> None:
        self.data.write(tmp_path)
        evidence = self.data.evidence()
        evidence = FabricationTreeEvidence(
            evidence.parts * 2,
            evidence.hardware,
            evidence.root_child_ids,
        )

        checks = FabricationPackRecordChecker().check(tmp_path, evidence)

        assert all(not check.passed for check in checks)
        assert all(
            any("duplicate tree path" in problem for problem in check.problems)
            for check in checks
        )


__all__ = ["TestFabricationPackRecordChecker"]
