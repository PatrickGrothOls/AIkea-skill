# Public alpha verification checks

## Scope

Run declared-environment verification on pushes and pull requests, including
Python tests, local skill discovery, viewer tests, and committed build output.

## Workpackages and tasks

### WP1 - Automation

- [x] Pin official checkout and setup actions to verified release commits.
- [x] Add Python dependency, skill packaging, and test checks.
- [x] Add viewer tests and exact committed-output verification.
- [x] Run the local packaging command and review the workflow.

### WP2 - Release validation

- [x] Run the full Python suite in the declared environment.
- [x] Confirm viewer rebuilding preserves the committed package.
- [x] Review the diff for this configuration checkpoint.
- [x] Confirm GitHub Actions after the release candidate is pushed.

## Current state

The workflow is prepared for Ubuntu 24.04 with the repository's declared runtime
versions. The skill verifier checks metadata, both discovery link sets, and
local documentation links. The corrected release candidate `ccb8f03` passes
469 Python tests and 72 subtests with 5 expected skips on Ubuntu 24.04. All 23
viewer tests pass and rebuilding preserves the committed package.
The complete [GitHub run](https://github.com/PatrickGrothOls/AIkea-skill/actions/runs/34046085643)
passes. Later publication-record edits change documentation only.

## Audit log

1. 2026-09-06 - The user authorized the release review's follow-up checks.
   CI turns the existing verification commands into repeatable release evidence.
2. 2026-09-06 - Official action release tags were resolved to immutable commits.
   The workflow requests read-only repository permissions and uses the existing
   direnv environment contract.
3. 2026-09-06 - The full-suite failure was `OSError: No space left on device` in
   the subprocess's temporary record write. Its isolated rerun passed after
   temporary-output cleanup; no production or test behavior was changed.
4. 2026-09-06 - The complete suite subsequently passed in one run after the
   authored cutter replacement: 467 tests, 72 subtests, and 5 expected skips.
5. 2026-09-06 - The first Ubuntu run exposed a runtime handoff that dereferenced
   virtual-environment interpreter symlinks. The fix includes two regressions;
   the corrected complete workflow passes 469 tests and 72 subtests, with 5
   expected skips. The viewer job also passes all 23 tests and output comparison.
