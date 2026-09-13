"""Scope: Resolve inspection ownership from explicit physical assembly relationships."""

from unit_mockup import UnitMockupInputError


class ReviewInspectionIdentity:
    """Keep display grouping separate from physical item names and source identity."""

    def path(self, item, assemblies) -> tuple[str, ...]:
        path = tuple(segment.split(":", 1)[-1] for segment in item.path[1:])
        if type(item).__name__ != "AssemblyTreeHardware":
            return path
        # Older saved projects may carry their own pre-ownership hardware contract.
        mounting_part = getattr(item.hardware.spec, "mounting_part_id", None)
        if mounting_part is None:
            return path
        owner = assemblies[item.path[:-1]].assembly
        if mounting_part not in {part.spec.part_id for part in owner.parts}:
            raise UnitMockupInputError([
                f"hardware mounting part is missing: {'/'.join(item.path)} -> {mounting_part}"
            ])
        return path[:-1] + (mounting_part, path[-1])
