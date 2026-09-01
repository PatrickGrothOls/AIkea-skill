"""Scope: Render one recursive-review registration for a KA 4532 drawer."""

from __future__ import annotations


class HettichKa4532SpacerReviewModuleRenderer:
    """Bind the generated drawer child to its exact review travel."""

    def render(self, plan) -> str:
        return (
            '"""Scope: Articulate the generated KA 4532 drawer subtree."""\n\n'
            "from hettich_ka_4532_spacer_review_feature import (\n"
            "    HettichKa4532SpacerReviewFeature,\n"
            ")\n\n\n"
            "REVIEW = HettichKa4532SpacerReviewFeature(\n"
            f"    {plan.drawer.assembly_id!r},\n"
            f"    {plan.hardware.nominal_runner_length_mm!r},\n"
            ")\n"
        )


__all__ = ["HettichKa4532SpacerReviewModuleRenderer"]
