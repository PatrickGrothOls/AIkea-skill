# Independent full dresser rebuild

## Scope

Rebuild the complete eight-drawer reference dresser with a fresh agent using the
current reusable AIkea skill. The user identified a possible runner-placement
problem in the previous exploded view and explicitly requested this new run.
Check physical runner installation in the assembled model before using an
exploded inspection. No manufacturing approval, push or merge is included.

Branch: `test/dresser-independent-rebuild`, starting at `ce4d125`. Refreshed
`origin/main` and verified its ancestry before creating this isolated worktree.

## Current state

A fresh agent rebuilt the complete reference dresser through this checkout's
skills. The final model has 59 panels and 40 explicit hardware pieces: eight
six-panel drawers, sixteen exact MOVENTO runners, sixteen handed locking clips,
eight dimensioned pull proxies and the complete framed body/legs/top/supports.
Its proposed case is 1450 x 580 x 850 mm; the pulls add 14 mm to occupied depth.
All dimensions and exact stock remain proposals.

The initial full candidate had a real neighboring runner/drawer collision
(9310.853 mm3 maximum), confirmed with actual solids. Reducing box height from
130 to 120 mm preserved the drawer-front layout and removed all 24 adjacent
failure pairs. The final nominal vertical gap is 5.975 mm. The lowest runner
also has only 1.475 mm nominal clearance above its deck; loads and tolerances
remain unqualified.

All 59 pre-finishing panels pass the declared single broad CNC face check. The
final model is **not fabrication-ready**: it retains 88 source intersections
that need resolution, unqualified runner/clip engagement and motion, a concrete
Cabineo end-distance mismatch in the shared clip-rail recipe, and unresolved
stock/fixing/secondary-finishing qualification. Exact pull CAD was obtained as
ACIS DXF/DWG; the existing importer cannot use that source, so the eight pulls
remain explicitly marked proxies.

Only the original photograph and unchanged manufacturer downloads were supplied.
No earlier dresser geometry, placements or generated design were copied. The
parent's prior-image investigation stays separate; new-model review feedback is
recorded explicitly. The >150-line shared contract review passed without refactor.

## Work packages

### WP1 — Freeze inputs and start a fresh builder

- [x] Verify checkout, branch, upstream ancestry and virtual environment.
- [x] Preserve the original image and manufacturer downloads as read-only inputs.
- [x] Record the user's full-design and manufacturing requirements in the agent brief.
- [x] Start the builder without conversation history or prior project access.

### WP2 — Build the complete furniture through the skill

- [x] Interpret and save proposed dimensions without calling them measured facts.
- [x] Build the body, integrated legs/frame, top, eight drawers and eight visible pull proxies.
- [x] Include each exact runner pair, locking hardware, actual clearance supports and mounting cuts.
- [x] Reconcile 188 Cabineo/brass-insert pairs and one declared broad CNC machining face per panel.
- [x] Export the current full assembly through both shared review paths.
- [x] Record capability gaps and complete the independent work-package review.

### WP3 — Independently verify and present

- [x] Measure the prior exploded displacement independently; physical source fit remains unresolved.
- [x] Independently reconcile the new full parts/hardware tree against the reference brief.
- [x] Check closed runner/host/drawer/clip relationships and mounting preparation; preserve unqualified fit findings.
- [x] Run chosen-face, construction and collision checks; establish that no registered motion adapter is present.
- [x] Inspect assembled, underside and exploded views and save screenshots.
- [x] Record remaining manufacturing gaps without suppressing failures.
- [x] Review results, update this plan and commit the bounded evaluation record locally.

## Reproducible evidence

Project root: `local-evidence/fresh-dresser/project`.

- Finished root: `assemblies/dresser_01/builder.py`; pre-finishing root:
  `assemblies/dresser_cnc_01/builder.py`.
- Final construction SHA-256:
  `fcb34a92e1048eb1e323b2a4f0144c2a98f5b658a2307c5681671010b2a5ee78`.
- Final canonical GLB SHA-256:
  `5be765f1df55959098fd84a3aa44bef5a2387fa6bdf4d0f6d616af0e4caf8221`.
- `reviews/dresser_01.geometry-check.json`: 99 pieces, zero invalid solids,
  zero outside-envelope items, zero ordinary overlaps, 88 uncertain source
  intersections; applied-operation verification passes but construction remains
  incomplete and `fabrication_ready` is false.
- `reviews/panel-setup-cnc.json`: 59 compatible panels under construction hash
  `d6d59fe649a7f9daa49725c533716104c9944e7897f6d68e731d67b76534b2d9`.
  The finished-stage audit correctly flags the 12 separate rounding operations.
- `reviews/complete-closed.review.json`: complete 99-piece recursive export;
  valid export status does not confer manufacturing authority. Its empty
  `feature_states` does not establish drawer extension or motion clearance.
- `manufacturing/item-counts.json`: 59 panels, 40 modeled hardware pieces,
  188 declared paired Cabineos and 188 brass inserts. Draft inventory retains
  33 unresolved items; a counted/paired connector is not a qualified joint.
- `reviews/iteration-01/`: preserved initial complete failed model and its
  actual neighboring runner/drawer collision.
- `run-report.md`: source authority, commands, corrections and exact limits.
- `manufacturing/fabrication-readiness.json`: blocked, including 43 unresolved
  construction requirements, 118 missing individual STEP/DXF artifacts, missing
  final manufacturing declarations and approval. Its "missing or stale" position
  message also covers invalid evidence: the current record/hash exists but
  deliberately remains invalid. The generic exact-hardware check only tests
  geometry presence and does not establish the eight proxies' source authority.

Independent evidence is under `local-evidence/parent-review/`:

- `fresh-evidence-reconciliation.json`: counts, exact hashes, initial/final
  collision comparison and measured neighboring envelopes.
- `presentation-provenance.json`: review copies preserve every binary geometry
  buffer and placement. Visual role names preserve metallic source rendering;
  the pull proxies receive only an illustrative finish. The 13-piece mounting
  view hides unrelated parts but retains the actual two full-height supports.
- `fresh-dresser-closed.png`, `fresh-drawer-underside.png`,
  `fresh-dresser-exploded.png`: browser inspections at zero, zero and 25 percent
  separation respectively. Explosion is an inspection pose, not motion or fit
  proof. Both open viewers were restored to their assembled state.
- `specification-responsibility-review.md`: required >150-line contract review.
- `final-fresh-rebuild-review.md`: independent final claim and release-gate review.

The local inspection servers are `http://127.0.0.1:56482/` for the full dresser
and `http://127.0.0.1:56478/?view=bottom` for the mounted drawer underside. Each
serves an immutable display copy of the final model and depends on its running
local process; the canonical GLB and saved screenshots persist separately.

## Remaining manufacturing work

- [ ] Resolve exact MOVENTO source Boolean/engagement and right rear-hook fit.
- [ ] Correct the shared clip-rail connector layout with source-backed end
  distances and actual relief/pilot collision checks before regenerating.
- [ ] Register/qualify exact moving runner members and check full-parent travel.
- [ ] Import exact pull CAD with verified units; qualify handle fixing length.
- [ ] Select exact stock and qualify pilots, screw/insert engagement, tightening
  access, material margins, stability/load and the 12 secondary finishing steps.
- [ ] Generate and qualify manufacturing exports/CAM/workholding, then obtain
  current assembly approval. A GLB and single-face audit do not complete this.

These are identified follow-on gates, not claimed deliverables of this isolated
fresh-run evaluation. No shared production code was changed during this run.

## Evidence boundary

The fresh agent receives the reference image, current skills, manufacturer source
downloads and the explicit manufacturing brief. It does not inherit earlier chat,
results, generated projects or diagnoses. Proposed dimensions remain proposals.
An exploded pose alone cannot establish runner mounting or movement. Geometry,
hardware identity, mounting preparation, single-face machining, material/screw
qualification and fabrication approval remain distinct checks.

## Audit log

- 2026-09-13 — User explicitly requested a new agent to rebuild the entire dresser
  because the exploded drawer's runners look incorrectly fitted. Created this
  isolated evaluation branch from the latest drawer skill and preserved original
  inputs. Fresh generation and independent comparison have separate owners.
- 2026-09-13 — Started `dresser_independent_rebuild` with no conversation history.
  Verified the copied image and all five hardware downloads byte-for-byte and
  verified all eleven skill entrypoints. Input hashes are recorded in
  `local-evidence/parent-review/input-manifest.json`.
- 2026-09-13 — The unchanged shared explosion layout lowers both runners by
  156.384 mm and their clips by 117.288 mm at the previous screenshot's 45 percent
  separation setting; side panels move outward by 114.03 mm. Those inspection
  offsets explain the floating appearance but do not qualify physical fit. The
  separate previous closed report retains its source Boolean, hook and engagement
  problems. Measurements are saved in `previous-explosion-offsets.json` under
  `local-evidence/parent-review/`; this diagnosis was not given to the fresh builder.
- 2026-09-13 — Reviewed the new shared specification at the fresh agent's request
  under the >150-line rule. Generated contract and template are byte-identical at
  153 lines. Independent reviewer recommends keeping the immutable contract
  together; geometry/policy remain in their separate owners. Report:
  `local-evidence/parent-review/specification-responsibility-review.md`.
- 2026-09-13 — First fresh build exposed source-pocket clipping at the top frame
  rail. The agent revised its own proposed rail and removed front/support seams
  with insufficient receiver margins while preserving the supports' top/back/deck
  connections. Parent flagged the fresh design's neighboring drawer/runner height
  envelopes for actual-solid checking; an envelope overlap alone is not classified
  as a physical collision or permission to change geometry.
- 2026-09-13 — The fresh agent confirmed the adjacent-runner collision with both
  intersection and wood subtraction. It retained the failed artifact, reduced
  its proposed box height by 10 mm and rebuilt the whole dresser. Independent
  reconciliation finds zero final adjacent failure pairs and a 5.975 mm nominal
  gap; all 88 unresolved source pairs remain visible to the gate.
- 2026-09-13 — Inspected the actual full assembled model, its mounted underside
  with original support geometry, and the complete exploded inspection. Saved
  screenshots and geometry-preserving display-copy provenance; no source
  hardware was moved or removed to improve appearance or test status.
- 2026-09-13 — Fresh manufacturer review found Lamello's minimum 20 mm end
  positioning requirement. The shared 64 mm MOVENTO clip rail uses seam
  positions 16/52 mm, leaving only 16/12 mm at its ends. The official manual and
  independent reviewer confirm the mismatch. Merely changing positions to
  20/44 mm intersects the existing runner relief, so no unsupported correction
  was applied. This needs a coherent reusable rail/layout correction.
- 2026-09-13 — Completed the full recursive export, inventory and fabrication
  gate. The gate remains blocked. Investigated two misleading generic messages:
  invalid current position evidence is reported as "missing or stale", and
  geometry presence is labeled exact hardware without verifying source identity.
  Recorded those limits instead of using either generic result as stronger proof.
- 2026-09-13 — Final independent review confirmed all 99 unique physical paths,
  80 runner fixing centers, 32 locking-clip fixing centers and all 59 chosen CNC
  faces. It found no additional nominal mounting-frame error, no weakened gate
  and no contradiction in the branch claims. It retained the four substantive
  release boundaries: connector end distance, source fit/motion, separate
  finishing, and exact material/purchase/fixing qualification. Closed and
  underside views are available for the next design review. Only this bounded
  evaluation record is committed; generated experiments and source downloads
  stay in ignored local evidence.
