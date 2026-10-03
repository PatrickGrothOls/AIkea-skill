"""Scope: Verify static review-file resolution stays inside the viewer bundle."""

from pathlib import Path

from review_file_resolver import ReviewFileResolver


class TestReviewFileResolver:
    """Keep local HTTP paths explicit and contained."""

    def test_resolves_viewer_root(self, tmp_path: Path) -> None:
        viewer = tmp_path / "viewer"
        viewer.mkdir()
        index = viewer / "index.html"
        index.write_text("viewer", encoding="utf-8")
        resolver = ReviewFileResolver(viewer)

        assert resolver.resolve("/") == index

    def test_resolves_bundled_assets(self, tmp_path: Path) -> None:
        viewer = tmp_path / "viewer"
        asset = viewer / "assets" / "viewer.js"
        asset.parent.mkdir(parents=True)
        asset.write_text("viewer", encoding="utf-8")
        resolver = ReviewFileResolver(viewer)

        assert resolver.resolve("/assets/viewer.js") == asset

    def test_does_not_resolve_files_outside_the_viewer(self, tmp_path: Path) -> None:
        viewer = tmp_path / "viewer"
        viewer.mkdir()
        model = tmp_path / "model.glb"
        model.write_bytes(b"mutable")
        resolver = ReviewFileResolver(viewer)

        assert resolver.resolve("/model.glb") is None

    def test_rejects_unknown_and_escaping_paths(self, tmp_path: Path) -> None:
        viewer = tmp_path / "viewer"
        viewer.mkdir()
        resolver = ReviewFileResolver(viewer)

        assert resolver.resolve("/missing.js") is None
        assert resolver.resolve("/../secret") is None
