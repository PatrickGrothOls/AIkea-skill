"""Scope: Verify the cabinet viewer supports close inspection of selected details."""

from pathlib import Path


class TestReviewViewerInteraction:
    """Protect the interaction required to inspect joints and machining closely."""

    def test_zoom_moves_straight_along_the_cabinet_rotation_axis(self) -> None:
        source = (
            Path(__file__).parents[1]
            / "aikea-review-unit/assets/viewer-source/src/CloseInspectionControls.jsx"
        ).read_text(encoding="utf-8")

        assert "raycaster.set(camera.position, zoomDirection)" in source
        assert "camera.position.addScaledVector(zoomDirection, travel)" in source
        assert "camera.position.addScaledVector(raycaster.ray.direction" not in source

    def test_close_zoom_uses_surface_distance_instead_of_target_distance(self) -> None:
        source = (
            Path(__file__).parents[1]
            / "aikea-review-unit/assets/viewer-source/src/CloseInspectionControls.jsx"
        ).read_text(encoding="utf-8")

        assert "CabinetSurfaceZoomTravel" in source
        assert "modelSpan" in source
        assert 'addEventListener("wheel"' in source
        assert "preventDefault" in source
        assert "stopImmediatePropagation" in source
        assert "camera.position.addScaledVector" in source

    def test_rotation_pivot_stays_at_the_cabinet_center_during_zoom(self) -> None:
        source = (
            Path(__file__).parents[1]
            / "aikea-review-unit/assets/viewer-source/src/CloseInspectionControls.jsx"
        ).read_text(encoding="utf-8")

        assert "controls.target.addScaledVector" not in source
        assert "enablePan={false}" in source

    def test_prebuilt_viewer_contains_the_close_zoom_controller(self) -> None:
        asset_root = (
            Path(__file__).parents[1]
            / "aikea-review-unit/assets/viewer/assets"
        )
        bundles = tuple(asset_root.glob("index-*.js"))
        assert len(bundles) == 1
        bundle = bundles[0].read_text(encoding="utf-8")

        assert "minimumTravel" in bundle
        assert "stopImmediatePropagation" in bundle
