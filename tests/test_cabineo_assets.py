"""Scope: Lock the two proven Cabineo cutter assets to their verified bytes."""

from hashlib import sha256
from pathlib import Path

from cabineo_profile import NON_BOTTOM_CABINEO


class TestCabineoAssets:
    """Prevent silent drift in the canonical binary cutter geometry."""

    _ASSET_ROOT = (
        Path(__file__).parents[1]
        / "aikea-build-units"
        / "assets"
        / "cabineo"
    )
    _EXPECTED_SHA256 = {
        "cabineo_with_perimeter_cap.step": (
            "aa2d23692bf32a6611b9e6abd1deb48a62f9748d437a9df5cc9a1e175a9ead32"
        ),
        "Cabineo_8_connector_9dot1_19dot5.step": (
            "b9215669a277332047bbb7fadb15c35fa15d63433e78c5b438fd38033e396d61"
        ),
    }

    def test_packaged_assets_match_the_proven_sources(self) -> None:
        actual = {
            path.name: sha256(path.read_bytes()).hexdigest()
            for path in self._ASSET_ROOT.glob("*.step")
        }

        assert actual == self._EXPECTED_SHA256

    def test_non_bottom_profile_owns_its_fixed_construction_values(self) -> None:
        profile = NON_BOTTOM_CABINEO

        assert profile.profile_revision == 1
        assert profile.cutter_asset_filename in self._EXPECTED_SHA256
        assert profile.alignment_asset_filename in self._EXPECTED_SHA256
        assert profile.face_inset_mm == 9.5
        assert profile.pocket_depth_mm == 10.5
        assert profile.extra_floor_mm == 0.5
