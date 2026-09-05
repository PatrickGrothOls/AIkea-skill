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

- [x] Run the complete Python suite in the available Python 3.11 CadQuery
  environment: 397 tests passed and 5 were skipped.
- [x] Rerun the localhost review-server tests with socket permission after the
  sandbox blocked their first attempt.
- [ ] Confirm a clean requirements install. The existing dependency graph selects
  NumPy 2 for `nptyping==2.0.1`, which still imports the removed `numpy.bool8`;
  changing the CAD dependency stack is outside this material-advice feature.

## Current state

The advisor, main-skill route, material-selection reference, and twelve-case
inference eval set are present. Skill validation and all five focused tests pass.
The complete repository suite passed after its localhost-only tests received the
required socket permission. A reproducible clean dependency installation remains
an existing repository-level blocker.

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
6. 2026-09-05 - The complete suite produced 392 passes, 5 expected skips, and
   5 sandbox-only localhost binding failures. All 6 tests in the affected viewer
   files passed with socket permission, giving 397 effective passes and 5 skips.
7. 2026-09-05 - A fresh dependency install exposed an existing incompatibility:
   `nptyping==2.0.1` requires a NumPy 1 API while current `nlopt` requires NumPy
   2. No dependency change is included in this feature branch.
