# Retire duplicate panel construction

## Scope and current state

Branch `refactor/legacy-panel-adapters`. The old PartBlankBuilder and
SheetPartBuilder APIs remain available to saved projects, but now translate their
inputs into the common blank, machining and subtraction tools. A test-only copy
of the historical implementation remains an independent geometry oracle.
Implementation, focused compatibility checks and independent review are complete.
The full candidate regression remains part of WP7.

## Work package and tasks

- [x] Confirm active generated builders use shared construction directly.
- [x] Confine old role/dimension conventions to a compatibility input adapter.
- [x] Remove duplicate production blank selection/subtraction implementations.
- [x] Retain an independent historical test oracle for geometry parity.
- [x] Verify saved per-part construction, configured/custom parity and failure behavior.
- [x] Complete the review skill, including independent compatibility checks.
- [ ] Run the final whole-candidate regression as part of WP7.

## Audit log

1. No current generated builder uses the old per-part engine. Existing public
   imports remain necessary for saved projects and geometry regression fixtures.
   Replacing those APIs with common-tool adapters removes the second engine
   without deleting the compatibility boundary or silently removing old grids.
2. Move the old construction code to tests only so parity tests remain independent
   after the production entry points delegate to the shared implementation.

## Validation

- Six existing parity/geometry files: 22 tests and 62 subtests passed.
- Three edge checks passed: old sloped doors require no new local-size field;
  a saved cutter that misses its participant fails the common material check.
- Independent review: no findings. Eight geometric probes cover all seven roles,
  both System32 faces, an offset/sloped back and a placed cut; symmetric difference
  is zero throughout. The test oracle is AST-identical to the old production
  classes after class renaming.
- Active configurators and skills have no fallback to the old per-part APIs.
  Compatibility imports remain only for saved callers and regression fixtures.
- `git diff --check` passed. No fabrication approval is inferred.

3. 2026-09-12 — Closed the review skill before starting the separate cold-start
   integration fixes. The legacy entry points preserve old input interpretation
   while their blank, grid and subtraction execution uses the common tools.
