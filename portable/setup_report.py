"""Scope: Persist setup stages and subprocess evidence without declaring desktop success."""

import json
from pathlib import Path
import subprocess


class SetupStepFailure(RuntimeError):
    """A logged subprocess failed; the caller must preserve its evidence."""


class SetupReport:
    def __init__(self, directory, package):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.path = self.directory / "setup-report.json"
        self.data = {"status": "RUNNING", "package": package, "checks": {},
                     "pending": ["desktop_interactive_viewer", "furniture_intake"],
                     "manufacturing_authority": False}
        self.save()

    def save(self):
        pending = self.path.with_suffix(".tmp")
        pending.write_text(json.dumps(self.data, indent=2) + "\n")
        pending.replace(self.path)

    def run(self, name, command, env):
        log_path = self.directory / f"{name}.log"
        self.data["active_stage"] = name
        self.data["checks"][name] = {"status": "RUNNING", "command": command,
                                     "log": str(log_path)}
        self.save()
        print(f"SETUP {name}: {log_path}", flush=True)
        with log_path.open("w") as log:
            try:
                subprocess.run(command, env=env, stdout=log, stderr=subprocess.STDOUT,
                               check=True)
            except (subprocess.CalledProcessError, OSError) as error:
                self.data["checks"][name].update(status="FAILED", error=str(error))
                self.data.update(status="BLOCKED", failed_stage=name)
                self.save()
                raise SetupStepFailure(f"{name} failed; inspect {log_path}") from error
        self.data["checks"][name]["status"] = "PASS"
        self.save()

    def complete(self, interpreters, artifacts):
        self.data.update(status="RUNTIME_VERIFIED", active_stage=None,
                         interpreters=interpreters, artifacts=artifacts)
        self.save()
        print(f"RUNTIME_VERIFIED: {self.path}; desktop viewer and intake still pending.", flush=True)
