---
name: aikea-review-unit
description: Build and open the first generated AIkea cabinet as a visually complete GLB mock-up for client approval. Use immediately after local unit folders are generated, or when repeating the first-unit visual review, before producing the remaining cabinets or manufacturing geometry.
---

# AIkea review unit

## Goal

Give the client one complete-looking cabinet they can rotate and inspect, so its
visible form and proportions are approved before the design is repeated across
the remaining units.

## Present the first cabinet

1. Resolve the active project and require its completed `aikea.yaml` and generated
   `assemblies/` folders.
2. Read [references/visual-review.md](references/visual-review.md) completely.
3. Run `python <skill-directory>/scripts/generate_unit_mockup.py <project>/aikea.yaml`.
4. Run `python <skill-directory>/scripts/serve_unit_review.py <generated-glb>` and
   leave the local viewer available while the client reviews the cabinet.
5. Briefly explain the visible result and ask one concrete question about whether
   its overall shape, proportions, and door appearance look right.
6. Stop with the project awaiting that visual decision. Do not produce the other
   cabinets until the client approves this one.

Communicate as a carpenter guiding a client through the physical result. Say what
the current work gives them and why it matters; keep implementation instructions
and standard construction details inside the skill.

## Responsibility boundary

This stage proves only the visible cabinet mock-up. It does not claim construction
or manufacturing readiness. The approved visible design becomes the reference for
the later deterministic construction stages.
