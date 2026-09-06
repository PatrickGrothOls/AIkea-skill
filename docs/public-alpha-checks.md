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
- [ ] Confirm the first GitHub Actions run after the release is pushed.

## Current state

The workflow is prepared for Ubuntu 24.04 with the repository's declared runtime
versions. The skill verifier checks metadata, both discovery link sets, and
local documentation links. After the authored cutter replacement, the complete
suite passes 467 tests and 72 subtests with 5 expected skips. All 23 viewer tests
pass and rebuilding preserves the committed package. GitHub execution remains
unverified until pushed.

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
