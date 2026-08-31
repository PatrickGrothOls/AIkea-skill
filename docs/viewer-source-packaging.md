# Viewer source packaging

## Scope

Keep the interactive review viewer available inside every installed AIkea skill
without making Node.js or frontend source code part of the skill runtime. Keep the
editable React and Three.js project in this repository so contributors can test,
rebuild, and improve it as normal open-source software.

## Workpackages and tasks

### WP1 - Packaging boundary

- [x] Confirm that installed skills receive the compiled interactive viewer.
- [x] Confirm that viewer source and Node tooling belong only to the repository.
- [ ] Move viewer source outside `aikea-review-unit/`.
- [ ] Keep the compiled viewer under `aikea-review-unit/assets/viewer/`.

### WP2 - Reproducible contributor build

- [ ] Update the viewer build to write the verified bundle into the skill asset.
- [ ] Add a dependency lockfile and pinned Node version.
- [ ] Update repository tests and ignore rules for the new source location.

### WP3 - Verification

- [ ] Install the locked viewer dependencies.
- [ ] Run the viewer source tests.
- [ ] Rebuild the compiled viewer asset.
- [ ] Run the repository checks that protect viewer interaction.
- [ ] Validate the installable review skill.

## Current state

Patrick approved the boundary: users install and run the already-compiled
interactive viewer without Node.js, while open-source contributors receive the
separate viewer project and its development tooling from this repository. The
existing source still lives inside the skill folder and must now be moved without
changing the compiled viewer's runtime behavior.

## Audit log

1. 2026-08-31 - Patrick confirmed that Node.js dependencies, their lockfile, and
   the editable viewer source are repository-only contributor resources. This
   keeps the installed skill smaller and avoids imposing frontend tooling on a
   user who only needs to generate and inspect furniture, while retaining a
   reproducible open-source path for improving the viewer.
