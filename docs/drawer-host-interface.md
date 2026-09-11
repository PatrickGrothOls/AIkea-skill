# Explicit drawer host interface

## Scope and current state

WP5b host-input slice on `feat/drawer-host-interface`, based on reviewed host
machining `a0ed283`. Implementation, focused regressions and the review skill
pass. All runner recipes now read
one bay contract: actual owned support panels plus front, depth, floor and ceiling.
The standard cabinet adapter supplies that contract from existing metadata.

This supports opposing upright sheet faces in the local parent frame. A parent
can itself be placed in a larger custom arrangement. This does not claim arbitrary
tilted runner installations or certify drawer load capacity.
The following proof slice will update the remaining KA 4532 proof helpers that
still assume canonical host names/front planes. Such custom proof remains
explicitly unresolved until then; the existing fail-closed check is retained.

## Work package and tasks

- [x] Define the explicit bay and resolve its real inside faces from part frames.
- [x] Let saved custom parents export `DRAWER_HOST` next to `SPEC`; retain the
  standard-cabinet adapter for existing callers.
- [x] Route drawer sizing, fit, runner placement and mounting cuts through those
  inputs while retaining exact selected hardware and unresolved fixing policy.
- [x] Express reservations in each actual support panel's canonical coordinates.
- [x] Prove configured/custom equivalence, translated bays, renamed supports,
  changed panel origins, invalid hosts and retained physical inventory.
- [x] Update skill examples and run the review skill; fix and recheck findings.

## Validation

- 13 tests passed across the host interface, saved-file revision protection and
  KA 4532/MOVENTO generators.
- 24 tests passed across the host interface, KA 5332 System 32 rows, KA 4532
  mounting/reservations/planning, MOVENTO placement and host machining.
- Seven drawer geometry and KA 4532 fixing-alignment regressions passed.
- All nine skill packages and their links validate; `git diff --check` passes.
- Independent review flipped both support frames to equivalent `<Z` inside
  faces. All three recipes retained identical drawer origins; each KA 5332
  owner-space cutter matched independently constructed cylinders with zero
  symmetric difference, and the shared result validator accepted the build.
- The reviewer independently verified that a different authored complete builder
  blocks generation before any project file changes. Full diff/caller review and
  testing-specialist review found no actionable issues in this slice.
- The inherited 156-line planner received a separate
  [responsibility review](reviews/drawer-host-interface-scope.md). It remains a
  coherent coordinator; no extraction was required.

These are local software/geometry checks, not physical fabrication or load proof.

## Audit log

1. A custom design declares real mounting participants and free space rather than
   inventing standard-cabinet width, shelf-role or top-profile metadata. This is
   the approved optional-configurator interface, not a new furniture engine.
2. KA 5332 row selection uses shared physical heights, then maps each row back
   to its support panel. Drilling is derived from the mounted world axes and
   transformed to each panel, preserving both hands and differing panel origins.
3. KA 4532 previously saved reservation heights in the parent frame while other
   fittings use panel coordinates. The host-aware path now maps those envelopes
   to the actual support frames; this makes interference checks comparable.
4. A fresh custom parent initially built only its base because it lacked the
   standard manifest entry point. Each drawer file set now supplies the shared
   complete builder under the existing generated-file conflict protections.
5. Closed this slice after local regression and independent review. The next
   branch covers KA 4532 proof inputs; no physical fixing blocker was resolved.
