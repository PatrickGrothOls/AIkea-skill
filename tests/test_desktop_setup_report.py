"""Scope: Verify persistent setup failure evidence and the desktop acceptance boundary."""

import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "portable"))
from setup_report import SetupReport, SetupStepFailure


class SetupReportTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.report = SetupReport(self.directory / "first", {"version": "test"})

    def test_failure_retains_output_and_exact_failed_stage(self):
        with self.assertRaises(SetupStepFailure):
            self.report.run("export", [sys.executable, "-c",
                            "print('deliberate export failure'); raise SystemExit(7)"], os.environ.copy())
        data = json.loads(self.report.path.read_text())
        self.assertEqual(data["status"], "BLOCKED")
        self.assertEqual(data["failed_stage"], "export")
        self.assertIn("deliberate export failure", (self.report.directory / "export.log").read_text())

    def test_runtime_completion_never_claims_desktop_ready(self):
        self.report.run("probe", [sys.executable, "-c", "print('PASS')"], os.environ.copy())
        self.report.complete({"cad": "isolated/python"}, {"step": "probe.step"})
        data = json.loads(self.report.path.read_text())
        self.assertEqual(data["status"], "RUNTIME_VERIFIED")
        self.assertEqual(data["checks"]["probe"]["status"], "PASS")
        self.assertEqual(data["pending"], ["desktop_interactive_viewer", "furniture_intake"])
        self.assertFalse(data["manufacturing_authority"])
        previous = self.report.path.read_bytes()
        SetupReport(self.directory / "second", {"version": "test"})
        self.assertEqual(self.report.path.read_bytes(), previous)


if __name__ == "__main__":
    unittest.main()
