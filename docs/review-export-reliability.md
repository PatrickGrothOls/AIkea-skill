# Review export reliability

## Scope

Fix wide-index geometry verification and preserve Riex door/hardware identities
in open review states. Keep positions, source CAD and ownership unchanged.

## Current state

Both fixes pass 9 regression tests. The real Claude cabinet exports in closed
and open states with the same 32 physical identities; every triangle index is
valid. Evidence is local-evidence/claude-export-regression/export-verification.json.
The tested Blender bake correction is the parent branch.

## Work packages

- [x] Reproduce and fix offsets beyond 65,535 vertices without changing triangles.
- [x] Preserve actual panel/hinge/plate ownership in alternate review states.
- [x] Export a complete real cabinet and compare identities in closed/open states.
- [x] Review, test and commit this focused fix before hanging-rail construction.

## Audit log

- 2026-09-21: User authorized resolving both export failures and the hanging rail.
  Fix export data ownership first so real purchased hardware can be verified in
  the resulting cabinet; do not relax identity or geometric equality checks.

- 2026-09-21: Reviewed the focused diff: widened integer arithmetic only; restored
  identity from actual purchased-hardware specs without moving geometry or
  loosening the verifier. All modified production files remain below 150 lines.
