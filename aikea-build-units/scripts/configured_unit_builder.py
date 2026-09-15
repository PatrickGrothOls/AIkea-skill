"""Scope: Apply the explicit cabinet/base recipe defaults around the common panel executor."""
from adjustable_shelf_support_feature import AdjustableShelfSupportFeature
from korrekt_base_feature import KorrektBaseFeature
from korrekt_base_layout import KorrektBaseLayout
from storage_shelf_policy import StorageShelfPolicy


class ConfiguredUnitBuilder:
    def __init__(self, spec, recipe, fixed_shelf_choices=()):
        self.spec, self.recipe, self.fixed_shelf_choices = spec, recipe, fixed_shelf_choices

    def build(self):
        from assemblies.panel_assembly import PanelAssemblyBuilder
        result = PanelAssemblyBuilder(self.spec,allow_unresolved=True).build()
        if self.recipe == "korrekt_base":
            deck = next(part for part in self.spec.parts if part.role == "base_deck")
            feature = KorrektBaseFeature(KorrektBaseLayout(self.spec.height_mm,deck.local_size_mm[2]))
            return feature.feature(self.spec).apply(result)
        shelves = StorageShelfPolicy().adjustable_ids(self.spec,self.fixed_shelf_choices)
        return AdjustableShelfSupportFeature(shelves).apply(result)
