"""Scope: Verify exact hardware geometry hydrates at arbitrary tree depth."""

from __future__ import annotations

from dataclasses import dataclass

from assembly_composition_test_case import AssemblyCompositionTestCase
from project_hardware_geometry_resolver import (
    ProjectHardwareGeometryError,
    ProjectHardwareGeometryResolver,
)
from purchased_hardware_hydrator import PurchasedHardwareHydrator


@dataclass
class GeometryResolverProbe:
    """Return visible sentinel geometry while recording requested assets."""

    calls: list[str]

    def resolve(self, _project_root, spec):
        self.calls.append(spec.hardware_asset_id)
        return f"geometry:{spec.hardware_asset_id}"


@dataclass
class ProviderProbe:
    """Expose one asset through the provider registry contract."""

    asset_id: str
    result: object

    def supports(self, asset_id: str) -> bool:
        return asset_id == self.asset_id

    def resolve(self, _project_root, _spec):
        return self.result


class TestPurchasedHardwareHydrator(AssemblyCompositionTestCase):
    """Protect recursive hydration and data-driven provider routing."""

    def test_hydrates_unresolved_child_hardware_once(self, generated_values) -> None:
        specification, project_root = generated_values
        placement = specification.IDENTITY_LOCAL_TO_PARENT
        hardware_spec = specification.PurchasedHardwareSpec(
            "runner_left",
            "Example",
            "R1",
            "asset-left",
            placement,
        )
        child_spec = self.fixture_assembly_spec(
            "drawer_01",
            "drawer",
            (),
            (hardware_spec,),
        )
        child = specification.BuiltAssembly(
            child_spec,
            (),
            (),
            purchased_hardware=(
                specification.BuiltPurchasedHardware(hardware_spec, None),
            ),
        )
        child_declaration = specification.ChildAssemblySpec(
            "drawer_01",
            "drawer",
            placement,
        )
        root_spec = self.fixture_assembly_spec(
            "cabinet_01",
            "cabinet",
            (child_declaration,),
            (),
        )
        root = specification.BuiltAssembly(
            root_spec,
            (),
            (),
            child_assemblies=(
                specification.BuiltChildAssembly(child_declaration, child),
            ),
        )
        probe = GeometryResolverProbe([])

        hydrated = PurchasedHardwareHydrator(probe).hydrate(project_root, root)

        built = hydrated.child_assemblies[0].assembly.purchased_hardware[0]
        assert built.solid == "geometry:asset-left"
        assert probe.calls == ["asset-left"]

    def test_registry_routes_by_asset_identity(self, tmp_path) -> None:
        expected = object()
        resolver = ProjectHardwareGeometryResolver(
            (ProviderProbe("asset-left", expected),)
        )

        result = resolver.resolve(
            tmp_path,
            type("Spec", (), {"hardware_asset_id": "asset-left"})(),
        )

        assert result is expected

    def test_default_registry_claims_each_supported_exact_hardware_family(
        self,
    ) -> None:
        resolver = ProjectHardwareGeometryResolver()
        assets = (
            "movento-760h5000s-runner-left",
            "hettich-ka-4532-500-runner-pair",
            "hettich-13952-spacer-profile",
            "hettich-ka-5332-500-runner-pair",
            "riex-nc70-f000001-closed",
        )

        assert all(
            any(provider.supports(asset) for provider in resolver.providers)
            for asset in assets
        )

    def test_registry_rejects_unregistered_hardware(self, tmp_path) -> None:
        resolver = ProjectHardwareGeometryResolver(())
        spec = type("Spec", (), {"hardware_asset_id": "unknown-asset"})()

        try:
            resolver.resolve(tmp_path, spec)
        except ProjectHardwareGeometryError as error:
            assert "unknown-asset" in str(error)
        else:
            raise AssertionError("unregistered hardware was accepted")
