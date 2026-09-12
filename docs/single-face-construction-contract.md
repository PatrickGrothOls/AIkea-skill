# One-face skill contract and fresh image-led trial

## Scope

Patrick wants a fresh agent to reconstruct the whole dresser in his supplied
reference, using the skill without the previous dresser conversation or code.
First ensure the skill itself carries the single-face three-axis CNC and paired
Cabineo constraints. This is a prototype design test, not publication or cutting.

## Current state

- Baseline `d3751ad`; refreshed `origin/main` is an ancestor.
- Isolated branch `docs/single-face-construction-contract`.
- Found a real routing gap: the one-face checker was listed in the tool map but
  the construction skill did not mandate the process or invoking its audit.
- Added one owning process reference, routed from design, build and review.
- A fresh skill export and image-only design trial are being prepared.
- Existing installed skill symlinks still point at the original checkout. The
  evaluation will use the exact updated export; this does not claim a public release.

## Work packages

### WP1 — Put the constraints in the skill

- [x] Inspect the current entry points and actual checker capabilities.
- [x] Require one chosen face, paired cuts, all hardware holes and explicit finishing stages.
- [x] Explain photograph evidence versus proposed dimensions/hidden construction.
- [x] Validate affected skills and linked references; review the responsibility boundary.
- [x] Commit the coherent skill-contract update.

### WP2 — Independent reference build

- [ ] Export the updated skill runtime without old projects, development docs or conversations.
- [ ] Give an agent with no inherited turns the user image and a minimal design request.
- [ ] Preserve its prompt, chosen assumptions, source and actual output reports.
- [ ] Inspect whether it discovered and followed the manufacturing constraints.

### WP3 — Review and show

- [ ] Compare the actual complete design with the supplied image.
- [ ] Inspect geometry, face compatibility, connection/hardware coverage and limitations.
- [ ] Show the resulting CAD model and record any observed skill failures.

## Audit log

1. 2026-09-12 — Patrick clarified that the whole reference dresser is the target,
   not just replacement feet. The interrupted feet-only turn made no edits.
2. 2026-09-12 — Patrick requested a fresh agent and asked whether machining rules
   must be added first. The skill's missing requirement is corrected before the trial.
3. 2026-09-12 — Keep process policy in one construction reference. Do not encode
   this dresser's dimensions, leg shape or previous design solution into the skill.
4. 2026-09-12 — Use a prepared CAD runtime so this tests independent design and
   skill behavior, not clean-computer installation. Old projects and our proposed
   solution are withheld from the agent. Its actual output will be reviewed.
5. 2026-09-12 — Direct drawer, door and lighting entry points also read the same
   process reference; their added holes cannot bypass the design-stage policy.

## WP1 review

The construction skill owns the process; component skills reference it before
placing holes and review uses it before making compatibility claims. The actual
checker and fabrication gate are unchanged. This is a discoverable skill rule,
not a new automated guarantee about undeclared operations. No design dimensions
or preferred arrangement from earlier prototypes were added.
