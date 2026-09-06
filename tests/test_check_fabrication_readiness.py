"""Scope: Verify invalid readiness checks replace stale fabrication approval."""

from __future__ import annotations

import json
from unittest.mock import Mock

from check_fabrication_readiness import CheckFabricationReadinessCommand
from fabrication_readiness_report import (
    FabricationReadinessCheck,
    FabricationReadinessReport,
)


class TestCheckFabricationReadinessCommand:
    """Protect the command boundary from leaving a stale ready report behind."""

    def test_invalid_yaml_overwrites_existing_ready_report(
        self,
        tmp_path,
        capsys,
    ) -> None:
        project_file = tmp_path / "aikea.yaml"
        project_file.write_text("[", encoding="utf-8")
        self._write_ready_report(tmp_path)

        status = CheckFabricationReadinessCommand().run(project_file)

        assert status == 2
        self._assert_blocked_report(tmp_path)
        payload = json.loads(capsys.readouterr().out)
        assert payload["status"] == "invalid"

    def test_evaluation_exception_overwrites_existing_ready_report(
        self,
        tmp_path,
        capsys,
        monkeypatch,
    ) -> None:
        project_file = tmp_path / "aikea.yaml"
        self._write_ready_report(tmp_path)
        command = CheckFabricationReadinessCommand()
        monkeypatch.setattr(
            command,
            "_evaluate",
            Mock(side_effect=RuntimeError("evaluation crashed")),
        )

        status = command.run(project_file)

        assert status == 2
        report = self._assert_blocked_report(tmp_path)
        assert report["checks"][0]["problems"] == ["evaluation crashed"]
        payload = json.loads(capsys.readouterr().out)
        assert payload["report"].endswith("manufacturing/fabrication-readiness.json")

    def test_an_empty_report_cannot_be_fabrication_ready(self) -> None:
        report = FabricationReadinessReport(())

        assert not report.is_ready
        assert report.as_dict()["status"] == "blocked"

    def _write_ready_report(self, project_root) -> None:
        FabricationReadinessReport(
            (FabricationReadinessCheck(code="previous.ready", passed=True),)
        ).write(project_root / "manufacturing/fabrication-readiness.json")

    def _assert_blocked_report(self, project_root) -> dict[str, object]:
        report_path = project_root / "manufacturing/fabrication-readiness.json"
        report = json.loads(report_path.read_text(encoding="utf-8"))
        assert report["status"] == "blocked"
        assert report["checks"][0]["code"] == "evaluation.invalid"
        assert report["checks"][0]["passed"] is False
        return report


__all__ = ["TestCheckFabricationReadinessCommand"]
