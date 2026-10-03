"""Scope: Reject private paths and obvious credentials in Git's index without echoing values."""

from pathlib import PurePosixPath
import re
import subprocess


class PrivateFileCheck:
    RULES = {
        "aws-access-key": re.compile(rb"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
        "github-token": re.compile(rb"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{60,})\b"),
        "private-key": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH |DSA |ENCRYPTED )?PRIVATE KEY-----"),
        "service-token": re.compile(rb"\b(?:sk-proj-|sk-ant-api|xox[baprs]-)[A-Za-z0-9_-]{20,}"),
        "credential-assignment": re.compile(
            rb"(?im)^\s*(?:export\s+)?[\"']?(?:aws_secret_access_key|aws_session_token|api_key|secret_key|password|access_token)[\"']?\s*[:=]\s*[\"']?([A-Za-z0-9/+_=.-]{16,})"),
        "personal-email": re.compile(rb"\b[A-Za-z0-9._%+-]+@(?:gmail|hotmail|outlook|icloud)\.com\b", re.I),
    }
    PLACEHOLDERS = (b"example", b"placeholder", b"synthetic", b"test-", b"your_")

    @staticmethod
    def private_path(name):
        path = PurePosixPath(name)
        parts, base = path.parts, path.name.lower()
        if any(part in {"local-evidence", ".aws", ".ssh", ".direnv", ".worktrees", "deployment.local"} for part in parts):
            return True
        environment = base == ".env" or base.startswith(".env.")
        return ((environment and base not in {".env.example", ".env.sample", ".env.template"})
                or base.endswith((".pem", ".key", ".p12", ".pfx", ".local.json"))
                or base in {".netrc", "credentials", "credentials.json"})

    def inspect(self, name, content):
        findings = []
        if self.private_path(name):
            findings.append((name, 0, "private-path"))
        for rule, pattern in self.RULES.items():
            for match in pattern.finditer(content):
                if rule == "credential-assignment" and match.group(1).lower().startswith(self.PLACEHOLDERS):
                    continue
                findings.append((name, content.count(b"\n", 0, match.start()) + 1, rule))
        return findings

    def indexed_findings(self, root="."):
        listing = subprocess.check_output(["git", "ls-files", "--stage", "-z"], cwd=root)
        findings = []
        for entry in listing.split(b"\0"):
            if not entry:
                continue
            metadata, name = entry.split(b"\t", 1)
            mode, blob, stage = metadata.split()
            filename = name.decode("utf-8", errors="replace")
            if stage != b"0" or mode == b"160000":
                findings.append((filename, 0, "unreviewed-index-entry"))
                continue
            content = subprocess.check_output(["git", "cat-file", "blob", blob.decode()], cwd=root)
            findings.extend(self.inspect(filename, content))
        return findings

    def run(self):
        findings = self.indexed_findings()
        for name, line, rule in findings:
            # repr escapes control characters in paths; never print matched content.
            print(f"{name!r}:{line}: {rule}")
        print(f"Privacy check: {len(findings)} finding(s); matched values are withheld.")
        return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(PrivateFileCheck().run())
