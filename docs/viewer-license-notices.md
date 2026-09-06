# Viewer license notices

## Scope

Include the copyright and permission notices for the dependencies actually
bundled into the public viewer, and regenerate them with each production build.

## Workpackages and tasks

### WP1 - Packaging

- [x] Confirm the installed Vite version can collect bundled dependency licenses.
- [x] Enable the built-in license output and link it from the attribution file.
- [x] Build the packaged viewer and inspect the generated notice coverage.

### WP2 - Verification

- [x] Run viewer tests and confirm JavaScript output is unchanged.
- [x] Review the diff for this standalone packaging checkpoint.

## Current state

The production build emits 22 bundled-package license entries. A static
supplement preserves the exact React Three Fiber release notice and documents
the MIT declarations in maath releases that omit standalone license files.
The attribution file now distinguishes the actual upstream licenses. All 23
viewer tests pass; generated JavaScript and CSS bytes remain unchanged.

## Audit log

1. 2026-09-06 - The user authorized execution of the public-release review fixes.
   This branch handles only the viewer's third-party license packaging.
2. 2026-09-06 - The installed Vite 8.2.2 implementation and official build-options
   documentation confirm that `build.license` generates notices for bundled
   dependencies. Using that maintained facility keeps collection tied to the
   actual build and avoids a second dependency-discovery implementation.
3. 2026-09-06 - Package inspection found that the old all-MIT attribution was
   inaccurate and two archives omit license text. The supplement records its
   sources explicitly and does not substitute a later maath author's copyright
   notice for earlier releases. No runtime dependencies were changed.
4. 2026-09-06 - The generated notice file preserves upstream CRLF text. Its
   file-specific whitespace attribute permits those line endings without
   rewriting third-party notices or changing the viewer output.
