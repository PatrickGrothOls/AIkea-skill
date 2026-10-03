# Common construction checks

## Scope

WP4 of [the foundation plan](shared-construction-foundation.md), on
`feat/common-construction-checks`, based on reviewed WP3 `76ce13a`.
Reuse the existing fabrication gate and physical tree to check configured,
custom and extended construction at official review/export boundaries.

## Current state

WP4a (operation result validation and shared entry points) is implemented and its
independent review findings are fixed and rechecked. WP4b (explicit requirement
coverage, extension qualification and context binding) is also implemented and
reviewed; see [its evidence](construction-requirement-evidence.md). Generic position
records and bounded contact allowances remain for WP4c. These slices keep the stack reviewable.
WP3 is fully verified: 561 unique tests and 72 subtests passed, five skipped,
including a successful rerun of local HTTP tests with socket permission.

## Work package and tasks

- [x] Inventory existing geometry, machining, feature and artifact checks.
- [x] Validate declared operations, participant coverage and actual removed
  material on any returned built tree, including directly authored builders.
- [x] Record explicit construction requirements and disposition/evidence gaps.
- [x] Keep extension qualification separate from successful solid generation.
- [x] Apply the common operation checks to review and fabrication commands for any root.
- [ ] Keep expected contact allowances bounded to exact participants/evidence.
- [x] Bind changed requirements, material, operations and products to current
  review evidence, reusing artifact checks where possible.
- [x] Test valid extensions, plausible-but-incomplete results and stale evidence.
- [ ] Run the `review` skill, fix/recheck findings and commit the slice.

## Audit log

1. Patrick authorized common validation and qualified extensions in WP4. Reuse
   `FabricationReadinessGate`; no new independent fabrication-ready switch.
2. Existing artifact checks compare actual STEP solids, feature-owned part hashes,
   exact position fingerprints and approved closed GLB bytes. Existing tree
   machining checks only require a cut with each joint ID; they do not check all
   participants or whether those cuts were applied. That is the first gap to close.
3. A complete tree cannot reveal requirements omitted from the design brief.
   Requirement coverage must be explicit and keep that limitation visible;
   neither touching panels nor connector spacing establishes structural strength.
4. The generic build command currently calls the bare builder, and fabrication
   CLI assumes `wardrobe_01`. Both need the existing complete-builder selection
   and arbitrary root selection, while preserving older artifact paths.
5. WP4a now checks returned results at the shared loader and repeats checks in the
   fabrication gate. It recomputes built-in cutters, checks full occurrence sets
   and rejects cut metadata that does not match removed material. Custom joint
   types remain explicitly unqualified at the gate pending WP4b evidence handling.
6. Generic rebuilds invalidate their previous report before execution and record
   the complete new report after export. A previous GLB can remain for inspection,
   but a failed run never references it as a fresh successful artifact.
7. An older loader-selection test returned a bare string. Updated that fixture
   to return a real built panel because the loader now validates physical output;
   its original complete-builder/runtime-selection assertion remains covered.
8. Independent review reproduced a bypass for a partially clipped System 32 grid.
   Added full local-cutter containment and collisions with earlier machining to
   the output checker, matching the shared executor. Raw clipped and duplicate
   grid regressions now reject both forms of incomplete construction.
9. A clean subprocess exposed a missing feature-runtime import when the fabrication
   CLI initialized its hardware providers. Hydration now runs inside the existing
   project runtime context; the custom-root CLI reaches the real artifact gates.

## WP4a verification

- Output-validator and fabrication-gate tests: 12 passed.
- Mixed geometry, feature, inventory and readiness regression: 29 passed; one
  fixture contract failure fixed as described above. All five feature-composition
  tests then passed.
- Final focused operation/boundary/gate/feature/CLI regression: **25 passed**.
- Independent review rechecked both fixes: two focused regressions passed; no
  outstanding findings. Primary critical/informational review is also complete.
- Standard/custom geometry parity and complete sloped four-unit review: **six
  passed**, including all six miters and unequal-thickness rejection. This full
  geometry check took 129 seconds; output validation adds CAD work at review boundaries.
- Changed code files are below 150 lines. No new database, network or publication
  behavior is introduced. Fabrication-ready status remains owned by the existing gate.
