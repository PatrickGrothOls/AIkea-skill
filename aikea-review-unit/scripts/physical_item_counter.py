"""Scope: Compose a draft physical inventory with explicit counting gaps."""

from dataclasses import asdict

from cabineo_item_counter import CabineoItemCounter
from cabineo_purchase_reconciler import CabineoPurchaseReconciler
from hardware_purchase_counter import HardwarePurchaseCounter


class PhysicalItemCounter:
    """Keep component instances, purchase units, and machining evidence distinct."""

    def count(self, visits) -> dict:
        paths = [visit.path for visit in visits]
        if len(paths) != len(set(paths)):
            raise ValueError("assembly tree contains duplicate instance paths")
        unresolved = []
        parts, hardware, connectors, hardware_visits = [], [], [], []
        for visit in visits:
            if hasattr(visit, "part"):
                parts.append(self._part(visit, unresolved))
            elif hasattr(visit, "hardware"):
                hardware.append(self._hardware(visit, unresolved))
                hardware_visits.append(visit)
            else:
                connectors.extend(CabineoItemCounter().count(visit, unresolved))
        counter = HardwarePurchaseCounter()
        purchases = counter.count(hardware_visits, unresolved)
        remaining = CabineoPurchaseReconciler().remaining(connectors, purchases, unresolved)
        connector_items = self._connector_items(remaining)
        if remaining["connector"]:
            unresolved.append(dict(code="cabineo.purchase_sku_missing", path=visits[0].path[0]))
        return dict(
            schema_version=1,
            status="draft",
            scope="Declared closed-tree inventory; design completeness and fabrication approval not assessed.",
            quantities="Installed units only; supplier packs, stock, prices and delivery excluded.",
            mounting_fasteners="Expected included with purchased parts unless explicitly excepted.",
            totals=dict(manufactured_parts=len(parts), hardware_components=len(hardware),
                        verified_cabineos=len(connectors), brass_inserts=len(connectors)),
            manufactured_parts=parts,
            hardware_components=hardware,
            cabineo_occurrences=connectors,
            purchased_units=purchases,
            purchased_summary=counter.summarize(purchases) + connector_items,
            unresolved=unresolved,
        )

    def _part(self, visit, unresolved) -> dict:
        spec = visit.part.spec
        path = "/".join(visit.path)
        material = getattr(spec, "material_id", "")
        dimensions = spec.local_size_mm
        # DrawerPartSpec provides local_size_mm but no optional panel dimension map or outline.
        named_dimensions = dict(getattr(spec, "dimensions_mm", ()))
        checks = {
            "part.material_missing": not material,
            "part.local_dimensions_missing": len(dimensions) != 3 or any(value <= 0 for value in dimensions),
            "shelf.support_product_undefined": "support_row_height" in named_dimensions,
        }
        unresolved.extend(dict(code=code, path=path) for code, failed in checks.items() if failed)
        return dict(path=path, role=spec.role, quantity=1, material_id=material,
                    local_size_mm=list(dimensions), dimensions_mm=named_dimensions,
                    outline_mm=[asdict(point) for point in getattr(spec, "outline_mm", ())])

    def _hardware(self, visit, unresolved) -> dict:
        spec = visit.hardware.spec
        path = "/".join(visit.path)
        checks = {
            "hardware.placement_missing": visit.local_to_root is None,
            "hardware.product_missing": not spec.manufacturer or not spec.product_code,
        }
        unresolved.extend(dict(code=code, path=path) for code, failed in checks.items() if failed)
        return dict(path=path, manufacturer=spec.manufacturer, product_code=spec.product_code,
                    asset_id=spec.hardware_asset_id, geometry_selector=spec.geometry_selector,
                    quantity=1)

    def _connector_items(self, remaining) -> list[dict]:
        connectors = [item["path"] for item in remaining["connector"]]
        inserts = [item["path"] for item in remaining["insert"]]
        rows = [
            dict(manufacturer="Lamello", product_code=None, description="Cabineo",
                 unit="piece", quantity=len(connectors), occurrence_paths=connectors),
            dict(manufacturer=None, supplier="Häfele", product_code="267.91.314",
                 description="Brass insert for Cabineo 8 M6", unit="piece",
                 quantity=len(inserts), occurrence_paths=inserts, supplier_pack_quantity=100,
                 selection_source="Patrick's supplied product screenshot; compatibility not revalidated"),
        ]
        return [row for row in rows if row["quantity"]]
