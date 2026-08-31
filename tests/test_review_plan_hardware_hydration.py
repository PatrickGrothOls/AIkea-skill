"""Scope: Verify hidden review hardware does not require duplicate source geometry."""

from __future__ import annotations

from dataclasses import dataclass

from assembly_composition_test_case import AssemblyCompositionTestCase
from assembly_tree_review_plan import AssemblyTreeReviewPlan
from purchased_hardware_hydrator import PurchasedHardwareHydrator


@dataclass
class RejectingGeometryResolver:
    """Record any incorrect attempt to hydrate plan-supplied geometry."""

    calls: list[str]

    def resolve(self, _project_root, spec):
        self.calls.append(spec.hardware_asset_id)
        raise AssertionError("hidden hardware must not be hydrated")


class TestReviewPlanHardwareHydration(AssemblyCompositionTestCase):
    """Protect the handoff between tree visibility and exact CAD hydration."""

    def test_leaves_hidden_hardware_declared_but_unhydrated(
        self,
        generated_values,
    ) -> None:
        specification, project_root = generated_values
        hardware_spec = specification.PurchasedHardwareSpec(
            "runner_left",
            "Example",
            "R1",
            "asset-left",
            specification.IDENTITY_LOCAL_TO_PARENT,
        )
        root_spec = self.fixture_assembly_spec(
            "cabinet_01",
            "cabinet",
            (),
            (hardware_spec,),
        )
        root = specification.BuiltAssembly(
            root_spec,
            (),
            (),
            purchased_hardware=(
                specification.BuiltPurchasedHardware(hardware_spec, None),
            ),
        )
        plan = AssemblyTreeReviewPlan(
            hidden_paths=(("cabinet_01", "hardware:runner_left"),)
        )
        resolver = RejectingGeometryResolver([])

        hydrated = PurchasedHardwareHydrator(resolver).hydrate(
            project_root,
            root,
            plan.hides,
        )

        assert hydrated.purchased_hardware[0].solid is None
        assert resolver.calls == []


__all__ = ["TestReviewPlanHardwareHydration"]
