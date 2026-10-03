# Preserve new shared design source

## Scope
Include permitted, nonignored untracked repository source dependencies in the
working-copy quote archive, using the same existing source-path exclusions.

## Work packages
- [x] Reproduce a new root helper missing from an otherwise accepted archive.
- [x] Include tracked and nonignored untracked source without staging customer work.
- [x] Cover shared helpers, ignored scratch files, other designs and excluded exports/secrets.
- [x] Pass 31 focused source, validation and hosted-flow tests.
- [x] Complete fresh independent reviews: round 3 passes all lanes.
- [x] Publish and merge.

## Current state
The selected repository snapshot includes new shared files as well as selected
design files and branch docs. Known excluded paths remain excluded; users must
still review the source snapshot because filename filtering is not secret scanning.

## Audit log
- 2026-10-01: Accepted the reproduced missing-helper defect under Patrick's review
  loop. Use Git's nonignored working-copy inventory with the existing allow policy
  so regeneration dependencies are preserved without changing files or staging them.

Release evidence and remaining limits: [desktop4-release.md](desktop4-release.md).
