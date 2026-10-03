"""Scope: Verify the native locking-device inspection command boundary."""

from pathlib import Path

from generate_locking_device_review import GenerateLockingDeviceReviewCommand


class TestLockingDeviceReviewCommand:
    """Keep review inputs explicit so local CAD provenance remains visible."""

    def test_accepts_an_output_and_hardware_directory(self) -> None:
        arguments = GenerateLockingDeviceReviewCommand.parser().parse_args(
            [
                "output/t51-devices.glb",
                "--hardware-directory",
                "downloads",
            ]
        )

        assert arguments.output == Path("output/t51-devices.glb")
        assert arguments.hardware_directory == Path("downloads")
