# Shared drawer host machining

## Scope and current state

WP5 drawer-host operation slice on `feat/drawer-host-machining`, based on
reviewed exact-hole reuse `7626d80`. Implementation and focused geometry tests
pass; the review skill is complete with no findings.

This slice makes the current KA 5332 host pattern explicit and composes it onto
existing parts using the shared cut executor. The subsequent host-interface slice
removes the remaining assumptions about standard cabinet dimensions and side IDs.
KA 4532 and MOVENTO keep their existing unresolved fixing boundaries.

## Work package and tasks

- [x] Use one cut applicator for a fresh panel and an already constructed panel.
- [x] Preserve earlier parts, cuts, requirements, child assemblies and purchases
  when appending a feature's local operations.
- [x] Save selected-profile host holes and exact reused-operation IDs in the
  installation input, with separate required-work declarations.
- [x] Verify old/new geometry, configured/custom panel behavior, removal,
  required-work coverage and existing drawer revisions.
- [x] Document the supported component boundary and run the review skill.

## Validation

Twenty-four host integration, KA 5332 generator and drilling-reuse tests passed.
They compare the new result with the previous cutter geometry, apply the same
requests to renamed authored panels, retain unrelated earlier drilling, preserve
unassessed parent requirements, and detect omitted host work. The first broader
group passed 26 tests but exposed an empty-intersection CAD boolean failure;
skipping zero-volume intersections fixes that failure, and the affected generator
case passed in the 24-test rerun. Nine skill packages and links verify.
Nine saved-file revision, command and hardware-ownership tests also passed.
The independent reviewer confirmed exact appended-versus-fresh geometry,
preserved child/hardware instances, rejected missing source cuts and rejected
changed saved mounting coordinates paired with stale output. No findings remain;
all changed code files are below 150 lines. Hardware generator probes use test
CAD bounds rather than a new vendor download or physical manufacturing proof.

## Audit log

1. Host mounting previously changed solids in a product-specific builder without
   declaring or retaining the host cuts. The recipe now emits complete drilling
   inputs; a shared feature uses the same applicator as fresh construction.
   Existing geometry is preserved, including legitimate System 32 hole reuse.
2. The feature retains an unassessed (`None`) parent-requirement state. Adding
   mounting requirements cannot imply that all earlier parent obligations were
   assessed. Authored hosts should declare their own requirements before use.
3. Integration exposed an empty-intersection boolean failure in the reuse check.
   The validator now checks intersection volume before subtracting an allowed
   reused region. No overlapping material is excluded by this fix.
