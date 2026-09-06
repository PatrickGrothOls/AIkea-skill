"""Scope: Verify local AIkea skill metadata, discovery links, and document links."""

from pathlib import Path
import re

import yaml


class SkillPackageVerifier:
    """Check that every checked-in skill can be discovered and read locally."""

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    def verify(self) -> None:
        entrypoints = sorted(self.root.glob("aikea*/SKILL.md"))
        self._require(bool(entrypoints), "No AIkea skill entrypoints found")
        for path in entrypoints:
            contents = path.read_text(encoding="utf-8")
            metadata = yaml.safe_load(contents.split("---", 2)[1])
            fields = {
                "name": metadata["name"] == path.parent.name,
                "description": isinstance(metadata["description"], str)
                and bool(metadata["description"].strip()),
            }
            for name, valid in fields.items():
                self._require(valid, f"{path}: invalid {name}")
            self._discovery_links(path)
            self._document_links(path, contents)
        print(f"Verified {len(entrypoints)} local AIkea skills and their links.")

    def _discovery_links(self, path: Path) -> None:
        for provider in (".agents", ".claude"):
            link = self.root / provider / "skills" / path.parent.name
            self._require(
                link.is_symlink() and link.resolve() == path.parent,
                f"{link}: missing or incorrect skill discovery link",
            )

    def _document_links(self, path: Path, contents: str) -> None:
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", contents):
            if "://" in target or target.startswith("#"):
                continue
            linked = (path.parent / target.split("#", 1)[0]).resolve()
            self._require(
                linked.is_relative_to(self.root) and linked.is_file(),
                f"{path}: unresolved local document link {target}",
            )

    def _require(self, valid: bool, message: str) -> None:
        if not valid:
            raise ValueError(message)


if __name__ == "__main__":
    SkillPackageVerifier(Path(__file__).resolve().parents[1]).verify()
