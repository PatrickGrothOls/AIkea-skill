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
- Seven affected skill entry points validate. Their relative links resolve.
- Skill contract committed at `1631f02`; the fresh agent completed its first
  whole-dresser prototype against that exact export, with no inherited turns.
- Actual closed geometry and declared entry faces pass for 65 physical pieces.
  Construction remains incomplete: 45 requirements remain open. Fabrication is blocked.
- The reference comparison is recognizable but shows unfinished apron/edge detail,
  grain and handle appearance. The initial source/model has been preserved unchanged.
- Existing installed skill symlinks still point at the original checkout. The
  evaluation used the exact updated export; this does not claim a public release.

## Work packages

### WP1 — Put the constraints in the skill

- [x] Inspect the current entry points and actual checker capabilities.
- [x] Require one chosen face, paired cuts, all hardware holes and explicit finishing stages.
- [x] Explain photograph evidence versus proposed dimensions/hidden construction.
- [x] Validate affected skills and linked references; review the responsibility boundary.
- [x] Commit the coherent skill-contract update.

### WP2 — Independent reference build

- [x] Export the updated skill runtime without old projects, development docs or conversations.
- [x] Give an agent with no inherited turns the user image and a minimal design request.
- [x] Preserve its prompt, chosen assumptions, source and actual output reports.
- [x] Inspect whether it discovered and followed the manufacturing constraints.

### WP3 — Review and show

- [x] Compare the actual complete design with the supplied image.
- [x] Inspect geometry, face compatibility, connection/hardware coverage and limitations.
- [x] Prepare the actual CAD comparison and record observed skill failures.
- [x] Verify browser delivery and responsive comparison; queue the live viewer in Codex.

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
6. 2026-09-12 — The agent independently used two centre supports to avoid opposite
   receiver demands, then ran the mandated audit and retained absent hardware holes
   as unresolved. No machining/design hints were supplied in a follow-up.
7. 2026-09-12 — CUA was unavailable and later reported a locked Mac. The parent
   captured the unchanged GLB through headless Chrome and supplied that image to
   the agent for its visual verdict. This environment intervention is recorded.
8. 2026-09-12 — Preserve the initial attempt, including its appearance and fabrication
   gaps. Parent presentation changes only the camera, not geometry or materials.

## WP1 review

The construction skill owns the process; component skills reference it before
placing holes and review uses it before making compatibility claims. The actual
checker and fabrication gate are unchanged. This is a discoverable skill rule,
not a new automated guarantee about undeclared operations. No design dimensions
or preferred arrangement from earlier prototypes were added.

## Independent trial

- Agent: `reference_dresser_fresh`, started with `fork_turns="none"`.
- Input: the raw user image and the request to recreate the entire dresser as
  a reviewable prototype, with missing dimensions/selections labelled proposals.
- Package: `/private/tmp/aikea-reference-cold-start-1631f02/skills/`.
- New project: `/private/tmp/aikea-reference-cold-start-1631f02/project/`.
- No prior dresser code, dimensions, rendered output, expected arrangement or
  machining solution was supplied. The prepared Python environment is disclosed.
- The handoff did not restate one-face machining or Cabineo policy. Those must
  be discovered from the updated skill, which is the behavior being tested.

## Parent review criteria

Compare the whole photo: eight closed slab fronts, the column/row arrangement,
small external pulls, restrained top overhang/edge, a continuous surrounding
frame, natural-wood presentation and slim straight feet with flat bottoms and
small curved shoulders. Treat apparent proportions as visual evidence, not exact
dimensions or material identification. Do not prescribe hidden construction to
the agent; assess its proposed arrangement from the resulting evidence.

Check one chosen face per actual part, all declared and missing openings,
paired Cabineo receivers, physical connectivity, independent requirements,
actual geometry and any additional finishing stage. Separate visual similarity,
declared-operation compatibility and fabrication completeness in the verdict.

## WP2 and WP3 review

The agent created a proposed 1500 × 500 × 950 mm dresser through the common
`PanelAssemblyBuilder`, paired Cabineo joints, surface pockets and shared drawer
box/stack planners. It authored no replacement cutter or project-local collision
engine. Its seven design Python files stay below 150 lines; their responsibilities
are separated into dimensions, frames, carcass, drawer adaptation, composition
and build. No source code changed after its first successful complete build.

| Check | Observed result |
| --- | --- |
| Full physical tree | 9 assemblies; 57 wooden panels plus 8 pull-form placeholders |
| Closed geometry | Valid; no overlaps, invalid solids, uncertain intersections or envelope violations |
| Declared machining | Applied operations pass; 65 chosen faces reconcile with the official audit |
| Cabineo evidence | 182 paired cut occurrences and 182 brass-insert occurrences; exact supply/installation unresolved |
| Purchased geometry | None; runners and selected pulls are absent |
| Construction coverage | Incomplete; 45 unresolved requirement instances |
| Fabrication gate | Blocked; attachments, motion/load/material proof and manufacturing pack remain incomplete |
| Visual comparison | Recognizable whole dresser; grain, handles, apron and softened edges differ |
| Browser | Viewer and GLB HTTP 200, no page errors; real model captured, live tab queued |

The parent independently reconciled every chosen face against the official audit
and every physical path against the position report. All four reports carry the
same construction fingerprint:
`a37ec88934a098991562da31635d30d76596172b1e7ab3b2d55e7bba6ba8c541`.
All 19 entries in the agent's artifact integrity manifest match their files.

This supports a discoverable one-face planning/checking workflow. It does not
establish an end-to-end manufacturable dresser. The agent explicitly identified
that blind outer drawer-runner holes would conflict with its inner-face box
joinery; withholding those holes is an unresolved requirement, not a solution.
Front and pull attachments are also unresolved despite plausible closed placement.

The mobile comparison displays the actual CAD and the user's reference. Both tabs
were checked at 320, 360 and 736 px in light/dark mode; images load and no horizontal
overflow or runtime errors were observed. The user has not approved the result.

## Retained evidence

The private snapshot is [reference-cold-start](../local-evidence/reference-cold-start/).
It contains the exact compressed skill export, raw photo, handoff prompt, prepared
environment disclosure, unchanged source/project, reports and original screenshot.
Its [parent integrity record](../local-evidence/reference-cold-start/parent-integrity-review.json)
records the independent reconciliation and artifact hashes.

- [Agent construction evidence](../local-evidence/reference-cold-start/project/docs/review-evidence.md)
- [Agent visual verdict](../local-evidence/reference-cold-start/project/docs/visual-verdict.md)
- [Saved actual model](../local-evidence/reference-cold-start/project/reviews/dresser_01.glb)
- [Parent screenshots and browser evidence](../local-evidence/reference-trial-review/)

The package contains no prior project or development documentation. Dependencies
were prepared, so this is not clean-machine installation proof. The local branch
has not been pushed, merged or substituted for the installed skills.

## Observed gaps for a subsequent slice

- [ ] Resolve a complete drawer attachment/runner strategy that keeps all required
  machining on one face, then prove its actual installation and motion.
- [ ] Make material-aware front treatment and grain explicit: the proposed 0.6 mm
  front recess must be reconciled with actual veneer thickness, not rendered as
  if stock selection and surface finish were already settled.
- [ ] Refine the continuous front apron and true curved/softened edge details.
  The initial side-foot outlines are faceted and the front apron is straight.
- [ ] Fix lighting default discoverability. The root routes lighting only when
  the client adds it, while the lighting skill says every new design includes it.
  This fresh agent omitted lighting because the reference does not show it;
  the user did not explicitly opt out. No lighting was retrofitted into this test.
