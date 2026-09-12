"""Scope: Declare the exact made-to-length lighting variant as one physical purchase."""
from purchased_hardware_spec import HardwarePurchaseSpec, PurchasedHardwareSpec


class LightingPurchase:
    def build(self, run, local_to_parent):
        variant = f"{run.profile.product_name} / {run.length_mm:g} mm / {run.color_temperature_k} K"
        return PurchasedHardwareSpec(run.run_id, run.profile.manufacturer, variant,
            run.profile.profile_id, local_to_parent,
            geometry_selector=f"{run.length_mm:g}mm_{run.color_temperature_k}k",
            purchase=HardwarePurchaseSpec(run.run_id, variant, "piece", "luminaire", ("luminaire",)))
