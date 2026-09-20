"""Scope: Build a deterministic desktop candidate using only tracked distributable files."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import zipfile


class PortablePackage:
    def __init__(self, root):
        self.root = Path(root)

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.root).decode().strip()

    def members(self):
        skills = {path.parent.name for path in self.root.glob("aikea*/SKILL.md")}
        members = {}
        for name in self.git("ls-files", "-z").split("\0"):
            if not name:
                continue
            path = Path(name)
            if path.parts[0] in skills:
                target = "skills/" + name
            elif path.parts[0] == "portable" and path.name != "start-prompt.txt":
                target = str(path.relative_to("portable"))
            elif name in {"LICENSE.md", "requirements.txt"}:
                target = name
            else:
                continue
            source = self.root / name
            if source.is_symlink():
                raise ValueError(f"Package source cannot be a symlink: {name}")
            members[target] = source.read_bytes()
        return members

    def build(self, output, version, download_url=None):
        if self.git("status", "--porcelain", "--untracked-files=no"):
            raise ValueError("Commit tracked changes before building an identifiable candidate")
        if not re.fullmatch(r"\d+\.\d+\.\d+-desktop\.\d+", version):
            raise ValueError("Use a candidate version such as 0.1.0-desktop.1")
        if download_url and not download_url.startswith("https://"):
            raise ValueError("The candidate download URL must use HTTPS")
        members = self.members()
        metadata = {"version": version, "source_revision": self.git("rev-parse", "HEAD")}
        manifest = dict(metadata, files={name: hashlib.sha256(data).hexdigest()
                                        for name, data in sorted(members.items())})
        members["package-manifest.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
        output.mkdir(parents=True, exist_ok=True)
        archive = output / "aikea-skill.zip"
        if archive.exists():
            raise ValueError("Use a new output directory; do not overwrite an existing candidate")
        with zipfile.ZipFile(archive, "w") as bundle:
            for name, contents in sorted(members.items()):
                info = zipfile.ZipInfo("aikea/" + name, date_time=(2026, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.create_system = 3
                info.external_attr = (0o100755 if name.endswith(".sh") else 0o100644) << 16
                bundle.writestr(info, contents, compresslevel=9)
        digest = hashlib.sha256(archive.read_bytes()).hexdigest()
        (output / "SHA256SUMS").write_text(f"{digest}  {archive.name}\n")
        distribution = dict(metadata, sha256=digest, download_url=download_url,
                            status="CANDIDATE_URL_UNVERIFIED" if download_url else "LOCAL_CANDIDATE_ONLY")
        (output / "distribution.json").write_text(json.dumps(distribution, indent=2) + "\n")
        if download_url:
            template = (self.root / "portable/start-prompt.txt").read_text()
            (output / "START_PROMPT.txt").write_text(template.format(download_url=download_url, sha256=digest))
        print(json.dumps(distribution, indent=2))


class PackageCommand:
    def run(self):
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("--output", type=Path, required=True)
        parser.add_argument("--version", required=True)
        parser.add_argument("--download-url", help="Approved candidate URL; still requires external verification")
        args = parser.parse_args()
        PortablePackage(Path(__file__).resolve().parents[1]).build(
            args.output.resolve(), args.version, args.download_url)


if __name__ == "__main__":
    PackageCommand().run()
