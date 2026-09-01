"""Scope: Verify the KA 4532 drawer command reaches CadQuery runtime handoff."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys

import pytest


pytest.importorskip("cadquery")


class TestGenerateHettichKa4532SpacerCabinetDrawerCommand:
    """Protect fresh projects whose default Python lacks CadQuery."""

    def test_hands_off_before_importing_the_cadquery_generator(self) -> None:
        script = (
            Path(__file__).resolve().parents[1]
            / "aikea-build-drawers"
            / "scripts"
            / "generate_hettich_ka_4532_spacer_cabinet_drawer.py"
        )

        bootstrap_python = Path("/usr/bin/python3")
        if not bootstrap_python.is_file():
            bootstrap_python = Path(sys.executable)
        environment = os.environ.copy()
        environment["AIKEA_CADQUERY_PYTHON"] = sys.executable

        completed = subprocess.run(
            [str(bootstrap_python), "-S", str(script), "--help"],
            check=False,
            capture_output=True,
            env=environment,
            text=True,
        )

        assert completed.returncode == 0, completed.stderr
        assert "Generate one AIkea drawer with KA 4532" in completed.stdout
