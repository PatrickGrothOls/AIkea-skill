"""Scope: Verify the KA 5332 prototype consumes a sourced hardware directory."""

from pathlib import Path

import pytest

from generate_hettich_ka_5332_prototype import (
    GenerateHettichKa5332PrototypeCommand,
)


class TestGenerateHettichKa5332PrototypeCommand:
    """Keep the review command aligned with the hardware-sourcing handoff."""

    def test_accepts_the_sourced_hardware_directory(self) -> None:
        arguments = GenerateHettichKa5332PrototypeCommand.parser().parse_args(
            [
                "project/aikea.yaml",
                "--assembly",
                "tall_storage_01",
                "--hardware-directory",
                "project/hardware/hettich/ka-5332/9057405/source",
                "--output-directory",
                "review",
            ]
        )

        assert arguments.hardware_directory == Path(
            "project/hardware/hettich/ka-5332/9057405/source"
        )

    def test_requires_the_sourced_hardware_directory(self) -> None:
        with pytest.raises(SystemExit):
            GenerateHettichKa5332PrototypeCommand.parser().parse_args(
                [
                    "project/aikea.yaml",
                    "--assembly",
                    "tall_storage_01",
                    "--output-directory",
                    "review",
                ]
            )
