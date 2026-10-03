"""Scope: Verify the KA 5332 saved-drawer command boundary."""

from pathlib import Path
import sys
from unittest.mock import Mock, patch

import pytest

from generate_hettich_ka_5332_cabinet_drawer import (
    GenerateHettichKa5332CabinetDrawerCommand,
    main,
)


class TestGenerateHettichKa5332CabinetDrawerCommand:
    """Require sourced hardware and the discovered CadQuery runtime."""

    def test_parser_requires_the_hardware_directory(self) -> None:
        with pytest.raises(SystemExit):
            GenerateHettichKa5332CabinetDrawerCommand.parser().parse_args(
                ["aikea.yaml", "--assembly", "cabinet_01", "--bottom-height-mm", "300"]
            )

    def test_parser_accepts_the_hardware_directory(self) -> None:
        arguments = GenerateHettichKa5332CabinetDrawerCommand.parser().parse_args(
            [
                "aikea.yaml",
                "--assembly",
                "cabinet_01",
                "--bottom-height-mm",
                "300",
                "--hardware-directory",
                "hardware/source",
            ]
        )

        assert arguments.hardware_directory == Path("hardware/source")

    def test_main_reexecutes_in_the_discovered_cadquery_runtime(self) -> None:
        runtime = Mock()
        runtime.current_is_ready.return_value = False
        runtime.run_script.return_value = 7

        with patch(
            "generate_hettich_ka_5332_cabinet_drawer.CadQueryRuntime.from_environment",
            return_value=runtime,
        ):
            result = main()

        assert result == 7
        runtime.run_script.assert_called_once_with(
            Path(sys.modules[main.__module__].__file__).resolve(),
            sys.argv[1:],
        )
