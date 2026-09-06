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
- [x] Move viewer source outside `aikea-review-unit/`.
- [x] Keep the compiled viewer under `aikea-review-unit/assets/viewer/`.

### WP2 - Reproducible contributor build

- [x] Update the viewer build to write the verified bundle into the skill asset.
- [x] Add a dependency lockfile and pinned Node version.
- [x] Update repository tests and ignore rules for the new source location.

### WP3 - Verification

- [x] Install the locked viewer dependencies.
- [x] Run the viewer source tests.
- [x] Rebuild the compiled viewer asset.
- [x] Run the repository checks that protect viewer interaction.
- [x] Validate the installable review skill.

## Contributor workflow

Run these commands from the repository root:

```sh
direnv exec . npm --prefix viewer ci
direnv exec . npm --prefix viewer test
direnv exec . npm --prefix viewer run build
```

The build replaces `aikea-review-unit/assets/viewer/` with the compiled static
application that is distributed with the skill.

## Current state

The packaging boundary is implemented. Users install and run the compiled
interactive viewer without Node.js. Open-source contributors work in the top-level
`viewer/` project with an exact Node.js version, npm version, and dependency
lockfile. Its production build writes directly to the skill's viewer asset. All
viewer source tests, packaging-contract tests, dependency checks, and skill
validation pass.

## Audit log

1. 2026-08-31 - the maintainer confirmed that Node.js dependencies, their lockfile, and
   the editable viewer source are repository-only contributor resources. This
   keeps the installed skill smaller and avoids imposing frontend tooling on a
   user who only needs to generate and inspect furniture, while retaining a
   reproducible open-source path for improving the viewer.
2. 2026-08-31 - Moved the editable application to `viewer/` and made its Vite
   output target the compiled skill asset. Updated path-sensitive tests and ignore
   rules to enforce that separation.
3. 2026-08-31 - Pinned Node.js 24.4.1, npm 11.4.2, and the complete dependency
   graph. Updated Vite to 8.2.2 after the registry audit identified a vulnerability
   in 8.0.9; the final audit reports zero known vulnerabilities.
4. 2026-08-31 - Rebuilt the installed viewer and verified 22 viewer tests, 10
   packaging-contract tests, and the skill package validator.
