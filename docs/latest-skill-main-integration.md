# Integrate the latest skill work into private origin/main

## Scope

Patrick authorized committing the latest Blender setup, logo and related skill
work and pushing it to origin/main on 2026-09-20. Origin was fetched and verified
as the private PatrickGrothOls/AIkea-skill-private-history repository. This does
not publish a public skill release or assert fabrication readiness.

## Current state

The existing branch contains 140 coherent commits above origin/main 52facbf.
The stack includes shared construction, drawer/base policies, hardware sourcing,
Blender provisioning and checked baking, viewer inspection, lighting routes,
release checks and the approved logo. No divergent remote commits were found.
Only the local node_modules link was untracked; it is not a deliverable.

## Work packages and tasks

- [x] WP1: Verify origin, fetch main and check ancestry and local changes.
- [x] WP1: Verify dependencies and all 11 skill metadata/discovery links.
- [x] WP2: Pass 67 viewer tests and reproduce the committed viewer bundle.
- [ ] WP2: Complete the Python suite and resolve integration failures.
- [ ] WP2: Verify hosted CI on the candidate before updating main.
- [ ] WP3: Fast-forward main and push normally; verify the remote commit.

## Audit log

- 2026-09-20: User explicitly authorized the main update, superseding the earlier
  defer-merge instruction. Preserve existing logical commits rather than squash
  the accumulated history; exclude ignored project evidence and dependencies.
- Dependency check and skill discovery passed. Viewer tests: 67 passed. Build
  reproduced tracked output; the existing large-bundle warning remains.
- Reviewed Blender/runtime subprocess argument handling and the read-only release
  checker using the pre-landing checklist. This is focused integration review,
  not a new exhaustive audit of all 621 changed files. Existing cold-start and
  hardware/lighting qualifications remain documented and unresolved.
- Removed one trailing blank line flagged by git diff --check. No behavior change.

- Broad regression exposed a stale preview-role gate still requiring retired rails
  and braces. The preview now requires the common deck/kickboard parts; existing
  Korrekt geometry/inventory tests retain purchased foot and plate checks.
- Updated structural-base eval answers to zero rails/braces, matching kickboards
  and explicit unresolved clip attachments. Shelf eval retains 0.5 mm side fit
  clearance. Generated-builder test now imports the actual recipe and verifies
  its specification instead of pinning obsolete constructor text. Six focused
  taxonomy/eval tests passed.
- Required independent review of the existing >150-line taxonomy test concluded
  its integration/regen concerns are coherent; no line-count-only split needed.
  Preserve current safety gates and do not reinterpret provisional CAD as ready.

- Remaining legacy door/plinth eval now asserts the full 582 mm deck and 82 mm
  kickboard, independently of the door length and front recess (2 tests passed).
- Panel migration comparison targets the unfeatured shared executor; adjustable
  supports are separately covered by feature tests. Door feature removal compares
  hardware specifications and solid differences rather than Python object identity.
- Panel pipeline test projects lack licensed Korrekt sources. A narrowly injected
  test-only provider supplies synthetic placement markers; these tests exercise
  panel geometry/export/evidence plumbing, not vendor fit or fabrication readiness.
  Production providers and checksum rejection remain unchanged.

- Found a prerequisite cycle: component movement proof called the complete review
  path, which demanded finished drawer-layout/travel evidence. Technical component
  proofs now explicitly label their review scope and remain non-manufacturing
  authority; ordinary reviews still reject missing layout evidence before hydration.
  Nine focused proof/review tests passed, including the unchanged rejection gate.
- Independent scope review accepted the existing full-run and drawer-state test
  files as coherent. The injected markers validate synthetic pipeline behavior,
  never exact hardware fit or fabrication readiness.

- The 1,000-test CAD suite is expensive and sequential validation remains running.
  Split hosted verification into four deterministic, disjoint file partitions
  without skips; preserve module/class fixtures and independent memory per runner.
  Local CAD execution remains limited to one heavy process.

- Continued regression corrected per-feature runner counts to preserve the twelve
  default shelf pins rather than treat them as extra drawer hardware. CLI status
  integration uses the same explicitly synthetic marker fixture. The >150-line
  spacer generator test passed the required responsibility review without a split.

- Current mixed-run inventory is 47 panels, 88 hardware components and 79 paired
  Cabineos/inserts: removing the brace frame removes 14 panels and 48 connectors;
  add 48 shelf pins plus 16 feet and 16 plates. Damage tests now target a Cabineo
  joint explicitly instead of accidentally damaging the new base drilling.
- Shelf geometry tests now retain 0.5 mm each-side and 2 mm front/rear clearance.
  Photo configuration checks follow PhotoRenderSession's owned renderer lifetime.
  Thirteen focused viewer/server/process checks passed outside socket restrictions.
- CI partition launch uses a real pytest module subprocess so multiprocessing
  spawn can import its entry point (unlike a stdin Python harness).

- Revalidation and direct tree-review tests now hydrate the same test markers used
  for the original export. Common configured build and sloped position evidence
  both passed locally after this correction; panel migration's four tests passed.
  Six immutable-artifact/approval API tests also passed with localhost permitted.
