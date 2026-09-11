"""Scope: Submit a standard closed review to the same position checker as authored designs."""

from construction_envelope_authority import ConstructionEnvelopeAuthority
from construction_position_evidence import ConstructionPositionEvidence


class ConfiguredConstructionEvidence:
    """Keep presentation-only poses and missing hidden geometry out of manufacturing evidence."""

    def write(self, root, project, visits, filename, door_states, review_plan):
        presentation = any((review_plan.motions, review_plan.hidden_paths,
                            review_plan.hidden_subtrees, review_plan.overlays))
        closed = all(state.value == "closed" for state in door_states.values())
        if filename != "full_wardrobe_review.glb" or presentation or not closed:
            return None
        envelope, allowances, source = ConstructionEnvelopeAuthority().read(
            root, visits[0].assembly.spec.assembly_id, project)
        return ConstructionPositionEvidence().write(root, visits, envelope,
                                                    allowances, envelope_source=source)
