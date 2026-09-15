# Full-depth adjustable shelves

## Scope
Carry Patrick's shelf-depth clarification into the existing shelf policy and
current Vilja build, preserving the cabinet-owned System 32 support grid.

## Current state
Instructions updated; the existing drawer agent has the change for the same
assembly. Displayed geometry still contains the old shortened shelves. No shelf
or hardware fit claim follows from this instruction update.

## Work packages
### WP1 — Preserve the design requirement
- [x] Require nearly full usable depth and four real pins in the common grid.
- [x] Allow visual overlap of lighting while retaining physical clearance checks.
- [x] Flag the existing shelf-relative support helper for grid reconciliation.
- [x] Send the change to the agent working on the same assembly.
### WP2 — Verify delivery
- [ ] Agent removes the 95 mm setback and verifies actual grid/pin bearing and clearance.
- [ ] Export and review changed shelves in the complete drawer assembly.
- [x] Validate the skill and prepare the focused policy commit.

## Audit log
1. Patrick requested shelves sitting on pins in the 32 mm pattern, nearly full
   depth, and explicitly allowed overlap of the lighting line.
2. Reuse actual cabinet rows/columns. A shortened shelf must not move its support
   holes off the common grid. The existing helper is shelf-relative, so its output
   needs reconciliation rather than an unsupported claim that it already does this.

3. Agent proposes 414 mm shelf depth (2 mm front clearance to 416 mm inner back),
   with pins at existing cabinet-depth columns 37/379 mm. This remains subject to
   physical clearance checks and is not yet exported.
