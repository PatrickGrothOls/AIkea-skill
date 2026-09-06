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

- [ ] Add the unmodified PolyForm Noncommercial License 1.0.0.
- [ ] State clearly that personal and noncommercial use is permitted.
- [ ] State clearly that commercial use requires separate permission.
- [ ] Avoid describing the noncommercial release as OSI open source.
- [ ] Record the provenance caveat for bundled Cabineo cutter assets.

### WP3 - Verification

- [ ] Validate every packaged AIkea skill entrypoint.
- [ ] Run the complete Python suite.
- [ ] Run the viewer test and production build.
- [ ] Independently review combined code simplicity and stability.

### WP4 - Publication

- [ ] Create `PatrickGrothOls/AIkea-skill` as a public repository.
- [ ] Publish the verified release as the default `main` branch.
- [ ] Verify visibility, license text, default branch, and remote HEAD.

## Current state

The material-advice and latest KA 4532 spacer branches are integrated without
merge conflicts. Clean installation exposed an unsatisfiable modern dependency
set around CadQuery 2.4. The Python-3.10-compatible CadQuery 2.7 and its required
VTK 9.3.1 install normally and pass the complete suite. No GitHub repository has
been created or changed yet.

## Audit log

1. 2026-09-06 - Patrick requested a new GitHub repository for the skill and
   confirmed the existing private `AIkea` repository is the earlier application.
2. 2026-09-06 - Patrick chose free personal use with commercial building
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
