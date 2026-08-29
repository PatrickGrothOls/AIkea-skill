"""Scope: Store one exact purchased-hardware CAD download in an AIkea project."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
from zipfile import ZipFile


@dataclass(frozen=True, slots=True)
class HardwareCadSource:
    """Identify one official purchased component and its download source."""

    manufacturer: str
    product_family: str
    catalog_item: str
    product_url: str
    cad_page_url: str
    terms_url: str


@dataclass(frozen=True, slots=True)
class StoredHardwareCad:
    """Return the local source directory and its provenance record."""

    hardware_directory: Path
    source_record: Path
    cad_files: tuple[Path, ...]


class HardwareCadStore:
    """Copy and safely expand one vendor download without changing its bytes."""

    _CAD_SUFFIXES = {".step", ".stp"}
    _IGNORE_CONTENT = "# AIkea local purchased-hardware CAD\n*\n!.gitignore\n"

    def store(
        self,
        aikea_file: Path,
        download: Path,
        source: HardwareCadSource,
    ) -> StoredHardwareCad:
        self._require_file(aikea_file, "AIkea global specification")
        self._require_file(download, "hardware CAD download")
        hardware_root = aikea_file.resolve().parent / "hardware"
        product_root = (
            hardware_root
            / self._slug(source.manufacturer)
            / self._slug(source.product_family)
            / self._slug(source.catalog_item)
        )
        source_directory = product_root / "source"
        source_directory.mkdir(parents=True, exist_ok=True)
        self._protect_local_library(hardware_root)
        stored_download = self._copy_unchanged(download.resolve(), source_directory)
        extracted = self._extract_archive(stored_download, source_directory)
        stored_files = tuple(sorted({stored_download, *extracted}))
        cad_files = tuple(
            path for path in stored_files if path.suffix.lower() in self._CAD_SUFFIXES
        )
        if not cad_files:
            raise ValueError("the stored download contains no STEP file")
        source_record = product_root / "source-record.json"
        self._write_record(source_record, source, stored_download, stored_files)
        return StoredHardwareCad(source_directory, source_record, cad_files)

    def _protect_local_library(self, hardware_root: Path) -> None:
        ignore_file = hardware_root / ".gitignore"
        if ignore_file.exists() and ignore_file.read_text() != self._IGNORE_CONTENT:
            raise FileExistsError(f"local hardware ignore file differs: {ignore_file}")
        ignore_file.write_text(self._IGNORE_CONTENT, encoding="utf-8")

    def _copy_unchanged(self, source: Path, destination: Path) -> Path:
        target = destination / source.name
        if target.exists() and self._checksum(target) != self._checksum(source):
            raise FileExistsError(f"different source bytes already exist: {target}")
        if not target.exists():
            shutil.copy2(source, target)
        return target

    def _extract_archive(self, archive: Path, destination: Path) -> tuple[Path, ...]:
        if archive.suffix.lower() != ".zip":
            return ()
        extracted: list[Path] = []
        with ZipFile(archive) as bundle:
            for member in bundle.infolist():
                member_path = Path(member.filename)
                if member.is_dir():
                    continue
                if member_path.is_absolute() or ".." in member_path.parts:
                    raise ValueError(f"unsafe archive member: {member.filename}")
                target = destination / member_path.name
                contents = bundle.read(member)
                if target.exists() and target.read_bytes() != contents:
                    raise FileExistsError(f"different extracted bytes exist: {target}")
                if not target.exists():
                    target.write_bytes(contents)
                extracted.append(target)
        return tuple(extracted)

    def _write_record(
        self,
        output: Path,
        source: HardwareCadSource,
        original_download: Path,
        stored_files: tuple[Path, ...],
    ) -> None:
        record = {
            "schema_version": 1,
            "manufacturer": source.manufacturer,
            "product_family": source.product_family,
            "catalog_item": source.catalog_item,
            "product_url": source.product_url,
            "cad_page_url": source.cad_page_url,
            "terms_url": source.terms_url,
            "original_download": original_download.name,
            "stored_files": [
                {
                    "filename": path.name,
                    "sha256": self._checksum(path),
                    "size_bytes": path.stat().st_size,
                }
                for path in stored_files
            ],
        }
        output.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")

    def _slug(self, value: str) -> str:
        slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
        if not slug:
            raise ValueError("hardware identity cannot be empty")
        return slug

    def _checksum(self, path: Path) -> str:
        return sha256(path.read_bytes()).hexdigest()

    def _require_file(self, path: Path, description: str) -> None:
        if not path.is_file():
            raise FileNotFoundError(f"{description} does not exist: {path}")


__all__ = ["HardwareCadSource", "HardwareCadStore", "StoredHardwareCad"]
