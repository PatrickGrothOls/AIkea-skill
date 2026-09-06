"""Scope: Protect exact KA 4532 and 13952 loading and native classification."""

from dataclasses import dataclass
from pathlib import Path

import hettich_ka_4532_spacer_step_set as step_set_module
from hettich_ka_4532_step_signature_test_support import (
    HettichKa4532StepSignatureTestSupport,
    NativeSolidTestDouble,
)
from hettich_ka_4532_spacer_step_set import HettichKa4532SpacerStepSetLoader


@dataclass(frozen=True, slots=True)
class NativeShapeTestDouble:
    """Return imported solids in deliberately non-classified order."""

    solids: tuple[NativeSolidTestDouble, ...]

    def Solids(self) -> tuple[NativeSolidTestDouble, ...]:
        return self.solids


@dataclass(frozen=True, slots=True)
class ImportedStepTestDouble:
    """Carry unchanged test geometry through the production loader."""

    shape: NativeShapeTestDouble


class ResolvedAssetTestDouble:
    """Record the exact manifest record admitted by the build-ready gate."""

    def __init__(self, record) -> None:
        self.record = record
        self.was_required_build_ready = False

    def require_build_ready(self) -> None:
        self.was_required_build_ready = True


class ResolverTestDouble:
    """Capture canonical product directories without reading vendor bytes."""

    roots: list[Path] = []
    resolved: list[ResolvedAssetTestDouble] = []

    def __init__(self, asset_root: Path) -> None:
        self.roots.append(asset_root)

    def resolve(self, record) -> ResolvedAssetTestDouble:
        asset = ResolvedAssetTestDouble(record)
        self.resolved.append(asset)
        return asset


class ImporterTestDouble:
    """Return recognizable shapes for the two exact registered assets."""

    imported_by_asset_id: dict[str, ImportedStepTestDouble] = {}

    def import_unchanged(self, asset) -> ImportedStepTestDouble:
        return self.imported_by_asset_id[asset.record.asset_id]


class TestHettichKa4532SpacerStepSetLoader:
    """Prove canonical loading, exact reuse, and native member classification."""

    _SIGNATURES = HettichKa4532StepSignatureTestSupport()

    def test_loads_and_classifies_the_exact_purchased_set(self, monkeypatch) -> None:
        solids = self._SIGNATURES.solids()
        fixed_left = solids["left-fixed"]
        moving_left = solids["left-moving"]
        moving_right = solids["right-moving"]
        fixed_right = solids["right-fixed"]
        spacer = solids["spacer"]
        runner_source = ImportedStepTestDouble(
            NativeShapeTestDouble(
                (moving_right, fixed_left, fixed_right, moving_left)
            )
        )
        spacer_source = ImportedStepTestDouble(NativeShapeTestDouble((spacer,)))
        ImporterTestDouble.imported_by_asset_id = {
            "hettich-ka-4532-500-runner-pair": runner_source,
            "hettich-13952-spacer-profile": spacer_source,
        }
        ResolverTestDouble.roots = []
        ResolverTestDouble.resolved = []
        monkeypatch.setattr(step_set_module, "HardwareAssetResolver", ResolverTestDouble)
        monkeypatch.setattr(step_set_module, "HardwareStepImporter", ImporterTestDouble)

        loaded = HettichKa4532SpacerStepSetLoader().load(Path("project/hardware"))

        assert ResolverTestDouble.roots == [
            Path("project/hardware/hettich/ka-4532-silent-system/9114276/source"),
            Path("project/hardware/hettich/ka-4532-spacer-profile/13952/source"),
        ]
        assert [asset.record.asset_id for asset in ResolverTestDouble.resolved] == [
            "hettich-ka-4532-500-runner-pair",
            "hettich-13952-spacer-profile",
        ]
        assert all(
            asset.was_required_build_ready
            for asset in ResolverTestDouble.resolved
        )
        assert loaded.runner_source is runner_source
        assert loaded.spacer_source is spacer_source
        assert loaded.runner_left.fixed_member is fixed_left
        assert loaded.runner_left.moving_member is moving_left
        assert loaded.runner_right.fixed_member is fixed_right
        assert loaded.runner_right.moving_member is moving_right
        assert loaded.spacer_solid is spacer
