"""Scope: Verify the local review server exposes only its viewer and chosen GLB."""

from pathlib import Path

from review_file_resolver import ReviewFileResolver


class TestReviewFileResolver:
    """Keep local HTTP paths explicit and contained."""

    def test_resolves_viewer_root_and_model(self, tmp_path: Path) -> None:
        viewer = tmp_path / "viewer"
        viewer.mkdir()
        index = viewer / "index.html"
        index.write_text("viewer", encoding="utf-8")
        model = tmp_path / "cabinet.glb"
        model.write_bytes(b"glb")
        resolver = ReviewFileResolver(viewer, model)

        assert resolver.resolve("/") == index
        assert resolver.resolve("/model.glb") == model

    def test_resolves_bundled_assets(self, tmp_path: Path) -> None:
        viewer = tmp_path / "viewer"
        asset = viewer / "assets" / "viewer.js"
        asset.parent.mkdir(parents=True)
        asset.write_text("viewer", encoding="utf-8")
        resolver = ReviewFileResolver(viewer, tmp_path / "cabinet.glb")

        assert resolver.resolve("/assets/viewer.js") == asset

    def test_rejects_unknown_and_escaping_paths(self, tmp_path: Path) -> None:
        viewer = tmp_path / "viewer"
        viewer.mkdir()
        resolver = ReviewFileResolver(viewer, tmp_path / "cabinet.glb")

        assert resolver.resolve("/missing.js") is None
        assert resolver.resolve("/../secret") is None
