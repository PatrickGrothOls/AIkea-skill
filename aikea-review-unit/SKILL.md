---
name: aikea-review-unit
description: Build and show generated AIkea cabinets, structural bases, or the complete furniture run as real CadQuery GLB assemblies for visual approval. Use after local unit folders are generated or when reviewing how approved assemblies meet.
---

# AIkea review unit

## Goal

Give the client a clear view of the real generated parts as physical assemblies,
so visible form, proportions, and contact between approved assemblies can be
checked before the design is repeated or manufacturing work continues.

## Present the first cabinet

1. Resolve the active project and require its completed `aikea.yaml` and generated
   `assemblies/` folders.
2. Read [references/visual-review.md](references/visual-review.md) completely.
3. Run `python <skill-directory>/scripts/generate_unit_mockup.py <project>/aikea.yaml`.
4. Run `python <skill-directory>/scripts/serve_unit_review.py <generated-glb>` and
   leave the local viewer available while the client reviews the cabinet.
5. Briefly explain the visible result and ask one concrete question about the
   physical feature currently being reviewed.
6. Stop with the project awaiting that visual decision. Do not produce the other
   cabinets until the client approves this one.

## Present the structural base

After the first cabinet is approved and the structural base folders exist, read
[references/assembly-positioning.md](references/assembly-positioning.md), then run
`python <skill-directory>/scripts/generate_base_review.py <project>/aikea.yaml` and
require its generated position check to pass before presenting the result.
Show the complete base by itself from the angles that explain its construction,
then show the first cabinet seated on its matching base module. Keep the review
focused on the physical result and the next decision the client can make.

## Present the full wardrobe

After the first cabinet and its base relationship are approved, run
`python <skill-directory>/scripts/generate_full_wardrobe_review.py <project>/aikea.yaml`
and require the full position report to pass. Open the generated GLB in the same
viewer. Present all saved cabinets with their doors closed on the complete base
so the client can judge the finished facade, spacing, and overall proportions.
Ask whether that complete visible result looks right before moving into the next
construction or manufacturing stage.

When the client wants to inspect the complete run with the doors open, generate
the same approved wardrobe with `--doors open`. This is an alternate view of the
unchanged parts and physical positions, so the verified closed assembly remains
the fit and manufacturing reference.

Communicate as a carpenter guiding a client through the physical result. Say what
the current work gives them and why it matters; keep implementation instructions
and standard construction details inside the skill.

## Responsibility boundary

This stage places and displays the parts returned by generated assembly builders.
It does not rebuild or alter their local geometry. Base review may isolate one
module beneath the first cabinet to make their contact legible, while the complete
base remains the authority for the full run. Full-wardrobe review maps every
approved assembly from its own local zero into the shared project coordinates.
Approved visible results become the reference for completing construction and
manufacturing stages.
