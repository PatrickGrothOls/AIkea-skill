"""Scope: Build reproducible public AIkea downloads from tracked canonical sources."""

import argparse
import hashlib
from pathlib import Path
import subprocess
import zipfile


class PortablePackage:
    """Assemble one Claude-compatible skill folder and an ordinary-chat guide."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.skills = sorted(path.parent.name for path in root.glob("aikea*/SKILL.md"))

    def guide(self) -> bytes:
        sections = [(self.root / "portable/chat-introduction.md").read_text()]
        sections.append("\n## Canonical stage index\n")
        for name in self.skills:
            url = f"https://raw.githubusercontent.com/PatrickGrothOls/AIkea-skill/v0.1.0-alpha.2/{name}/SKILL.md"
            sections.append(f"- [{name}]({url}) — package path: `skills/{name}/SKILL.md`")
        for name in (
            "aikea/references/client-conversation.md",
            "aikea/SKILL.md",
            "aikea/references/overall-wardrobe-measurements-and-settings.md",
            "aikea/assets/wardrobe-measurement-sheet.md",
        ):
            content = (self.root / name).read_text(encoding="utf-8")
            if content.startswith("---\n"):
                content = content.split("---", 2)[2].lstrip()
            sections.append(f"\n---\n<!-- Source: {name} -->\n\n{content}")
        template = (self.root / "aikea/assets/aikea.yaml").read_text()
        sections.append(f"\n## Blank project template\n\n```yaml\n{template}```\n")
        return ("\n".join(sections).rstrip() + "\n").encode("utf-8")

    def members(self) -> dict[str, bytes]:
        tracked = subprocess.check_output(
            ["git", "ls-files", "-z"], cwd=self.root
        ).decode().split("\0")
        members = {}
        for name in tracked:
            path = Path(name)
            if not name or path.parts[0] not in self.skills:
                continue
            source = self.root / path
            if source.is_symlink():
                raise ValueError(f"Portable skill sources must be regular files: {name}")
            members[f"aikea/skills/{name}"] = source.read_bytes()
        for target, source in {
            "SKILL.md": "portable/SKILL.md",
            "setup_aikea.py": "portable/setup_aikea.py",
            "requirements.txt": "requirements.txt",
            "LICENSE.md": "LICENSE.md",
        }.items():
            members[f"aikea/{target}"] = (self.root / source).read_bytes()
        members["aikea/AIKEA_CHAT.md"] = self.guide()
        return members

    def build(self, output: Path, check: bool) -> None:
        guide = self.guide()
        published = self.root / "AIKEA_CHAT.md"
        if check:
            if published.read_bytes() != guide:
                raise ValueError("AIKEA_CHAT.md is stale; run scripts/build_portable_package.py")
        else:
            published.write_bytes(guide)
        output.mkdir(parents=True, exist_ok=True)
        (output / "AIKEA_CHAT.md").write_bytes(guide)
        archive = output / "aikea-skill.zip"
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
            for name, contents in sorted(self.members().items()):
                info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                bundle.writestr(info, contents, compresslevel=9)
        checksums = []
        for path in (archive, output / "AIKEA_CHAT.md"):
            checksums.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n")
        (output / "SHA256SUMS").write_text("".join(checksums), encoding="utf-8")
        print(f"Built {archive} with {len(self.skills)} skills ({archive.stat().st_size:,} bytes)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("dist"))
    parser.add_argument("--check", action="store_true", help="Reject an out-of-date chat guide")
    args = parser.parse_args()
    PortablePackage(Path(__file__).resolve().parents[1]).build(args.output.resolve(), args.check)
