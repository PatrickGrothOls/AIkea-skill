"""Scope: Keep the entry skill aligned with the approved single-door hand policy."""

from pathlib import Path
import unittest


class AikeaRouterDoorHandContractTest(unittest.TestCase):
    """Protect the invariant before the specialized door skill is loaded."""

    def test_router_forbids_boundary_inference_and_defaults_left(self):
        skill_path = Path(__file__).parents[1] / "aikea" / "SKILL.md"
        skill_text = " ".join(skill_path.read_text().split())

        self.assertIn("Never use those room boundaries", skill_text)
        self.assertIn("Every single door begins left-hinged", skill_text)
        self.assertIn("only an explicit client choice", skill_text)


if __name__ == "__main__":
    unittest.main()
