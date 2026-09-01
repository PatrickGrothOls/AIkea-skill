"""Scope: Verify review adapters resolve by complete generated assembly lineage."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from assembly_review_feature_loader import AssemblyReviewFeatureLoader
from unit_mockup import UnitMockupInputError


class TestRecursiveReviewFeatureLoading:
    """Protect sibling cabinets and repeated child IDs from leaf-name ambiguity."""

    def test_resolves_a_cabinet_feature_beneath_the_wardrobe_root(
        self,
        tmp_path,
    ) -> None:
        self._feature_package(
            tmp_path,
            "assemblies/tall_storage_01",
            "cabinet",
        )

        reviews = AssemblyReviewFeatureLoader().load(
            tmp_path,
            ("wardrobe_01", "tall_storage_01"),
        )

        assert reviews[0].feature.marker == "cabinet"

    def test_resolves_repeated_drawer_ids_by_parent_lineage(self, tmp_path) -> None:
        self._feature_package(
            tmp_path,
            "assemblies/cabinet_01/children/drawer_01",
            "first",
        )
        self._feature_package(
            tmp_path,
            "assemblies/cabinet_02/children/drawer_01",
            "second",
        )

        first = AssemblyReviewFeatureLoader().load(
            tmp_path,
            ("wardrobe_01", "cabinet_01", "drawer_01"),
        )
        second = AssemblyReviewFeatureLoader().load(
            tmp_path,
            ("wardrobe_01", "cabinet_02", "drawer_01"),
        )

        assert first[0].feature.marker == "first"
        assert second[0].feature.marker == "second"

    def test_rejects_duplicate_packages_for_one_lineage(self, tmp_path) -> None:
        self._feature_package(
            tmp_path,
            "assemblies/cabinet_01/first/drawer_01",
            "first",
        )
        self._feature_package(
            tmp_path,
            "assemblies/cabinet_01/second/drawer_01",
            "second",
        )

        with pytest.raises(UnitMockupInputError, match="ambiguous"):
            AssemblyReviewFeatureLoader().load(
                tmp_path,
                ("wardrobe_01", "cabinet_01", "drawer_01"),
            )

    def test_returns_empty_when_the_owner_has_no_manifest(self, tmp_path) -> None:
        self._assembly_package(tmp_path, "assemblies/cabinet_01")

        assert AssemblyReviewFeatureLoader().load(
            tmp_path,
            ("wardrobe_01", "cabinet_01"),
        ) == ()

    def test_does_not_fall_back_to_a_shallow_leaf_manifest(self, tmp_path) -> None:
        self._feature_package(
            tmp_path,
            "assemblies/drawer_01",
            "unrelated",
        )
        self._assembly_package(
            tmp_path,
            "assemblies/cabinet_01/children/drawer_01",
        )

        assert AssemblyReviewFeatureLoader().load(
            tmp_path,
            ("wardrobe_01", "cabinet_01", "drawer_01"),
        ) == ()

    def _feature_package(self, root: Path, relative: str, marker: str) -> None:
        package = self._assembly_package(root, relative)
        (package / "review.py").write_text(
            f"class ProbeReview:\n    marker = {marker!r}\n\nREVIEW = ProbeReview()\n",
            encoding="utf-8",
        )
        (package / "features.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "features": [
                        {
                            "module": "probe.feature",
                            "order": 10,
                            "review_module": "review",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )

    def _assembly_package(self, root: Path, relative: str) -> Path:
        package = root / relative
        package.mkdir(parents=True, exist_ok=True)
        current = root
        for segment in Path(relative).parts:
            current /= segment
            (current / "__init__.py").write_text("", encoding="utf-8")
            if segment.startswith(("cabinet_", "drawer_", "tall_storage_")):
                (current / "spec.py").write_text("", encoding="utf-8")
        return package


__all__ = ["TestRecursiveReviewFeatureLoading"]
