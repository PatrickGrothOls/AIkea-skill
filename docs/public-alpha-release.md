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

- [x] Prepare a fresh Git history with the verified tree and a public identity.
- [x] Run GitHub Actions against the fresh private release candidate.
- [x] Preserve the former repository privately.
- [x] Tag the alpha and verify its clean tree, history, and private release.
- [ ] Obtain explicit publication approval and change visibility to public.
- [x] Bring the original local source folder up to the verified release.

## Current state

The release fixes are committed as separate, reviewable changes. The fresh
alpha's exact code commit `ccb8f03`, tagged `v0.1.0-alpha.1`, passes 469 Python
tests, 72 subtests, and 23 viewer tests on GitHub, with 5 expected Python skips.
The receiver remains diameter 9.1 mm and depth 12.5 mm. The clean history excludes
removed personal content and imported CAD; all new commits use a public no-reply
identity.

`PatrickGrothOls/AIkea-skill` holds the verified alpha and remains private.
`PatrickGrothOls/AIkea-skill-private-history` retains the former repository and
development history privately. Automatic approval review rejected changing
visibility because it requires explicit approval to expose this source tree.
That visibility change is the only remaining publication action.

The original development folder tracks the private-history remote. Future public
changes must be based on the clean alpha history; do not merge the old private
history into the publication repository.

## Audit log

1. 2026-09-06 - The maintainer approved execution of the public-release review
   fixes and clarified that the female machining pocket was enlarged for brass
   threaded inserts. The replacement preserves the measured custom cut.
2. 2026-09-06 - Each remediation was committed independently: viewer notices,
   public guide and source cleanup, CI, then authored cutter geometry.
3. 2026-09-06 - A fresh release history avoids exposing removed content through
   old Git objects. The existing repository and local development branches will
   remain private; no old history will be force-rewritten or deleted.
4. 2026-09-06 - The first Ubuntu run passed 466 tests and found one runtime
   handoff failure. A separate fix preserves interpreter symlinks and includes
   two regressions that failed before the correction and now pass.
5. 2026-09-06 - The original source folder now contains the release changes and
   a local copy of the verified CadQuery 2.7 environment. Its previous runtime
   is retained under the ignored `env/` directory. Local discovery selects the
   intended virtual environment, and skill packaging checks pass there.
6. 2026-09-06 - The corrected complete Ubuntu workflow and viewer job pass at
   `ccb8f03`. The private alpha tag points to that exact verified code commit.
7. 2026-09-06 - The original repository retains its identity under the private
   history name. The fresh repository now uses the intended AIkea-skill URL.
   Both remain private; their histories were neither rewritten nor deleted.
8. 2026-09-06 - Automatic approval review rejected the public-visibility action
   because the full source payload needs explicit publication authorization.
   The private tag and release notes were completed without retrying publication.
9. 2026-09-06 - Final release-record and platform-description changes affect
   documentation only. Their commits skip duplicate CI; no verified code or
   workflow changes accompany that record update.
