"""Scope: Reject hanging-rail solids intersecting existing cabinet parts or fittings."""
from local_to_parent_location import LocalToParentLocation


class HangingRailClearance:
    def validate(self, assembly, added):
        from assemblies.assembly_tree import AssemblyTreeWalker, AssemblyTreePart, AssemblyTreeHardware
        old = []
        for visit in AssemblyTreeWalker().walk(assembly):
            if isinstance(visit, AssemblyTreePart):
                old.append(('/'.join(visit.path), self.world(visit.part, visit.local_to_root)))
            elif isinstance(visit, AssemblyTreeHardware) and visit.hardware.has_geometry:
                old.append(('/'.join(visit.path), self.world(visit.hardware, visit.local_to_root)))
        for item in added:
            solid = self.world(item, item.spec.local_to_parent)
            box = solid.BoundingBox()
            for identity, other in old:
                bound = other.BoundingBox()
                overlaps = (min(getattr(box, axis+'max'), getattr(bound, axis+'max'))-
                            max(getattr(box, axis+'min'), getattr(bound, axis+'min'))
                            for axis in 'xyz')
                if min(overlaps) <= 1e-6:
                    continue
                if solid.intersect(other).Volume() > 1e-6:
                    raise ValueError(f'{item.spec.hardware_id} intersects {identity}; revise the rail layout')

    def world(self, item, placement):
        solid = item.solid.val() if hasattr(item.solid, 'val') else item.solid
        return solid.moved(LocalToParentLocation().build(placement))
