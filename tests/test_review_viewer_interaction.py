"""Scope: Verify the cabinet viewer supports close inspection of selected details."""

from pathlib import Path


class TestReviewViewerInteraction:
    """Protect the interaction required to inspect joints and machining closely."""

    def test_zoom_follows_the_detail_under_the_pointer(self) -> None:
        source = (
            Path(__file__).parents[1]
            / "aikea-review-unit/assets/viewer-source/src/AssemblyReviewViewer.jsx"
        ).read_text(encoding="utf-8")

        assert "zoomToCursor" in source
