"""Scope: Provide shared project data and calculation setup for overall tests."""

from pathlib import Path

import yaml

from overall_wardrobe_calculator import OverallWardrobeCalculator
from overall_wardrobe_inputs import OverallWardrobeInputReader
from overall_wardrobe_results import OverallWardrobeResult


class OverallWardrobeTestProject:
    """Load a fresh flat project and run its overall calculation."""

    def load_flat(self) -> dict:
        path = Path(__file__).parent / "fixtures" / "flat-aikea.yaml"
        return yaml.safe_load(path.read_text(encoding="utf-8"))

    def calculate(self, project: dict) -> OverallWardrobeResult:
        inputs = OverallWardrobeInputReader().read(project)
        return OverallWardrobeCalculator().calculate(inputs)
