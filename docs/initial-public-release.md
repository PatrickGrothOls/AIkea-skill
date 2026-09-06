# Initial public AIkea skill release

## Scope

Publish the complete AIkea skill source in a new public GitHub repository while
leaving the existing private AIkea application repository unchanged.

The release permits personal and other noncommercial use. Commercial use is not
granted and requires separate permission from the licensor.

## Plan

### WP1 - Release assembly

- [x] Confirm both feature branches descend from the standalone skill mainline.
- [x] Create a clean publication worktree and release branch.
- [x] Integrate the reviewed material-advice and latest KA 4532 spacer work.
- [x] Confirm the combined tree has no merge residue or unrelated changes.

### WP2 - Licensing and public documentation

- [x] Add the unmodified PolyForm Noncommercial License 1.0.0.
- [x] State clearly that personal and noncommercial use is permitted.
- [x] State clearly that commercial use requires separate permission.
- [x] Avoid describing the noncommercial release as OSI open source.
- [x] Record the provenance caveat for bundled Cabineo cutter assets.

### WP3 - Verification

- [x] Validate every packaged AIkea skill entrypoint.
- [x] Run the complete Python suite.
- [x] Run the viewer test and production build.
- [x] Independently review combined code simplicity and stability.

### WP4 - Publication

- [x] Create `PatrickGrothOls/AIkea-skill` as a public repository.
- [x] Publish the verified release as the default `main` branch.
- [x] Verify visibility, license text, default branch, and remote HEAD.
- [x] Change the repository to private pending the maintainer's sensitive-content review.
- [ ] Publish the clean replacement repository only after the maintainer approves.

## Current state

The material-advice and latest KA 4532 spacer branches are integrated without
merge conflicts. Clean installation exposed an unsatisfiable modern dependency
set around CadQuery 2.4. The Python-3.10-compatible CadQuery 2.7 and its required
VTK 9.3.1 install normally and pass the complete suite. The merge review's two
test-responsibility findings are corrected with shared fixtures and a dedicated
runner-checker test. All nine skill entrypoints validate. The viewer tests and
production build pass without changing its committed static output. Final
independent simplicity and stability reviews pass. The release is hosted at
`https://github.com/PatrickGrothOls/AIkea-skill` on its default `main` branch.
That initial repository is now retained privately as `AIkea-skill-private-history`.
A fresh verified alpha at the original URL remains private pending explicit
publication approval; see `public-alpha-release.md` for the current release.

## Audit log

1. 2026-09-06 - the maintainer requested a new GitHub repository for the skill and
   confirmed the existing private `AIkea` repository is the earlier application.
2. 2026-09-06 - the maintainer chose free personal use with commercial building
   prohibited. The release will use the established PolyForm Noncommercial 1.0.0
   terms and be described as source-available, because commercial restrictions
   are incompatible with the Open Source Definition.
3. 2026-09-06 - The public-release audit found no credential patterns in the
   combined branch history. Two bundled Cabineo cutter STEP assets remain and
   require an explicit provenance caveat in the public documentation.
4. 2026-09-06 - A fresh Python 3.10.16 environment reproduced an import failure
   because CadQuery 2.4 pins `nptyping` to a NumPy 1.x API while current NLopt
   requires NumPy 2.x. Pinning NumPy alone therefore cannot produce a clean
   dependency solve.
5. 2026-09-06 - CadQuery 2.7.0 and its required VTK 9.3.1 install cleanly on
   Python 3.10.16. The complete repository suite passed with 466 tests, 5
   expected skips, and 72 subtests in that isolated environment.
6. 2026-09-06 - Independent review of merge commit `978c5a5` passed stability
   with 141 focused tests and exact feature parity. Simplicity review required
   one duplicated evidence fixture to be shared and runner-only cases to move
   out of the installed-spacer checker test. All reviewed production files over
   150 lines were judged cohesive.
7. 2026-09-06 - The evidence fixture is now shared and runner articulation has
   its own test file. The six affected test/support files are each below 150
   lines, and their focused slice passes 53 tests under CadQuery 2.7.
8. 2026-09-06 - The public release uses the unmodified PolyForm Noncommercial
   1.0.0 terms. The README permits personal and hobby projects, identifies paid
   design/build activity as commercial, and states that separate permission is
   required. It also records the Cabineo cutter provenance boundary and product
   trademark disclaimer.
9. 2026-09-06 - Final simplicity review of `d3dda7f` found one pure test
   forwarding method after confirming the substantive responsibility fixes.
   Its five callers now use the canonical evidence fixture directly.
10. 2026-09-06 - All nine packaged skill entrypoints pass the skill validator.
    The publication environment's complete Python suite passes with 467 tests,
    5 expected skips, and 72 subtests.
11. 2026-09-06 - The viewer passes all 23 tests and its Vite production build.
    Rebuilding produces no tracked changes in the committed static viewer.
12. 2026-09-06 - Independent final review of exact code commit `e655749`
    passed simplicity with 56 focused tests and stability with 116 material and
    KA 4532 tests. Clean Python 3.10 dependency installation, `pip check`, CAD
    imports, exact purchased-spacer hashes, and all eight official fixing axes
    passed. Existing door-panel collisions and the unresolved screw and cabinet
    pilot specification continue to fail closed.
13. 2026-09-06 - Created the separate public `PatrickGrothOls/AIkea-skill`
    repository and published the verified release as `main`. GitHub reports the
    repository as public with `main` as its default branch. The published
    `LICENSE.md` Git blob exactly matches the locally verified PolyForm license.
14. 2026-09-06 - the maintainer requested a private verification gate after the
    initial publication. The repository was changed to private and GitHub
    confirmed the new visibility. Returning it to public now requires the maintainer's
    explicit approval.
15. 2026-09-06 - The reviewed release fixes now have a clean replacement history
    and a verified private alpha tag. The former repository remains private under
    its history name; the replacement awaits explicit public-visibility approval.
