"""Scope: Keep material advice with the dedicated AIkea decision owner."""

from pathlib import Path


class TestAikeaMaterialRouterContract:
    """Protect the entry skill's material-adviser handoff."""

    def test_router_loads_material_adviser_for_the_material_topic(self) -> None:
        skill_text = " ".join(
            (Path(__file__).parents[1] / "aikea" / "SKILL.md").read_text().split()
        )

        assert "At the material or thickness stage" in skill_text
        assert "load `$aikea-choose-materials`" in skill_text
        assert "Return here only when it reports the material stage complete" in skill_text

    def test_router_creates_the_project_and_delegates_before_calculation(self) -> None:
        router = (Path(__file__).parents[1] / "aikea" / "SKILL.md").read_text()

        create_position = router.index("Once the measured space is complete")
        delegation_position = router.index(
            "before classifying any\n   project complete or running the calculator"
        )
        calculation_position = router.index("After the material adviser reports")

        assert create_position < delegation_position < calculation_position

    def test_adviser_owns_legacy_approval_and_unresolved_requirements(self) -> None:
        skill_text = " ".join(
            (
                Path(__file__).parents[1]
                / "aikea-choose-materials"
                / "SKILL.md"
            ).read_text().split()
        )

        assert "Numeric thicknesses alone are legacy inputs" in skill_text
        assert "reference's stable marker" in skill_text

    def test_generated_legacy_project_stops_instead_of_routing_in_a_loop(self) -> None:
        skill_text = " ".join(
            (
                Path(__file__).parents[1]
                / "aikea-choose-materials"
                / "SKILL.md"
            ).read_text().split()
        )

        assert "stop with a material-migration blocker" in skill_text
        assert "Do not mutate `aikea.yaml`" in skill_text
        assert "Return to `$aikea` only after the stage is complete" in skill_text

    def test_drawer_builder_keeps_drawer_material_ownership(self) -> None:
        skill_text = " ".join(
            (
                Path(__file__).parents[1]
                / "aikea-choose-materials"
                / "SKILL.md"
            ).read_text().split()
        )

        assert "`$aikea-build-drawers` owns drawer-box and drawer-front materials" in (
            skill_text
        )
        assert "Never apply the global door choice to drawer fronts implicitly" in (
            skill_text
        )
