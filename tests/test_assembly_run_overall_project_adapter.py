"""Scope: Verify generated assembly runs retain their global room boundaries."""

from __future__ import annotations

import unittest

from assembly_run import AssemblyRunReader
from assembly_run_overall_project_adapter import AssemblyRunOverallProjectAdapter


class TestAssemblyRunOverallProjectAdapter(unittest.TestCase):
    def test_explicit_room_boundaries_survive_the_run_adapter(self) -> None:
        boundaries = {"left": True, "right": True, "top": True}
        project = {
            "design_settings": {
                "installation_boundaries": boundaries,
                "assembly_run": {
                    "left_clearance": 5,
                    "right_clearance": 5,
                    "gap": 2,
                    "ceiling_clearance": 0,
                    "assemblies": [
                        {
                            "id": "tall_storage_01",
                            "purpose": "tall_storage",
                            "width_share": 1,
                        }
                    ],
                },
            }
        }

        assembly_run = AssemblyRunReader().read(project)
        adapted = AssemblyRunOverallProjectAdapter().adapt(project, assembly_run)

        self.assertEqual(adapted["design_settings"]["installation_boundaries"], boundaries)
        self.assertIn("cabinet_run", adapted["design_settings"])
        self.assertIn("assembly_run", project["design_settings"])


if __name__ == "__main__":
    unittest.main()
