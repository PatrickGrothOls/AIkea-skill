"""Scope: Verify proof authority is cleared before CadQuery runtime handoff."""

from __future__ import annotations

import json

import pytest

import generate_hettich_ka_4532_spacer_proof as command_module
from cadquery_runtime import CadQueryRuntimeError


class MissingCadQueryRuntime:
    """Reproduce a launcher that cannot locate a usable CadQuery interpreter."""

    def current_is_ready(self) -> bool:
        return False

    def run_script(self, script, arguments) -> int:
        raise CadQueryRuntimeError("No CadQuery Python runtime")


class MissingCadQueryRuntimeFactory:
    """Supply the failing runtime without probing the developer machine."""

    @classmethod
    def from_environment(cls) -> MissingCadQueryRuntime:
        return MissingCadQueryRuntime()


class TestGenerateHettichKa4532SpacerProofCommand:
    """Prevent a launcher failure from leaving older valid proof evidence."""

    def test_runtime_handoff_failure_invalidates_older_report(
        self,
        tmp_path,
        monkeypatch,
    ) -> None:
        output, report_path = self._stale_report(tmp_path)
        monkeypatch.setattr(command_module, "CadQueryRuntime", MissingCadQueryRuntimeFactory)
        monkeypatch.setattr(
            command_module.sys,
            "argv",
            [
                "generate_hettich_ka_4532_spacer_proof.py",
                str(tmp_path / "aikea.yaml"),
                "--assembly",
                "cabinet_01",
                "--output-directory",
                str(output),
            ],
        )

        assert command_module.main() == 2

        evidence = json.loads(report_path.read_text(encoding="utf-8"))
        assert evidence["status"] == "invalidated-before-run"
        assert evidence["manufacturing_authority"] is False
        assert evidence["problems"] == ["No CadQuery Python runtime"]

    def test_argument_failure_invalidates_older_report(
        self,
        tmp_path,
        monkeypatch,
    ) -> None:
        output, report_path = self._stale_report(tmp_path)
        monkeypatch.setattr(
            command_module.sys,
            "argv",
            [
                "generate_hettich_ka_4532_spacer_proof.py",
                str(tmp_path / "aikea.yaml"),
                "--assembly",
                "cabinet_01",
                "--output-directory",
                str(output),
                "--bogus",
            ],
        )

        with pytest.raises(SystemExit):
            command_module.main()

        evidence = json.loads(report_path.read_text(encoding="utf-8"))
        assert evidence["status"] == "invalidated-before-run"
        assert evidence["manufacturing_authority"] is False

    def _stale_report(self, tmp_path):
        output = tmp_path / "review"
        output.mkdir()
        report_path = output / "ka4532-spacer-movement-collision-check.json"
        report_path.write_text('{"status":"previously-valid"}', encoding="utf-8")
        return output, report_path
