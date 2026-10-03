"""Scope: Export synthetic routing coupons; no dimensions here qualify a vendor product."""

import argparse
from dataclasses import replace
import json
from pathlib import Path
import sys

PACKAGE = Path(__file__).resolve().parents[2]
for skill in ("aikea", "aikea-build-units", "aikea-add-lighting", "aikea-review-unit"):
    sys.path.insert(0, str(PACKAGE / skill / "scripts"))

import cadquery as cq

from furniture_design_project import FurnitureDesignProject
from generated_project_module_runtime import GeneratedProjectModuleRuntime
from lighting_route_spec import ConnectorPocket, LightingRouteSpec
from panel_setup_checker import PanelSetupChecker
from recessed_luminaire_profile import RecessedLuminaireProfile
from routed_lighting_feature import RoutedLightingFeature


class RoutedLightingCoupon:
    def export(self, output):
        self.output = output.resolve()
        self.output.mkdir(parents=True, exist_ok=True)
        FurnitureDesignProject().initialize(self.output / "project")
        return GeneratedProjectModuleRuntime().execute(self.output / "project", self._build)

    def _build(self):
        from assemblies.specification import IDENTITY_LOCAL_TO_PARENT, PartSpec
        from assemblies.panel_assembly import PanelAssemblySpec, PanelAssemblyBuilder

        profile = RecessedLuminaireProfile("synthetic_routing", "Test fixture",
            "Synthetic rectangular light", "synthetic://not-a-purchased-product",
            4, 8, 24, 10, 2000, (4300,))
        part = PartSpec("panel", "routing coupon", (), IDENTITY_LOCAL_TO_PARENT,
                       local_size_mm=(160, 80, 16), material_id="test_stock")
        base = PanelAssemblyBuilder(PanelAssemblySpec("coupon", "test", (part,), requirements=())).build()
        common = LightingRouteSpec("coupon", "panel", "light", ">Z", ((0, 0), (160, 0)),
            inset_mm=20, start_margin_mm=5, end_margin_mm=5, profile=profile,
            color_temperature_k=4300, cable_width_mm=2, cable_depth_mm=10,
            cutter_radius_mm=0.5, minimum_stock_mm=6)
        records = []
        for end in ("none", "start", "end"):
            pocket = None if end == "none" else ConnectorPocket(20, 8, 9, 1, 18)
            route = replace(common, connector_end=end, connector_pocket=pocket)
            built = RoutedLightingFeature(route).apply(base)
            shape = built.parts[0].solid
            cq.exporters.export(shape, str(self.output / f"connector-{end}.step"))
            records.append({"connector_end": end, "removed_mm3": base.parts[0].solid.val().Volume()-shape.val().Volume(),
                            "setup": PanelSetupChecker().check(built)})
        report = {"fabrication_ready": False, "dimensions": "synthetic test values",
                  "scope": "Single-panel recess coupons; no cross-panel wiring or vendor fit qualification",
                  "coupons": records}
        (self.output / "report.json").write_text(json.dumps(report, indent=2)+"\n")
        return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    print(json.dumps(RoutedLightingCoupon().export(parser.parse_args().output), indent=2))
