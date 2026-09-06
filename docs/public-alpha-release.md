# Public alpha release

## Scope

Publish the reviewed alpha with complete viewer notices, an authored machining
cutter, clear product limits, and a clean source history. Preserve prior
development history in a private repository.

## Workpackages and tasks

### WP1 - Release fixes

- [x] Include actual bundled viewer licenses and supplemental notices.
- [x] Replace imported STEP cutter inputs while preserving the brass-insert cut.
- [x] Remove personal project details from the current source tree.
- [x] Document the material identity and manufacturing-output limitations.
- [x] Add the first-project guide and declared-environment CI.
- [x] Pass the complete Python suite and viewer verification locally.

### WP2 - Publication

- [ ] Prepare a fresh Git history with the verified tree and a public identity.
- [ ] Run GitHub Actions against the fresh private release candidate.
- [ ] Preserve the former repository privately and publish the clean alpha.
- [ ] Tag the alpha and verify its public tree, history, and visibility.
- [ ] Bring the original local source folder up to the verified release.

## Current state

The release fixes are committed as separate, reviewable changes. Local
verification passes 467 Python tests, 72 subtests, and 23 viewer tests, with 5
expected Python skips. The receiver remains diameter 9.1 mm and depth 12.5 mm.
The current private repository still contains the old history; a fresh release
repository is needed so earlier personal details and imported STEP objects are
not part of the public Git history.

## Audit log

1. 2026-09-06 - The maintainer approved execution of the public-release review
   fixes and clarified that the female machining pocket was enlarged for brass
   threaded inserts. The replacement preserves the measured custom cut.
2. 2026-09-06 - Each remediation was committed independently: viewer notices,
   public guide and source cleanup, CI, then authored cutter geometry.
3. 2026-09-06 - A fresh release history avoids exposing removed content through
   old Git objects. The existing repository and local development branches will
   remain private; no old history will be force-rewritten or deleted.
