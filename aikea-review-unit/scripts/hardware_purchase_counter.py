"""Scope: Reconcile explicit modeled members into installed purchased units."""

from collections import Counter, defaultdict


class HardwarePurchaseCounter:
    """Count an installation once, including members owned by a child assembly."""

    def count(self, visits, unresolved: list[dict]) -> list[dict]:
        groups = defaultdict(list)
        for visit in visits:
            spec = visit.hardware.spec
            path = "/".join(visit.path)
            purchase = getattr(spec, "purchase", None)
            if purchase is None:
                unresolved.append(dict(code="hardware.purchase_undefined", path=path))
                continue
            owner = visit.path[:-1]
            levels = purchase.owner_levels_up
            if not 0 <= levels < len(owner):
                unresolved.append(dict(code="hardware.invalid_purchase_owner", path=path))
                continue
            owner = owner[:len(owner) - levels]
            group_path = "/".join((*owner, f"purchase:{purchase.purchase_id}"))
            groups[group_path].append((path, spec, purchase))
        purchases = []
        for path, members in sorted(groups.items()):
            purchase = self._reconcile(path, members, unresolved)
            if purchase:
                purchases.append(purchase)
        return purchases

    def _reconcile(self, path, members, unresolved) -> dict | None:
        first = members[0][2]
        definitions = {
            (spec.manufacturer, purchase.product_code, purchase.unit,
             tuple(sorted(purchase.required_members)), purchase.mounting_fasteners_included)
            for _, spec, purchase in members
        }
        required = Counter(first.required_members)
        actual = Counter(purchase.member for _, _, purchase in members)
        checks = {
            "hardware.purchase_definition_mismatch": len(definitions) != 1,
            "hardware.purchase_members_mismatch": (
                not required or any(value != 1 for value in required.values()) or actual != required
            ),
            "hardware.purchase_identity_missing": (
                not first.purchase_id or not first.product_code or not first.unit
                or not members[0][1].manufacturer
            ),
        }
        failures = [code for code, failed in checks.items() if failed]
        unresolved.extend(dict(code=code, path=path) for code in failures)
        if failures:
            return None
        if not first.mounting_fasteners_included:
            unresolved.append(dict(code="hardware.separate_fasteners_required", path=path))
        return dict(
            path=path,
            manufacturer=members[0][1].manufacturer,
            product_code=first.product_code,
            unit=first.unit,
            quantity=1,
            component_paths=sorted(member[0] for member in members),
            mounting_fasteners_included=first.mounting_fasteners_included,
        )

    def summarize(self, purchases: list[dict]) -> list[dict]:
        groups = defaultdict(list)
        for purchase in purchases:
            key = tuple(purchase[name] for name in ("manufacturer", "product_code", "unit"))
            groups[key].append(purchase["path"])
        return [
            dict(manufacturer=key[0], product_code=key[1], unit=key[2],
                 quantity=len(paths), purchase_paths=sorted(paths))
            for key, paths in sorted(groups.items())
        ]
