"""Scope: Verify generic review orchestration uses registered feature adapters."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from assembly_feature_review import RegisteredAssemblyFeatureReview
from assembly_tree_review_plan import AssemblyReviewMotion, AssemblyTreeReviewPlan
from complete_assembly_review_generator import CompleteAssemblyReviewGenerator
from generate_complete_assembly_review import FeatureStateArguments
from unit_mockup import UnitMockupInputError


class AssemblyTreeAssembly:
    """Represent the minimum owner node consumed by the generic loop."""

    def __init__(self) -> None:
        self.path = ("cabinet_01",)
        self.assembly = SimpleNamespace(
            spec=SimpleNamespace(assembly_id="cabinet_01")
        )


class AssemblyTreePart:
    """Represent the hidden door part referenced by the feature plan."""

    def __init__(self) -> None:
        self.path = ("cabinet_01", "part:door")


class ReviewFeatureProbe:
    """Expose the requested state as one hidden path for observable composition."""

    def __init__(self) -> None:
        self.states = []

    def plan(self, context, state):
        self.states.append((context.owner_path, state))
        return AssemblyTreeReviewPlan(
            hidden_paths=(context.owner_path + ("part:door",),)
        )


class InvalidReviewFeatureProbe:
    """Return one motion targeting an assembly absent from the closed tree."""

    def plan(self, _context, _state):
        return AssemblyTreeReviewPlan(
            motions=(
                AssemblyReviewMotion(("cabinet_01", "missing_01"), object()),
            )
        )


class ReviewLoaderProbe:
    """Return one root for both generated tree walks."""

    def load_assembly(self, _root, _assembly_id):
        return "built"

    def walk(self, _root, _assembly):
        return AssemblyTreeAssembly(), AssemblyTreePart()


class ReviewFeatureLoaderProbe:
    """Return one registered feature independently of builder execution."""

    def __init__(self, feature) -> None:
        self.feature = feature

    def load(self, _root, _owner_path):
        return (RegisteredAssemblyFeatureReview("door", self.feature),)


class HydratorProbe:
    """Prove hidden review paths are not hydrated as physical hardware."""

    def hydrate(self, _root, _built, skip_path):
        assert skip_path(("cabinet_01", "part:door"))
        return "hydrated"


class HydratorMustNotRun:
    """Fail if an invalid review plan reaches hardware resolution."""

    def hydrate(self, *_arguments):
        raise AssertionError("invalid review plan reached hardware hydration")


class GeometryProbe:
    """Return one render item after confirming the merged plan survives."""

    def build(self, _visits, _door_states, plan):
        assert plan.hides(("cabinet_01", "part:door"))
        return ("rendered",)


class ExporterProbe:
    """Capture the generic export call without requiring CadQuery."""

    def __init__(self) -> None:
        self.call = None

    def export(self, assembly_id, parts, output):
        self.call = (assembly_id, parts, output)


class ReporterProbe:
    """Capture the reusable manifest call without geometric bounds."""

    def __init__(self) -> None:
        self.call = None

    def write(self, assembly_id, output, parts, states):
        self.call = (assembly_id, output, parts, states)
        return output.with_suffix(".review.json")


class TestCompleteAssemblyReviewGenerator:
    """Protect recursive orchestration from furniture-specific branches."""

    def test_merges_registered_state_and_exports_one_tree(self, tmp_path) -> None:
        feature = ReviewFeatureProbe()
        exporter = ExporterProbe()
        reporter = ReporterProbe()
        output = tmp_path / "review.glb"
        generator = CompleteAssemblyReviewGenerator(
            loader=ReviewLoaderProbe(),
            feature_loader=ReviewFeatureLoaderProbe(feature),
            hydrator=HydratorProbe(),
            geometry=GeometryProbe(),
            exporter=exporter,
            reporter=reporter,
        )

        result = generator.generate(
            tmp_path,
            "cabinet_01",
            output,
            {"cabinet_01/door": "open"},
        )

        assert feature.states == [(("cabinet_01",), "open")]
        assert exporter.call == ("cabinet_01", ("rendered",), output)
        assert reporter.call == (
            "cabinet_01",
            output,
            ("rendered",),
            {"cabinet_01/door": "open"},
        )
        assert result.feature_selectors == ("cabinet_01/door",)
        assert result.part_count == 1
        assert result.rendered_parts == ("rendered",)
        assert result.report_path == output.with_suffix(".review.json")

    def test_rejects_unknown_feature_selector(self, tmp_path) -> None:
        generator = CompleteAssemblyReviewGenerator(
            loader=ReviewLoaderProbe(),
            feature_loader=ReviewFeatureLoaderProbe(ReviewFeatureProbe()),
            hydrator=HydratorProbe(),
            geometry=GeometryProbe(),
            exporter=ExporterProbe(),
            reporter=ReporterProbe(),
        )

        with pytest.raises(UnitMockupInputError, match="unknown assembly feature"):
            generator.generate(
                tmp_path,
                "cabinet_01",
                tmp_path / "review.glb",
                {"cabinet_01/lighting": "on"},
            )

    def test_cli_state_parser_requires_scoped_selectors(self) -> None:
        assert FeatureStateArguments().parse(
            ["cabinet_01/door_hinges=open"]
        ) == {"cabinet_01/door_hinges": "open"}

        with pytest.raises(ValueError, match="assembly-id"):
            FeatureStateArguments().parse(["door_hinges=open"])

    def test_rejects_invalid_feature_plan_before_hardware_hydration(
        self,
        tmp_path,
    ) -> None:
        generator = CompleteAssemblyReviewGenerator(
            loader=ReviewLoaderProbe(),
            feature_loader=ReviewFeatureLoaderProbe(InvalidReviewFeatureProbe()),
            hydrator=HydratorMustNotRun(),
            geometry=GeometryProbe(),
            exporter=ExporterProbe(),
            reporter=ReporterProbe(),
        )

        with pytest.raises(UnitMockupInputError, match="unknown path"):
            generator.generate(
                tmp_path,
                "cabinet_01",
                tmp_path / "review.glb",
            )
