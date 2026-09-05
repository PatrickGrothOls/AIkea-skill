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

- [x] Add realistic natural-language cases with hidden required and forbidden inferences.
- [x] Cover dry use, water exposure, shelf load, appearance, wear, handling, price, images, and confirmation.
- [x] Add structural tests for inference keys, scoring rules, and coverage.
- [x] Run skill validation and the focused automated tests.

### WP4 - Repository verification

- [x] Run skill-package validation and the focused material tests.
- [x] Run the complete Python suite with the repository's pinned Python 3.10 and
  CadQuery environment: 454 tests and 72 subtests passed; 5 tests were skipped.
- [x] Run the localhost review-server tests with socket permission.

## Current state

The advisor, main-skill route, material-selection reference, deterministic
unresolved-material gate, and twelve-case inference eval set are complete. Skill
validation and all 26 focused tests pass. The complete repository suite passes
with 454 tests, 5 expected skips, and 72 subtests.

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
7. 2026-09-05 - The complete Python suite passed with 454 tests, 5 expected
   skips, and 72 subtests.
