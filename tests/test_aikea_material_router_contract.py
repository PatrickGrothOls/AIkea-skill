"""Scope: Keep material advice with the dedicated AIkea decision owner."""

from pathlib import Path


class TestAikeaMaterialRouterContract:
    """Protect the entry skill's material-adviser handoff."""

    def test_router_loads_material_adviser_for_the_material_topic(self) -> None:
        skill_text = " ".join(
            (Path(__file__).parents[1] / "aikea" / "SKILL.md").read_text().split()
        )

        assert "When the next missing topic is material or thickness" in skill_text
        assert "load `$aikea-choose-materials`" in skill_text
        assert "save only the client's confirmed" in skill_text

    def test_legacy_thicknesses_do_not_count_as_material_approval(self) -> None:
        skill_text = " ".join(
            (Path(__file__).parents[1] / "aikea" / "SKILL.md").read_text().split()
        )

        assert "numeric thicknesses alone do not prove approval" in skill_text
        assert "legacy projects that contain thicknesses" in skill_text
