"""Scope: Verify the cabinet viewer supports close inspection of selected details."""

from pathlib import Path


class TestReviewViewerInteraction:
    """Protect the interaction required to inspect joints and machining closely."""

    def test_zoom_moves_toward_the_pointed_cabinet_detail(self) -> None:
        controls_source = (
            Path(__file__).parents[1]
            / "aikea-review-unit/assets/viewer-source/src/FixedPivotCameraControls.js"
        ).read_text(encoding="utf-8")

        assert "raycaster.setFromCamera(pointer, this.camera)" in controls_source
        assert (
            "camera.position.addScaledVector(this.raycaster.ray.direction, travel)"
            in controls_source
        )

    def test_close_zoom_uses_surface_distance_instead_of_target_distance(self) -> None:
        binding_source = (
            Path(__file__).parents[1]
            / "aikea-review-unit/assets/viewer-source/src/CloseInspectionControls.jsx"
        ).read_text(encoding="utf-8")
        controls_source = (
            Path(__file__).parents[1]
            / "aikea-review-unit/assets/viewer-source/src/FixedPivotCameraControls.js"
        ).read_text(encoding="utf-8")
        viewer_source = (
            Path(__file__).parents[1]
            / "aikea-review-unit/assets/viewer-source/src/AssemblyReviewViewer.jsx"
        ).read_text(encoding="utf-8")

        assert "CabinetSurfaceZoomTravel" in controls_source
        assert "intersectObject(this.modelRoot, true)" in controls_source
        assert "modelRoot: scene" in viewer_source
        assert "scene.children" not in controls_source
        assert 'addEventListener("wheel"' in binding_source
        assert "preventDefault" in binding_source
        assert "stopImmediatePropagation" in binding_source

    def test_rotation_pivot_stays_at_the_cabinet_center_during_zoom(self) -> None:
        source = (
            Path(__file__).parents[1]
            / "aikea-review-unit/assets/viewer-source/src/FixedPivotCameraControls.js"
        ).read_text(encoding="utf-8")

        assert "this.rotationCenter.addScaledVector" not in source
        assert (
            "this.camera.position.copy(this.rotationCenter).add(this.orbitOffset)"
            in source
        )
        assert "this.camera.quaternion.premultiply(this.orbitRotation)" in source

    def test_shift_gestures_pan_the_camera_in_its_viewing_plane(self) -> None:
        binding_source = (
            Path(__file__).parents[1]
            / "aikea-review-unit/assets/viewer-source/src/CloseInspectionControls.jsx"
        ).read_text(encoding="utf-8")
        controls_source = (
            Path(__file__).parents[1]
            / "aikea-review-unit/assets/viewer-source/src/FixedPivotCameraControls.js"
        ).read_text(encoding="utf-8")

        assert "panCameraByPixels" in controls_source
        assert "if (event.shiftKey)" in binding_source
        assert "event.deltaX" in binding_source
        assert "-event.deltaY" in binding_source
        assert "panCameraByPixels(-deltaX, deltaY" in binding_source

    def test_photo_sampling_keeps_a_clean_interactive_preview(self) -> None:
        source = (
            Path(__file__).parents[1]
            / "aikea-review-unit/assets/viewer-source/src/AssemblyPhotoRenderer.jsx"
        ).read_text(encoding="utf-8")

        assert "dynamicLowRes={false}" in source
        assert "rasterizeScene" in source
        assert "renderDelay={350}" in source

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

    def test_prebuilt_viewer_preserves_review_only_source_materials(self) -> None:
        asset_root = (
            Path(__file__).parents[1]
            / "aikea-review-unit/assets/viewer/assets"
        )
        bundles = tuple(asset_root.glob("index-*.js"))
        assert len(bundles) == 1

        assert "review_only__" in bundles[0].read_text(encoding="utf-8")

    def test_prebuilt_viewer_contains_the_clean_photo_handoff(self) -> None:
        asset_root = (
            Path(__file__).parents[1]
            / "aikea-review-unit/assets/viewer/assets"
        )
        bundles = tuple(asset_root.glob("AssemblyPhotoRenderer-*.js"))
        assert len(bundles) == 1
        bundle = bundles[0].read_text(encoding="utf-8")

        assert "dynamicLowRes:!1" in bundle
        assert "rasterizeScene:!0" in bundle
        assert "renderDelay:350" in bundle

    def test_door_review_ends_with_two_concrete_client_actions(self) -> None:
        source = (
            Path(__file__).parents[1]
            / "aikea-review-unit/assets/viewer-source/src/DoorOpeningApprovalPanel.jsx"
        ).read_text(encoding="utf-8")

        assert "Approve door openings" in source
        assert "Change a door" in source
        assert "ready={modelBounds.modelRoot !== null}" in (
            Path(__file__).parents[1]
            / "aikea-review-unit/assets/viewer-source/src/AssemblyReviewViewer.jsx"
        ).read_text(encoding="utf-8")
