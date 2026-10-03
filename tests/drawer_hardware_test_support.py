"""Scope: Supply a no-CAD hardware gate double to drawer generator unit tests."""

from dataclasses import dataclass, field
from pathlib import Path

from drawer_hardware_set_verifier import SOURCE_CAD_VERIFIED_UNPLACED


@dataclass(frozen=True, slots=True)
class VerifiedDrawerHardwareSetTestDouble:
    """Expose only the state consumed after the gate succeeds."""

    geometry_state: str = SOURCE_CAD_VERIFIED_UNPLACED


class DrawerHardwareSetVerifierTestDouble:
    """Accept profiles whose full hardware identity set is registered."""

    def verify(self, runner):
        runner.require_hardware_asset_set()
        return VerifiedDrawerHardwareSetTestDouble()


@dataclass(slots=True)
class DrawerHardwareSetVerifierFactoryTestDouble:
    """Record the explicit directory while avoiding STEP import in unit tests."""

    hardware_directories: list[Path] = field(default_factory=list)

    def create(self, hardware_directory: Path) -> DrawerHardwareSetVerifierTestDouble:
        self.hardware_directories.append(hardware_directory)
        return DrawerHardwareSetVerifierTestDouble()


TEST_HARDWARE_DIRECTORY = Path("test-hardware-directory")


__all__ = [
    "DrawerHardwareSetVerifierFactoryTestDouble",
    "TEST_HARDWARE_DIRECTORY",
]
