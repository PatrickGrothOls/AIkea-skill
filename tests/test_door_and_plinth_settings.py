"""Scope: Verify shared door and plinth choices are read as independent settings."""

from pathlib import Path

import pytest
import yaml

from door_and_plinth_settings import DoorBottom, PlinthFront
from overall_wardrobe_inputs import (
    OverallWardrobeInputError,
    OverallWardrobeInputReader,
)


class TestDoorAndPlinthSettings:
    """Protect new choices while preserving version-eight project meaning."""

    _FIXTURE = Path(__file__).parent / "fixtures" / "flat-aikea.yaml"

    def setup_method(self) -> None:
        self.project = yaml.safe_load(self._FIXTURE.read_text(encoding="utf-8"))

    def test_version_eight_keeps_the_original_full_flush_design(self) -> None:
        settings = OverallWardrobeInputReader().read(self.project).settings

        assert settings.door_bottom is DoorBottom.FLOOR
        assert settings.plinth_front is PlinthFront.FLUSH
        assert settings.plinth_recess_mm == 0.0

    @pytest.mark.parametrize(
        ("door_bottom", "plinth_front", "recess_mm"),
        (
            ("floor", "flush", 0),
            ("floor", "recessed", 60),
            ("plinth", "flush", 0),
            ("plinth", "recessed", 60),
        ),
    )
    def test_version_nine_reads_every_independent_combination(
        self,
        door_bottom: str,
        plinth_front: str,
        recess_mm: float,
    ) -> None:
        self.project["schema_version"] = 9
        self.project["design_settings"]["doors"]["bottom"] = door_bottom
        self.project["design_settings"]["base"].update(
            {"front": plinth_front, "recess": recess_mm}
        )

        settings = OverallWardrobeInputReader().read(self.project).settings

        assert settings.door_bottom.value == door_bottom
        assert settings.plinth_front.value == plinth_front
        assert settings.plinth_recess_mm == recess_mm

    @pytest.mark.parametrize(
        ("plinth_front", "recess_mm"),
        (("flush", 60), ("recessed", 0)),
    )
    def test_rejects_a_recess_that_conflicts_with_the_plinth_choice(
        self,
        plinth_front: str,
        recess_mm: float,
    ) -> None:
        self.project["schema_version"] = 9
        self.project["design_settings"]["doors"]["bottom"] = "floor"
        self.project["design_settings"]["base"].update(
            {"front": plinth_front, "recess": recess_mm}
        )

        with pytest.raises(OverallWardrobeInputError):
            OverallWardrobeInputReader().read(self.project)
