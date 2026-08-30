"""Scope: Verify one review proposal covers every door without building later units."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from door_hinge_side import DoorHingeSide
from door_opening_run_resolver import DoorOpeningRunResolver
from door_opening_side_resolver import DoorOpeningSidePlan


@dataclass(frozen=True, slots=True)
class _Item:
    assembly_id: str


@dataclass(frozen=True, slots=True)
class _Run:
    assemblies: tuple[_Item, ...]


@dataclass(frozen=True, slots=True)
class _Spec:
    assembly_id: str
    parts: tuple["_Part", ...]


@dataclass(frozen=True, slots=True)
class _Part:
    part_id: str


class _SpecLoader:
    def __init__(self) -> None:
        self.loaded: list[str] = []

    def load(self, _project_root: Path, assembly_id: str) -> _Spec:
        self.loaded.append(assembly_id)
        parts = () if assembly_id == "bench_01" else (_Part("door_panel"),)
        return _Spec(assembly_id, parts)


class _SideResolver:
    def resolve(
        self,
        spec: _Spec,
        preferred_side: DoorHingeSide | None,
    ) -> DoorOpeningSidePlan:
        side = preferred_side or DoorHingeSide.LEFT
        return DoorOpeningSidePlan(
            spec.assembly_id,
            DoorHingeSide.LEFT,
            side,
            "resolved",
            "client_choice" if preferred_side else "standard",
        )


class TestDoorOpeningRunResolver(unittest.TestCase):
    def test_every_door_is_resolved_and_saved_as_local_metadata(self) -> None:
        resolver = DoorOpeningRunResolver()
        resolver.specs = _SpecLoader()
        resolver.side = _SideResolver()
        run = _Run(
            tuple(_Item(f"tall_storage_{index:02d}") for index in range(1, 4))
            + (_Item("bench_01"),)
        )
        project = {
            "design_settings": {
                "installation_boundaries": {
                    "left": True,
                    "right": True,
                    "top": True,
                },
                "door_openings": {"tall_storage_02": "right"},
            }
        }

        with TemporaryDirectory() as directory:
            root = Path(directory)
            result = resolver.resolve(root, project, run)
            result.write_local_plans(root)

            self.assertEqual(resolver.specs.loaded, [
                "tall_storage_01",
                "tall_storage_02",
                "tall_storage_03",
                "bench_01",
            ])
            self.assertEqual(len(result.plans), 3)
            self.assertTrue(result.has_doors)
            self.assertIs(
                result.for_assembly("tall_storage_01").proposed_side,
                DoorHingeSide.LEFT,
            )
            self.assertTrue(result.for_assembly("tall_storage_02").changes_default)
            self.assertTrue(
                (root / "assemblies/tall_storage_03/door_hinges/opening-plan.json").is_file()
            )
            self.assertFalse((root / "assemblies/bench_01/door_hinges").exists())

    def test_doorless_run_is_not_presented_as_an_opening_proof(self) -> None:
        resolver = DoorOpeningRunResolver()
        resolver.specs = _SpecLoader()
        resolver.side = _SideResolver()

        with TemporaryDirectory() as directory:
            result = resolver.resolve(
                Path(directory),
                {"design_settings": {}},
                _Run((_Item("bench_01"),)),
            )

        self.assertFalse(result.has_doors)
        self.assertIn("no fitted single doors", result.failure_reason)


if __name__ == "__main__":
    unittest.main()
