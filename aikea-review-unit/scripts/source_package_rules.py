"""Scope: Define portable source paths allowed in editable CNC request archives."""

from pathlib import PurePosixPath


class SourcePackageRules:
    SUFFIXES = {".py", ".js", ".jsx", ".ts", ".tsx", ".css", ".html", ".json",
                ".yaml", ".yml", ".toml", ".ini", ".cfg", ".md", ".txt", ".csv", ".sh", ".lock"}
    DIRECTORIES = {".git", ".aws", ".ssh", ".venv", "venv", "node_modules", "__pycache__",
                   ".worktrees", "local-evidence", "dist", "reviews", "renders", "cnc-files"}
    NAMES = {"credentials", "credentials.json", "secrets.json", "secrets.yaml",
             "secrets.yml", "token.json", "package-manifest.json"}

    @classmethod
    def allows(cls, name):
        path = PurePosixPath(name)
        parts = name.split("/")
        if (not name or "\\" in name or ":" in name or any(ord(c) < 32 for c in name)
                or any(p in {"", ".", ".."} for p in parts) or len(name) > 500):
            return False
        if any(p.lower() in cls.DIRECTORIES or p.lower().startswith(".env") for p in parts):
            return False
        if path.name.lower() in cls.NAMES:
            return False
        return path.suffix.lower() in cls.SUFFIXES or path.name in {"Makefile", "Dockerfile", ".gitignore"}
