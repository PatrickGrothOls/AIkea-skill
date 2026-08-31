"""Scope: Verify review adapters resolve at arbitrary generated tree depth."""

from __future__ import annotations

import json

from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader


class TestRecursiveReviewFeatureLoading:
    """Protect package discovery without encoding drawer or cabinet folders."""

    def test_loads_a_review_adapter_beneath_a_nested_assembly(self, tmp_path) -> None:
        package = tmp_path / "assemblies/cabinet_01/children/drawer_01"
        package.mkdir(parents=True)
        for parent in (
            tmp_path / "assemblies",
            tmp_path / "assemblies/cabinet_01",
            tmp_path / "assemblies/cabinet_01/children",
            package,
        ):
            (parent / "__init__.py").write_text("", encoding="utf-8")
        (package / "review.py").write_text(
            "class ProbeReview:\n    marker = 'nested'\n\nREVIEW = ProbeReview()\n",
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

        reviews = GeneratedAssemblyBuilderLoader().load_review_features(
            tmp_path,
            ("cabinet_01", "drawer_01"),
        )

        assert len(reviews) == 1
        assert reviews[0].feature_id == "probe"
        assert reviews[0].feature.marker == "nested"
