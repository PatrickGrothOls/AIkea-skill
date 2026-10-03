# Shared construction regression fixtures

## Scope and current state

Branch `test/shared-construction-regressions` repairs two old test fixtures found
by the full suite at `87bada6`. No production code or assertions are weakened.

## Work package and tasks

- [x] Include the current construction requirement template in the inventory probe.
- [x] Give the runner reservation fixture its actual opposing panel frames and bay.
- [x] Rerun both failed files and inspect the assertions.
- [x] Review using the review skill, including the inherited test file's scope.

## Audit log

1. The full run passed 671 tests and 72 subtests, skipped five and failed two.
   The generated-project renderer already includes the requirement template;
   only the manually copied fixture omitted it. The drawer contract intentionally
   requires actual mounted support frames; the old dummy supplied dimensions only.
2. Preserve the inventory-root and collision-avoidance expectations exactly.
   Refresh test setup rather than adding runtime fallbacks for incomplete inputs.

## Validation

Both files pass: six tests in 4.21 seconds. Independent review reran the same
six tests successfully and found no issues. All original assertions remain.
The [157-line fixture scope review](reviews/shared-reservation-fixture-scope.md)
keeps the data setup with its focused reservation tests. `git diff --check` passes.

The full suite is not claimed as a fresh all-green run: its 671 passing tests
and two repaired failures are separate results. The final integration checkpoint
will rerun the full candidate after the remaining component migrations.
