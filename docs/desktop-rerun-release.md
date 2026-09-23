# Desktop release and fresh run

## Scope
Publish the completed material, presentation, export and hardware sourcing fixes
in one installer, then observe a fresh Claude desktop run from the public starter
prompt. During that run, handle approvals only; do not coach or modify its work.

## Current state
Published v0.1.0-desktop.3 and merged PR #9 to main at af89870. The public archive
matches its checksum and all 602 manifest members; a clean macOS setup passed
real CAD and Blender probes. Seven CI partitions and the viewer passed on
8f0edcd; the remaining partition passed on 92083d0 after shortening a megabyte
parameter ID. No test inputs, assertions or production files changed in that
last correction. The complete repeat CI run remains in progress.

The fresh Claude run has not started. Native desktop screenshots remain visible,
but New Chat and keyboard actions do not produce a verified new-chat screen;
coordinate input reports noWindowsAvailable. Desktop access or permission to use
Chrome is pending. No prompt, coaching or file changes were sent to Claude.

## Work packages
- [x] WP1: Integrate the completed branches and resolve the README conflict.
- [x] WP1: Review the combined diff and run affected regression checks.
- [x] WP2: Build the versioned installer and verify its runtime probes.
- [x] WP2: Publish the release, update public links and merge to main.
- [x] WP2: Download the public archive and verify its checksum and contents.
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

- 2026-09-23: Seven CI partitions and the viewer passed. The final partition
  stopped advancing its visible log immediately before the oversized-response
  case, whose default pytest ID contains one million characters. Added explicit
  short case IDs without changing inputs, assertions or production code.

- 2026-09-23: Published the installer from 7626f42 and independently verified its
  public bytes. PR #9 merged at af89870. The remaining full CI rerun is recorded
  separately from the completed coverage across validation runs. The desktop
  interaction blocker remains unresolved; the acceptance run has not begun.

## Claude observation log
Not started. No instructions or workarounds have been supplied to Claude.
Detailed local observations: `local-evidence/desktop-rerun-20260923/RUN_LOG.md`.
