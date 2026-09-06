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
- [x] Commit checkpoint `6d48407` with the Codex agent signature.
- [x] Pass the independent simplicity review on that exact commit.
- [x] Record the stability review failure: its confirmation fixture exposed the
  expected answer and all new material fixtures used the wrong lifecycle shape.
- [x] Move the expected answer outside the copied project and convert every new
  material fixture to the calculator's `cabinet_run` shape.
- [x] Commit fixture correction `fb521ae` with the Codex agent signature.
- [x] Pass its independent stability review.
- [x] Record its simplicity-review failure: tests did not explicitly reject a
  lifecycle regression in every seed or an oracle elsewhere in the fixture tree.
- [x] Lock both corrected boundaries with direct assertions.
- [x] Split fixture-lifecycle checks from inference scoring when the combined
  test file crossed the 150-line separation-of-concerns review threshold.
- [x] Commit regression assertions `fd7e9bc` with the Codex agent signature.
- [x] Pass its independent simplicity review.
- [x] Record its stability-review failure: lexical path ancestry allowed `..`
  to hide an expected answer inside the copied fixture tree.
- [x] Resolve both paths before checking oracle ancestry and reproduce the
  traversal attempt in a regression test.
- [x] Commit normalized-path assertion `428ca07` with the Codex agent signature.
- [x] Pass its independent simplicity review.
- [x] Record its stability-review failure: resolving only the target allowed a
  symlink entry stored inside the copied fixture tree to point outward.
- [x] Check both the normalized entry and resolved target, with a symlink regression test.
- [x] Commit path-boundary assertion `2ea9c39` with the Codex agent signature.
- [x] Pass its independent simplicity review.
- [x] Record its stability-review failure: case-insensitive macOS paths allowed
  uppercase `FIXTURES` to alias the copied lowercase directory.
- [x] Replace fixture exclusion with a strict lowercase `expected/` allow-list
  and require the resolved target to remain inside it.
- [x] Commit allow-list boundary `8e5b58f` with the Codex agent signature.
- [x] Record both independent review failures: the allow-list root itself could
  be a symlink into copied fixtures.
- [x] Require `evals/expected` to resolve to its own real directory entry and
  reproduce the root-alias attack in a regression test.
- [x] Commit isolated-root assertion `a16e989` with the Codex agent signature.
- [x] Pass independent code simplicity and stability reviews on that exact commit.

## Current state

Implementation and verification are complete. The advisor
now has a replayable thirteen-case inference eval, an explicit drawer-material
boundary, safe handling for generated legacy projects, and a deterministic gate
requiring the three globally supported material decisions. Both skills validate,
32 focused and compatibility tests pass. The unrestricted full suite passes with
409 tests, 5 expected skips, and 72 subtests, including the localhost viewer tests.
Independent review of exact commit `a16e989` passed simplicity and stability.
The immutable-archive stability run passed 44 focused checks, rejected every
requested traversal, case-alias, and symlink attack, and confirmed the expected
YAML remains valid in the real calculator.

## Audit log

1. 2026-09-05 - the maintainer approved a separate advisory skill covering price,
   quality, aesthetics, and images.
2. 2026-09-05 - the maintainer required questions that clients can answer. Technical
   properties are inferred from ordinary descriptions instead of requested from
   the client.
3. 2026-09-05 - the maintainer required an eval set that verifies those inferences. The
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
8. 2026-09-05 - the maintainer identified that commit `53364a7` came from a message sent
   to the wrong task and approved retaining its useful discovery, routing, gate,
   and test work in this plan.
9. 2026-09-05 - the maintainer approved continuing with the listed closure work. The
   supported global groups are therefore enforced before calculation; generated
   legacy projects stop for migration; drawer-front materials remain owned by
   the drawer builder because the global schema has no drawer-material field.
10. 2026-09-05 - The material eval was made replayable with concrete isolated
    project fixtures, evidence, an actual image, stable case IDs, and exact file
    outcomes. A thirteenth case covers the generated legacy-project deadlock.
11. 2026-09-05 - The final unrestricted verification passed 409 tests, 5
    expected skips, and 72 subtests, including the localhost viewer checks.
12. 2026-09-05 - Independent review of signed commit `6d48407` passed
    simplicity and failed stability because the confirmation seed copied its
    expected answer and every new material fixture used post-arrangement
    `assembly_run` fields before arrangement occurred.
13. 2026-09-05 - The expected answer moved outside every copied fixture. The
    fixtures now use the valid pre-arrangement `cabinet_run` shape, and tests
    enforce both isolation and calculator validity.
14. 2026-09-05 - The corrected unrestricted suite passed 409 tests, 5 expected
    skips, and 72 subtests, including the localhost viewer checks.
15. 2026-09-05 - Independent review of signed commit `fb521ae` passed stability
    and failed simplicity because its tests did not directly reject lifecycle
    regressions in every seed or oracle placement elsewhere in the fixture tree.
16. 2026-09-05 - The eval contract now asserts `cabinet_run` and rejects
    `assembly_run` in every starting fixture, and keeps every expected answer
    outside the entire copied material-fixture tree.
17. 2026-09-05 - Adding those assertions pushed the combined eval test over the
    150-line review threshold. Fixture and lifecycle checks were extracted into
    their own focused test file; inference scoring remains separate.
18. 2026-09-06 - Independent review of signed commit `fd7e9bc` passed
    simplicity and failed stability because an expected path containing `..`
    could bypass the lexical fixture-tree comparison.
19. 2026-09-06 - The fixture root and expected path are now resolved before
    ancestry comparison. A direct `expected/../fixtures/...` regression case
    proves the boundary rejects traversal into copied fixtures.
20. 2026-09-06 - Independent review of signed commit `428ca07` passed
    simplicity and failed stability because a symlink entry inside the copied
    fixture tree could point to the external expected file.
21. 2026-09-06 - The oracle boundary now checks both the normalized entry path
    and resolved target path. A direct symlink-entry regression case protects
    the copy boundary.
22. 2026-09-06 - Independent review of signed commit `2ea9c39` passed
    simplicity and failed stability because case-insensitive APFS allowed an
    uppercase fixture alias to evade path equality.
23. 2026-09-06 - The boundary now allows only explicit lowercase `expected/`
    paths without parent traversal and requires their resolved targets to remain
    inside that directory. Case aliases and outward symlinks have direct tests.
24. 2026-09-06 - Independent review of signed commit `8e5b58f` failed both
    simplicity and stability because the `expected` allow-list root could itself
    be a symlink into copied fixtures.
25. 2026-09-06 - The allow-list root must now resolve to its own real directory
    entry. A direct root-alias regression case protects that requirement.
26. 2026-09-06 - Independent code reviews of signed commit `a16e989` passed
    simplicity and stability. The stability review passed 44 focused checks,
    rejected the requested path attacks, and validated the expected YAML with
    the real calculator.
