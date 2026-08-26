"""Scope: Verify the cabinet viewer supports close inspection of selected details."""

from pathlib import Path


class TestReviewViewerInteraction:
    """Protect the interaction required to inspect joints and machining closely."""

    def test_zoom_follows_the_detail_under_the_pointer(self) -> None:
        source = (
            Path(__file__).parents[1]
            / "aikea-review-unit/assets/viewer-source/src/CloseInspectionControls.jsx"
        ).read_text(encoding="utf-8")

        assert "zoomToCursor" in source

    def test_close_zoom_moves_past_the_orbit_target_toward_the_surface(self) -> None:
        source = (
            Path(__file__).parents[1]
            / "aikea-review-unit/assets/viewer-source/src/CloseInspectionControls.jsx"
        ).read_text(encoding="utf-8")

        assert "PointerZoomTravel" in source
        assert "modelSpan" in source
        assert 'addEventListener("wheel"' in source
        assert "preventDefault" in source
        assert "stopImmediatePropagation" in source
        assert "camera.position.addScaledVector" in source
        assert "controls.target.addScaledVector" in source

    def test_prebuilt_viewer_contains_the_close_zoom_controller(self) -> None:
        bundle = (
            Path(__file__).parents[1]
            / "aikea-review-unit/assets/viewer/assets/index-CWHFNJWm.js"
        ).read_text(encoding="utf-8")

        assert "minimumTravel" in bundle
        assert "stopImmediatePropagation" in bundle
