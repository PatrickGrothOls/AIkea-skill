---
name: aikea-review-unit
description: Build and show generated AIkea cabinets, structural bases, or the complete furniture run as real CadQuery GLB assemblies for visual approval. Use after local unit folders are generated or when reviewing how approved assemblies meet.
---

# AIkea review unit

Before any client-facing message, including progress commentary, read
[../aikea/references/client-conversation.md](../aikea/references/client-conversation.md)
completely and apply it throughout this stage.

## Goal

Give the client a clear view of the real generated parts as physical assemblies,
so visible form, proportions, and contact between approved assemblies can be
checked before the design is repeated or manufacturing work continues.

## Present the first cabinet

1. Resolve the active project and require its completed `aikea.yaml` and generated
   `assemblies/` folders.
2. Read [references/visual-review.md](references/visual-review.md) completely.
3. Resolve whether the first cabinet has a fitted hinged door. When it does, load
   `$aikea-build-doors` and use its checked closed and open cabinet artifacts for
   this review. The visible door panel, purchased hinges, and paired panel work
   must come from that one completed door relationship.
4. For an intentionally doorless assembly, run
   `python <skill-directory>/scripts/generate_unit_mockup.py <project>/aikea.yaml`.
5. For a cabinet with any registered features, generate the closed complete tree:

   ```bash
   python <skill-directory>/scripts/generate_complete_assembly_review.py \
     <project>/aikea.yaml --assembly <cabinet-id> \
     --output <project>/assemblies/<cabinet-id>/review/complete-closed.glb
   ```

   Generate an exact alternate feature state through the same command. For the
   first fitted-door review, add
   `--state <cabinet-id>/door_hinges=open` and write `complete-open.glb`. Never
   create project-local scripts to combine features; their registered review
   adapters contribute to this generic traversal. Read the command's generated
   `.review.json` for every rendered item and its placed bounds. Do not create a
   project-local inspection or collision script. The complete-tree report plus
   each feature's saved fit, movement, and reservation reports are the evidence
   for visual review; manufacturing authority remains with the later fabrication
   readiness gate.
6. Serve the generated complete GLB:

   ```bash
   python <skill-directory>/scripts/serve_unit_review.py <generated-glb> \
     --review-data <project>/reviews/door-openings.json
   ```

   Leave the local viewer available while the client reviews the cabinet. Show
   both checked states when the completed door supplies closed and open artifacts.
7. Let the loaded model reveal the run-wide opening proposal. It states that
   single doors hinge on the left unless marked otherwise, labels each cabinet,
   and ends with `Approve door openings` and `Change a door`.
8. Stop with the project awaiting that visual decision. An approval confirms the
   saved proposal. A change request returns to the conversation so the client can
   name the cabinet and preferred side before a new checked review is produced.
   Do not produce the other cabinets until the client approves this one.

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

When the client wants to inspect the complete run differently, treat every
cabinet door as an independent review module. Generate the same approved wardrobe
with each requested door closed, open, or removed from view. Use `--doors open`
for a uniform open review, or repeat `--door <assembly-id>=<state>` for specific
cabinets. These are alternate views of unchanged parts and physical positions,
so the verified closed assembly remains the fit and manufacturing reference.

Communicate as a carpenter guiding a client through the physical result. Say what
the current work gives them and why it matters; keep implementation instructions
and standard construction details inside the skill.

## Present a cabinet drawer

When `$aikea-build-drawers` has generated a cabinet-owned drawer child, run
`python <skill-directory>/scripts/generate_drawer_wardrobe_review.py <project>/aikea.yaml --assembly <cabinet-id> --drawer-state <closed|open|removed>`.
Require its drawer position report and the complete wardrobe position report to
pass. Show the door-removed cabinet close-up first, then the same composed
cabinet in the complete furniture run. Treat the closed drawer as the physical
fit authority and the open drawer as its presentation state. The open view must
also pass its runner movement report. Use the removed state to inspect the exact
cabinet-owned runner CAD in its checked mounting frames.

For cabinets with repeated drawer children, use
`generate_drawer_collection_wardrobe_review.py`. Assign drawer extensions and
door states independently so the client can reveal the useful cabinets without
changing any checked closed geometry. It accepts the same `--doors` default and
repeated `--door <assembly-id>=<state>` choices as the full wardrobe review.

For the first KA 4532 drawer fitted with exact article 13952 spacers, save the
closed/open physical proof through the same recursive tree:

`python <skill-directory>/scripts/generate_hettich_ka_4532_spacer_proof.py <project>/aikea.yaml --assembly <cabinet-id> --output-directory <review-directory>`

If a fitted door is present, add `--state <cabinet-id>/door_hinges=open` so both
drawer states are compared with the same unobstructed door state. Require the
saved `ka4532-spacer-movement-collision-check.json` to have no failed checks.
Its swept AABB result is conservative conflict evidence, not an exact collision
claim. The report must retain `manufacturing_authority: false` until the spacer
fixing authority is complete.

## Inspect drawer locking devices

When the client needs to inspect the moving locking devices before their mounting
transform is resolved, export the verified native CAD separately:

`python <skill-directory>/scripts/generate_locking_device_review.py <output.glb> --hardware-directory <directory-containing-the-downloaded-STEP-files>`

This shows the verified handed T51.7601 parts in their vendor coordinate frames.
It is an inspection view only: do not place it on the drawer or represent it as
an installed rail relationship until the hardware-specific mounting transform is
also verified.

## Responsibility boundary

This stage places and displays the parts returned by generated assembly builders.
It does not rebuild or alter their local geometry. Base review may isolate one
module beneath the first cabinet to make their contact legible, while the complete
base remains the authority for the full run. Full-wardrobe review maps every
approved assembly from its own local zero into the shared project coordinates.
Approved visible results become the reference for completing construction and
manufacturing stages.

## Grant fabrication readiness

Read [references/fabrication-readiness.md](references/fabrication-readiness.md)
before making any fabrication claim. After the complete closed assembly is
approved, run
`python <skill-directory>/scripts/check_fabrication_readiness.py <project>/aikea.yaml`.
Only its `fabrication-ready` result grants that state. A valid GLB, a passed
position report, or visual approval alone is insufficient; every recursive
part, joint, machining declaration, purchased item, STEP, drawing, BOM, cut-list
row, feature proof, and current model checksum must pass together.
