# Explicit reuse of existing drilling

## Scope and current state

WP5 drawer-host prerequisite on `feat/shared-drilling-reuse`, based on reviewed
drawer children `5e344cf`. Implementation, focused tests and the review skill
pass. The two review findings are fixed and independently rechecked. This slice lets one saved
mounting pattern explicitly use exactly matching holes from earlier declared
local machining. It does not select hardware or add a new drilling standard.

## Work package and tasks

- [x] Declare named prior operations on surface-drilling inputs.
- [x] Verify whole-hole geometry, same-part ownership and prior execution;
  reject partial overlaps, mismatched dimensions and missing dependencies.
- [x] Preserve the complete mounting-pattern cut record and independently
  verify both reused and newly removed material.
- [x] Prove System 32 reuse, full-pattern reuse, negative cases and serialization.
- [x] Update shared-tool guidance and run the review skill before committing.

## Validation

The shared/reuse drilling group passed 27 tests. A second group covering reuse,
independent output checks, authored panels, extensions and drawer parity passed
41 tests (groups overlap). It includes raw-builder bypass attempts and proof that
one reused hole does not permit another partial collision. All nine skill
packages and links verify. Changed code files remain below 150 lines.
After the review fixes, 33 drilling/reuse/drawer parity tests passed. The
independent reviewer reproduced both original cases against the fix and verified
that full-pattern reuse still removes no additional material and retains both
operation records. No findings remain.

## Audit log

1. The current KA 5332 pattern uses the existing front System 32 hole. Adding
   it as an unrelated operation would correctly trip the collision check.
   Explicit same-hole reuse preserves the existing geometry without weakening
   checks for arbitrary intersecting cuts. This is an implementation dependency
   of the already approved common construction path, not a construction-policy
   change. Hardware choice and physical-fit obligations remain separate.
2. Review found that two overlapping cylinders within one request could enlarge
   a reused hole, and duplicate geometry with different IDs behaved differently
   between construction and raw validation. The shared hole-pattern boundary now
   rejects intersecting/duplicate physical holes. This fixes both paths; merged
   openings require their own supported operation rather than masquerading as
   separate drilled holes.
