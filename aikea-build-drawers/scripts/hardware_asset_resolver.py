"""Scope: Resolve and verify one user-supplied drawer-hardware STEP file."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from hardware_asset_manifest import HardwareAssetRecord, HardwareAssetState


class HardwareAssetError(ValueError):
    """Report a missing, changed, or incomplete local hardware asset."""


@dataclass(frozen=True, slots=True)
class ResolvedHardwareAsset:
    """Carry one checked local path and its immutable source identity."""

    record: HardwareAssetRecord
    path: Path
    sha256: str

    def require_build_ready(self) -> None:
        if self.record.state is not HardwareAssetState.READY:
            raise HardwareAssetError(
                f"{self.record.asset_id} is {self.record.state.value}, not build-ready"
            )


class HardwareAssetResolver:
    """Find hardware under one local root and verify known source bytes."""

    def __init__(self, asset_root: Path) -> None:
        self.asset_root = asset_root

    def resolve(
        self,
        record: HardwareAssetRecord,
        explicit_path: Path | None = None,
    ) -> ResolvedHardwareAsset:
        candidates = self._candidate_paths(record, explicit_path)
        existing = tuple(candidate for candidate in candidates if candidate.is_file())
        for path in existing:
            if path.suffix.lower() not in {".step", ".stp"}:
                continue
            actual_sha256 = sha256(path.read_bytes()).hexdigest()
            if record.expected_sha256 and actual_sha256 != record.expected_sha256:
                continue
            return ResolvedHardwareAsset(record, path, actual_sha256)
        if not existing:
            searched = ", ".join(str(candidate) for candidate in candidates)
            raise HardwareAssetError(
                f"local hardware STEP file is missing; searched: {searched}"
            )
        if all(path.suffix.lower() not in {".step", ".stp"} for path in existing):
            raise HardwareAssetError(f"hardware asset is not a STEP file: {existing[0]}")
        if record.expected_sha256:
            raise HardwareAssetError(
                f"hardware asset checksum does not match {record.asset_id}"
            )
        raise HardwareAssetError(f"hardware asset is not a STEP file: {existing[0]}")

    def _candidate_paths(
        self,
        record: HardwareAssetRecord,
        explicit_path: Path | None,
    ) -> tuple[Path, ...]:
        if explicit_path is not None:
            return (explicit_path.resolve(),)
        filenames = (record.local_filename, record.download_filename)
        return tuple(
            (self.asset_root / filename).resolve()
            for filename in filenames
            if filename
        )


__all__ = ["HardwareAssetError", "HardwareAssetResolver", "ResolvedHardwareAsset"]
