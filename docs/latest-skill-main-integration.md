# Integrate the latest skill work into private origin/main

## Scope

Patrick authorized committing the latest Blender setup, logo and related skill
work and pushing it to origin/main on 2026-09-20. Origin was fetched and verified
as the private PatrickGrothOls/AIkea-skill-private-history repository. This does
not publish a public skill release or assert fabrication readiness.

## Current state

The complete stack was fast-forwarded from 52facbf to 50eb7df and pushed to
private origin/main; the remote SHA was independently verified. It includes
shared construction, drawer/base policies, hardware sourcing, Blender provisioning
and checked baking, viewer inspection, lighting routes and the approved logo.
Verification across hosted and local runs accounts for all 1,002 Python cases:
996 passed and six optional-asset checks skipped. All 67 viewer tests passed and
the viewer build reproduced tracked output. The final eight-partition hosted run
is still pending; it is not claimed green. Local dependencies and project evidence
remain excluded from Git.

## Work packages and tasks

- [x] WP1: Verify origin, fetch main and check ancestry and local changes.
- [x] WP1: Verify dependencies and all 11 skill metadata/discovery links.
- [x] WP2: Pass 67 viewer tests and reproduce the committed viewer bundle.
- [x] WP2: Account for the complete Python suite and resolve integration failures.
- [ ] WP2: Finish the independent eight-partition hosted verification.
- [x] WP3: Fast-forward main and push normally; verify the remote commit.

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

- The complete focused integration run passed 16 tests. Hosted candidate 26a1ef6
  passed the viewer and three Python partitions (767 passed, four optional skips);
  the fourth partition exceeded the available time in the earlier diagnostic run.
  Split coverage across eight runners, keeping the 30-minute bound and deriving
  the stride from the matrix size so no test is omitted or duplicated.
- The local remaining partition exposed dataclass identity changing across
  generated-module reloads. Door-feature removal now compares all serialized
  hardware fields as well as the existing solid-difference checks.
- Both hinge hands and the full door-machining file passed locally. The runner
  assertion now checks both the model family (KA 5332) and its exact purchase
  article (9057405) in their respective fields rather than conflating them.
- Final remaining partition coverage passed in three local segments: 44 passed;
  10 passed/one optional skip; 175 passed/one optional skip. Combined with the
  three hosted partitions, every collected case has a passing or optional-skip
  result on the final code. This evidence replaces waiting for the earlier
  four-partition hosted timeout before integration; the fresh hosted run remains
  an explicit pending verification, not a claimed pass.
- Fast-forwarded and pushed main normally, preserving the logical commit history.
  git ls-remote verified origin/main at 50eb7df157c0b710d0bd30cf512cb7fc5ec5973f.
  This documentation-only follow-up records the completed integration and does
  not change the tested code or resolve outstanding fabrication/release gates.
