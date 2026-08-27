"""Scope: Provide shared setup for structural base review tests."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import yaml

from assembly_taxonomy_generator import AssemblyTaxonomyGenerator


class BaseReviewTestCase(unittest.TestCase):
    """Build one temporary generated project for each base review test."""

    _FIXTURE = Path(__file__).parent / "fixtures" / "review-unit-aikea.yaml"

    def setUp(self) -> None:
        from base_review_generator import BaseReviewGenerator

        self.temporary_directory = TemporaryDirectory()
        self.project_root = Path(self.temporary_directory.name)
        self.project = yaml.safe_load(self._FIXTURE.read_text(encoding="utf-8"))
        AssemblyTaxonomyGenerator().generate(self.project, self.project_root)
        self.generator = BaseReviewGenerator()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()
