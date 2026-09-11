"""Scope: Reconcile explicit purchased connectors with paired-machining occurrences."""

from collections import defaultdict


class CabineoPurchaseReconciler:
    """Keep modeled purchases and inferred installation requirements from duplicating."""

    def remaining(self, connectors, purchases, unresolved):
        paths = {item["path"] for item in connectors}
        covered = {"connector": set(), "insert": set()}
        claims = defaultdict(list)
        for purchase in purchases:
            occurrence = purchase.get("connection_occurrence_path")
            if occurrence is not None:
                claims[(occurrence, purchase["connection_component"])].append(purchase)
        for (path, component), items in claims.items():
            if (path not in paths or component not in covered or len(items) != 1
                    or items[0]["unit"] != "piece" or items[0]["quantity"] != 1):
                unresolved.append(dict(code="connection.purchase_mismatch", path=path))
                continue
            covered[component].add(path)
        return {component: [item for item in connectors if item["path"] not in covered[component]]
                for component in covered}
