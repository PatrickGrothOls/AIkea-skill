# Desktop release and fresh run

## Scope
Publish the completed material, presentation, export and hardware sourcing fixes
in one installer, then observe a fresh Claude desktop run from the public starter
prompt. During that run, handle approvals only; do not coach or modify its work.

## Current state
The fixes are integrated. All 66 selected regression checks pass and all 11 skill
packages resolve their links. The clean installer passed real CAD and Blender probes. Public release and
the fresh Claude run are pending; full CI exposed an outdated material assertion. The SL 322 exact STEP acquisition remains a
task for the construction workflow, not a completed result of this release.

## Work packages
- [x] WP1: Integrate the completed branches and resolve the README conflict.
- [x] WP1: Review the combined diff and run affected regression checks.
- [x] WP2: Build the versioned installer and verify its runtime probes.
- [ ] WP2: Publish the release, update public links and merge to main.
- [ ] WP2: Download the public archive and verify its checksum and contents.
- [ ] WP3: Start a fresh Claude desktop run using only the public starter prompt.
- [ ] WP3: Log observed steps, approvals, questions and final artifacts.
- [ ] WP3: Report the actual outcome without repairing the acceptance run.

## Audit log
- 2026-09-23: Patrick authorized publishing and merging the local fixes, then an
  approval-only cold start with a log. Integration retains the newer README
  wording and all material propagation code. No unrelated branches are included.
- 2026-09-23: Combined targeted suite: 66 passed. Skill package: 11 skills passed.
  Existing real Blender and CAD evidence remains separate from the fresh run.

- 2026-09-23: Clean macOS installer passed all four runtime stages, including
  real lighting and exact geometry verification. Full CI found an old test
  expecting an empty material after generation. Updated that assertion to the
  fixture's selected material; production behavior and package bytes are unchanged.

## Claude observation log
Not started. No instructions or workarounds have been supplied to Claude.
