"""Scope: Protect exact KA 4532 and 13952 recursive-review hydration."""

from pathlib import Path
from types import SimpleNamespace

import pytest

from hettich_ka_4532_spacer_geometry_provider import (
    HettichKa4532SpacerGeometryProvider,
)


class StepSetLoaderProbe:
    """Return one recognizable exact set while recording its hardware root."""

    def __init__(self, step_set) -> None:
        self.step_set = step_set
        self.hardware_roots: list[Path] = []

    def load(self, hardware_root: Path):
        self.hardware_roots.append(hardware_root)
        return self.step_set


class NativeShapeGeometryProvider(HettichKa4532SpacerGeometryProvider):
    """Expose the selected native solid without requiring CadQuery in tests."""

    def _workplane(self, shape):
        return shape

    def _compound_workplane(self, members):
        return members


class TestHettichKa4532SpacerGeometryProvider:
    """Verify asset routing never changes purchased source geometry."""

    @pytest.mark.parametrize(
        ("selector", "expected_name"),
        (
            ("left-fixed", "left-fixed-native"),
            ("left-moving", "left-moving-native"),
            ("right-fixed", "right-fixed-native"),
            ("right-moving", "right-moving-native"),
        ),
    )
    def test_selects_each_unchanged_runner_member(
        self,
        tmp_path,
        selector,
        expected_name,
    ) -> None:
        provider, loader = self._provider()
        spec = SimpleNamespace(
            hardware_asset_id="hettich-ka-4532-500-runner-pair",
            geometry_selector=selector,
        )

        resolved = provider.resolve(tmp_path, spec)

        assert resolved.name == expected_name
        assert loader.hardware_roots == [tmp_path / "hardware"]

    @pytest.mark.parametrize(
        ("selector", "expected_names"),
        (
            ("left", ("left-fixed-native", "left-moving-native")),
            ("right", ("right-fixed-native", "right-moving-native")),
        ),
    )
    def test_compounds_both_unchanged_members_for_one_purchased_hand(
        self,
        tmp_path,
        selector,
        expected_names,
    ) -> None:
        provider, _ = self._provider()
        spec = SimpleNamespace(
            hardware_asset_id="hettich-ka-4532-500-runner-pair",
            geometry_selector=selector,
        )

        members = provider.resolve(tmp_path, spec)

        assert tuple(member.name for member in members) == expected_names

    def test_both_placements_reuse_the_same_unchanged_spacer_solid(
        self,
        tmp_path,
    ) -> None:
        provider, loader = self._provider()
        left_placement = object()
        right_placement = object()
        left = SimpleNamespace(
            hardware_asset_id="hettich-13952-spacer-profile",
            geometry_selector=None,
            local_to_parent=left_placement,
        )
        right = SimpleNamespace(
            hardware_asset_id="hettich-13952-spacer-profile",
            geometry_selector=None,
            local_to_parent=right_placement,
        )

        left_solid = provider.resolve(tmp_path, left)
        right_solid = provider.resolve(tmp_path, right)

        assert left.local_to_parent is not right.local_to_parent
        assert left_solid is right_solid
        assert left_solid.name == "spacer-13952-native"
        assert loader.hardware_roots == [tmp_path / "hardware"]

    def test_rejects_runner_without_an_explicit_member_selector(
        self,
        tmp_path,
    ) -> None:
        provider, _ = self._provider()
        spec = SimpleNamespace(
            hardware_asset_id="hettich-ka-4532-500-runner-pair",
            geometry_selector=None,
        )

        with pytest.raises(ValueError, match="saved hand or member selector"):
            provider.resolve(tmp_path, spec)

    def _provider(self):
        step_set = SimpleNamespace(
            runner_left=SimpleNamespace(
                fixed_member=SimpleNamespace(name="left-fixed-native"),
                moving_member=SimpleNamespace(name="left-moving-native"),
            ),
            runner_right=SimpleNamespace(
                fixed_member=SimpleNamespace(name="right-fixed-native"),
                moving_member=SimpleNamespace(name="right-moving-native"),
            ),
            spacer_solid=SimpleNamespace(name="spacer-13952-native"),
        )
        loader = StepSetLoaderProbe(step_set)
        return NativeShapeGeometryProvider(loader), loader
