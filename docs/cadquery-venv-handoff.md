# Preserve virtual environments during CadQuery handoff

## Scope

Fix the system-Python command handoff discovered by the first Ubuntu alpha CI
run. Preserve the selected virtual environment's interpreter path.

## Workpackages and tasks

### WP1 - Root cause and regression

- [x] Trace the Ubuntu drawer-command failure to runtime discovery.
- [x] Reproduce loss of both override and current virtual-environment paths.
- [x] Preserve interpreter symlinks while making candidate paths absolute.
- [x] Run runtime and actual command-handoff regression checks.

### WP2 - Release integration

- [x] Commit the fix as a separate checkpoint.
- [x] Apply the same change to the clean release history.
- [x] Confirm the complete Ubuntu workflow passes before publication.

## Current state

The initial Ubuntu run passed 466 tests and 72 subtests, with 5 expected skips.
The system-Python handoff failed because `Path.resolve()` followed the chosen
virtual environment's Python symlink to the base interpreter, which has no
CadQuery package. The macOS base interpreter happened to contain CadQuery and
masked the environment loss. Two focused regression cases now distinguish the
virtual-environment path from its base executable. Both failed before the change;
all 7 runtime and actual command-handoff tests pass after it. The corrected
complete Ubuntu workflow passes 469 tests and 72 subtests, with 5 expected skips.

## Audit log

1. 2026-09-06 - The first Ubuntu run exposed an existing runtime-discovery bug.
   Fixing this shared boundary is necessary to complete the authorized release
   verification; no drawer geometry or machining dimensions need to change.
2. 2026-09-06 - Candidate paths must remain absolute without dereferencing the
   final interpreter symlink, because that path determines Python's environment.
3. 2026-09-06 - The fix changes only candidate-path handling. The regression stub
   also preserves candidate identity so it cannot mask the same bug.
