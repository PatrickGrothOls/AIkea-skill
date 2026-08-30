---
name: aikea-build-doors
description: Build a complete fitted door on an existing generated AIkea cabinet, including exact purchased concealed hinges, paired door and cabinet machining, saved local placement, and closed/open visual review. Use when adding, attaching, checking, opening, or reviewing a hinged AIkea door.
---

# AIkea Build Doors

Before any client-facing message, including progress commentary, read
[../aikea/references/client-conversation.md](../aikea/references/client-conversation.md)
completely and apply it throughout this stage.

Turn the cabinet's saved door relationship into one complete, adjustable fitted
door. The result must connect the visible slab, the selected purchased hinge
system, both participating panels, and the real opening movement through shared
placements.

## Resolve the front first

Confirm that the cabinet run can be divided into supported door leaves before
building any hinge hardware. Read the door-layout section in
[references/door-and-hinge-construction.md](references/door-and-hinge-construction.md).
If the resolved cabinets would create unsuitable leaves, revise the arrangement
before local door construction instead of treating the result as a hardware
search problem.

Treat a left-side hinge as the ordinary single-door arrangement. Apply it to
every single door before visual review unless the project already contains an
explicit client choice for that door. Do not infer another hand from room
boundaries, slopes, or the door's position in the run. Present the complete
proposal with the first visual review so the client can approve it or request an
exception.

## Build one complete door

1. Resolve the active AIkea project and the existing generated cabinet that owns
   the door.
2. Read
   [references/door-and-hinge-construction.md](references/door-and-hinge-construction.md)
   completely.
3. Resolve the door relationship, geometry, material, weight, and every
   cabinet-owned feature that constrains hinge placement. Read every cabinet's
   saved specification and any explicit client opening choices to produce one
   opening-side proposal for the complete run without building later cabinets.
4. Select an exact registered hinge-and-plate profile that supports the resolved
   door. If its source CAD is missing, load `$aikea-source-hardware-cad` and
   resume from the returned project-local hardware directory.
5. Let one calculated hinge plan select the required positions from the cabinet's
   saved hardware grid, produce the matching door-side machining and opening
   pose, and save each opening plan beneath its owning cabinet. Use the shared
   cabinet hardware map so both fixing-node conflicts and physical overlap with
   shelves, runners, or other fittings are resolved before review. Keep the
   run-wide proposal in the project review record.
6. Build closed and open review artifacts from the same machined panels. Use the
   manufacturer's closed and open CAD states when they are supplied rather than
   inventing a hardware movement.
7. Explain the physical result and any genuine compatibility issue. Show the
   first complete door in both states, state the proposed hands for the whole run,
   and stop at `Approve door openings` or `Change a door`. A requested change is
   saved as a project choice and shown again before approval. Repeat no cabinet
   door before that decision.

For the implemented first proof, run:

```bash
python <this-skill>/scripts/generate_door_hinge_review.py \
  <project>/aikea.yaml \
  --assembly <cabinet-id> \
  --hardware-root <project>/hardware/riex/nc70
```

## Current capability

The first construction slice supports one full-overlay 18 mm slab door with the
registered Riex NC70 F000001 soft-close 35 mm hinge and F000049 H0 Euro-screw
plate. It derives the published cup and plate datums, places the published hinge
quantity on adjacent System 32 rows around saved cabinet features and hardware
reservations, machines the door, resolves left- and right-hand rigid placements,
records the standard left-hand proposal or a client-selected exception, and
exports the exact manufacturer closed and open states. A profile compatibility
failure remains visible and prevents fabrication approval without blocking the
visual proof.

Half-overlay and inset relationships, the 26 mm mini-hinge profile, final screw
selection, repetition across a wardrobe, evals, and toolpaths remain later gates.
