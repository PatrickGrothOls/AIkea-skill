"""Scope: Adapt a flat multi-part child front to the existing upright hinge host datum."""

from dataclasses import replace

from door_host import DoorHost
from local_to_parent_location import LocalToParentLocation


class AssemblyDoorHost(DoorHost):
    """Use an envelope datum for planning without adding a fictitious physical part."""

    def __init__(self, assembly, declaration, hinge_side):
        if not hasattr(assembly, "spec"):
            raise ValueError("a multi-part door host requires the built parent and real child parts")
        matches = tuple(child for child in assembly.child_assemblies
                        if child.spec.assembly_id == declaration.door_assembly_id)
        if len(matches) != 1 or declaration.door_part_id != declaration.door_assembly_id:
            raise ValueError("the door datum ID must name one directly owned front assembly")
        self.front = matches[0]
        if not self.front.assembly.parts or self.front.assembly.child_assemblies:
            raise ValueError("this door host supports a flat child containing explicit physical panels")
        if declaration.door_part_id in {part.spec.part_id for part in assembly.parts}:
            raise ValueError("the front datum must not duplicate a physical parent part ID")
        boxes = tuple(part.solid.val().located(LocalToParentLocation().build(
            part.spec.local_to_parent)).BoundingBox() for part in self.front.assembly.parts)
        minimum = tuple(min(getattr(box, axis+'min') for box in boxes) for axis in 'xyz')
        maximum = tuple(max(getattr(box, axis+'max') for box in boxes) for axis in 'xyz')
        if any(abs(value) > 1e-6 for value in minimum):
            raise ValueError("the front child datum must start at its width, height and back-face origin")
        reference = replace(self.front.assembly.parts[0].spec,
            part_id=declaration.door_part_id, role="hinge_surface_datum", dimensions_mm=(),
            outline_mm=(), local_size_mm=maximum, inside_face="<Z",
            local_to_parent=self.front.spec.local_to_parent)
        # This dimension-only view exists only inside the host adapter, never in the built tree.
        view = replace(assembly.spec, parts=assembly.spec.parts+(reference,))
        super().__init__(view, declaration, hinge_side)
        self.physical_assembly = assembly

    @property
    def front_subjects(self):
        return tuple(f"{self.front.spec.assembly_id}/part:{part.spec.part_id}"
                     for part in self.front.assembly.parts)
