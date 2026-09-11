"""Scope: Render a recipe's declared obligations separately from its joint execution."""


class ConfiguredRequirementRenderer:
    """Keep missing fittings visible instead of treating every rendered panel as complete."""

    def render(self, assembly):
        entries, covered = [], set()
        for joint in assembly.joints:
            participants = getattr(joint, "participant_ids", ()) or (
                joint.source_part_id, joint.target_part_id,
            )
            covered.update(participants)
            entries.append(self._entry(
                joint.joint_id, f"{joint.purpose}: {', '.join(participants)}",
                tuple(f"part:{part}" for part in participants),
                (f"joint:{joint.joint_id}",), "operations",
            ))
        entries.extend(self._entry(
            f"{part.part_id}_support", f"Resolve support or attachment of {part.part_id}",
            (f"part:{part.part_id}",), (), "unresolved",
        ) for part in assembly.parts if part.part_id not in covered)
        return "    requirements=(\n" + "\n".join(entries) + "\n    ),\n"

    def _entry(self, identity, description, subjects, operations, disposition):
        return (f"        ConstructionRequirementSpec({identity!r}, {description!r}, "
                f"{subjects!r}, {operations!r}, {disposition!r}),")
