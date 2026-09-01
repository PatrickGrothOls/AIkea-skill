"""Scope: Verify fabrication feature scopes follow exact generated lineage."""

from __future__ import annotations

import json

from fabrication_feature_scope_resolver import FabricationFeatureScopeResolver


class TestFabricationFeatureScopeResolver:
    """Keep repeated local IDs bound to their physical parent path."""

    def test_resolves_repeated_nested_id_through_its_complete_lineage(
        self,
        tmp_path,
    ) -> None:
        manifest = self._manifest(tmp_path, "cabinet_02")
        assembly_paths = (
            "wardrobe_01/cabinet_01/drawer_01",
            "wardrobe_01/cabinet_02/drawer_01",
        )

        scopes = FabricationFeatureScopeResolver().resolve(
            tmp_path,
            manifest,
            assembly_paths,
        )

        assert scopes is not None
        assert scopes[0].expected_paths == (
            "wardrobe_01/cabinet_02/drawer_01/bottom",
        )

    def _manifest(self, root, cabinet_id: str):
        path = root / "assemblies/wardrobe_01/assemblies" / cabinet_id
        path = path / "assemblies/drawer_01"
        for spec_root in (
            root / "assemblies/wardrobe_01",
            root / "assemblies/wardrobe_01/assemblies" / cabinet_id,
            path,
        ):
            spec_root.mkdir(parents=True, exist_ok=True)
            (spec_root / "spec.py").write_text("SPEC = None\n", encoding="utf-8")
        manifest = path / "features.json"
        manifest.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "features": [
                        {
                            "module": "drawer_bottom.feature",
                            "order": 10,
                            "affected_manufactured_part_paths": ["bottom"],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        return manifest


__all__ = ["TestFabricationFeatureScopeResolver"]
