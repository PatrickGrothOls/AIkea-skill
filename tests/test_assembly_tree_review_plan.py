"""Scope: Verify generic review poses preserve recursive assembly ownership."""

from __future__ import annotations

from types import SimpleNamespace

import cadquery as cq

from assembly_composition_test_case import AssemblyCompositionTestCase
from assembly_tree_pose_resolver import AssemblyTreePoseResolver
from assembly_tree_review_plan import (
    AssemblyReviewMotion,
    AssemblyTreeReviewPlan,
)


class TestAssemblyTreeReviewPlan(AssemblyCompositionTestCase):
    """Protect local-axis motion and exact path visibility independently of features."""

    def test_moves_a_nested_subtree_along_its_own_axes(
        self,
        generated_values,
    ) -> None:
        values, _ = generated_values
        root_path = ("wardrobe_01",)
        drawer_path = root_path + ("drawer_01",)
        root_frame = values.IDENTITY_LOCAL_TO_PARENT
        drawer_frame = values.LocalToParentPlacement(
            values.Point3D(110.0, 0.0, 0.0),
            values.AxisBasis(
                values.AxisDirection(0.0, 1.0, 0.0),
                values.AxisDirection(-1.0, 0.0, 0.0),
                values.AxisDirection(0.0, 0.0, 1.0),
            ),
        )
        part_frame = drawer_frame.compose_child(
            values.LocalToParentPlacement(
                values.Point3D(5.0, 0.0, 0.0),
                values.IDENTITY_AXIS_BASIS,
            )
        )
        assemblies = {
            root_path: SimpleNamespace(local_to_root=root_frame),
            drawer_path: SimpleNamespace(local_to_root=drawer_frame),
        }
        part = SimpleNamespace(
            path=drawer_path + ("part:left_side",),
            local_to_root=part_frame,
        )
        plan = AssemblyTreeReviewPlan(
            motions=(
                AssemblyReviewMotion(
                    drawer_path,
                    cq.Location(cq.Vector(0.0, -20.0, 0.0)),
                ),
            )
        )
        resolver = AssemblyTreePoseResolver()

        posed = resolver.assembly_locations(assemblies, plan)
        location = resolver.item_location(part, assemblies, posed)
        origin = cq.Vector().transform(cq.Matrix(location.wrapped.Transformation()))

        assert (origin.x, origin.y, origin.z) == (130.0, 5.0, 0.0)

    def test_hides_exact_items_and_complete_subtrees(self) -> None:
        plan = AssemblyTreeReviewPlan(
            hidden_paths=(("wardrobe_01", "hardware:runner_left"),),
            hidden_subtrees=(("wardrobe_01", "drawer_01"),),
        )

        assert plan.hides(("wardrobe_01", "hardware:runner_left"))
        assert not plan.hides(("wardrobe_01", "hardware:runner_right"))
        assert plan.hides(("wardrobe_01", "drawer_01", "part:left_side"))


__all__ = ["TestAssemblyTreeReviewPlan"]
