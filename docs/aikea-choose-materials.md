# AIkea material advice

## Scope

Add a reusable AIkea material-advice stage. It must let ordinary clients describe
their life, desired appearance, and budget; infer the technical material demands;
show honest visual references; compare current purchasable systems; and save only
an explicitly approved project choice.

This branch does not change the `aikea.yaml` schema or implement downstream
per-part material assignment.

## Plan

### WP1 - Advisory boundary

- [x] Create the dedicated `aikea-choose-materials` skill.
- [x] Route material and isolated-thickness questions from the main AIkea skill.
- [x] Keep geometry, construction, and fabrication ownership outside the advisor.

### WP2 - Client inference and visuals

- [x] Ask only ordinary, answerable questions one topic at a time.
- [x] Infer service, load, wear, finish, handling, and cost requirements internally.
- [x] Use sourced images for appearance choices without treating images as technical proof.
- [x] Require a physical sample before visible-material approval.

### WP3 - Evaluation

- [x] Add thirteen stable natural-language cases with hidden required and forbidden inferences.
- [x] Cover dry use, water exposure, shelf load, appearance, wear, handling,
  price, hostile sources, images, confirmation, revision, and legacy migration.
- [x] Provide concrete project fixtures, evidence files, an actual image
  attachment, and an exact expected YAML for the mutating case.
- [x] Document an isolated fresh-chat run and exact file scoring.
- [x] Lock case identities, fixture paths, attachments, and expected values in tests.

### WP4 - Repository verification

- [x] Validate the main and material-advice skill packages.
- [x] Pass all 32 focused material, routing, and compatibility tests.
- [x] Correct the three legacy eval fixtures exposed by the first full-suite run.
- [x] Rerun the complete Python suite: 409 tests and 72 subtests passed; 5 skipped.
- [x] Run the localhost review-server tests with socket permission as part of that suite.

### WP5 - Review closure

- [x] Retain inherited commit `53364a7` as the discovery, routing, and
  unresolved-material checkpoint.
- [x] Require exactly one confirmed decision for each supported global material group.
- [x] Stop generated legacy projects at a material-migration blocker instead of looping.
- [x] Keep drawer-box and drawer-front material ownership with `$aikea-build-drawers`.
- [ ] Commit the corrective checkpoint with the Codex agent signature.
- [ ] Run independent simplicity and stability reviews on the exact commit.

## Current state

Implementation is complete but final verification is still running. The advisor
now has a replayable thirteen-case inference eval, an explicit drawer-material
boundary, safe handling for generated legacy projects, and a deterministic gate
requiring the three globally supported material decisions. Both skills validate,
32 focused and compatibility tests pass. The unrestricted full suite passes with
409 tests, 5 expected skips, and 72 subtests, including the localhost viewer tests.

## Audit log

1. 2026-09-05 - Patrick approved a separate advisory skill covering price,
   quality, aesthetics, and images.
2. 2026-09-05 - Patrick required questions that clients can answer. Technical
   properties are inferred from ordinary descriptions instead of requested from
   the client.
3. 2026-09-05 - Patrick required an eval set that verifies those inferences. The
   cases therefore contain hidden required and forbidden inference keys, not only
   preferred response wording.
4. 2026-09-05 - The material advisor and routing contract passed package
   validation and four focused automated tests.
5. 2026-09-05 - Review identified a need for one thickness authority, safe
   handling of legacy and already built projects, explicit exceptional-part
   blockers, less duplicated routing, and an untrusted-data boundary for external
   sources. Those safeguards are now included.
6. 2026-09-05 - A second review required the exceptional-part blocker to fail
   deterministically, material validation to precede completeness, and project
   file creation to cover fully supplied new projects. The calculator gate,
   routing order, and recovery-case tests now enforce those boundaries.
7. 2026-09-05 - The complete Python suite passed with 402 tests, 5 expected
   skips, and 72 subtests.
8. 2026-09-05 - Patrick identified that commit `53364a7` came from a message sent
   to the wrong task and approved retaining its useful discovery, routing, gate,
   and test work in this plan.
9. 2026-09-05 - Patrick approved continuing with the listed closure work. The
   supported global groups are therefore enforced before calculation; generated
   legacy projects stop for migration; drawer-front materials remain owned by
   the drawer builder because the global schema has no drawer-material field.
10. 2026-09-05 - The material eval was made replayable with concrete isolated
    project fixtures, evidence, an actual image, stable case IDs, and exact file
    outcomes. A thirteenth case covers the generated legacy-project deadlock.
11. 2026-09-05 - The final unrestricted verification passed 409 tests, 5
    expected skips, and 72 subtests, including the localhost viewer checks.
