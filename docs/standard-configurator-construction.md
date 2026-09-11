# Standard cabinet recipe through shared construction

## Scope

WP3 of [the foundation plan](shared-construction-foundation.md), on
`feat/standard-configurator-construction`, based on WP2 at `9ab790f`.
Migrate the tall-storage recipe while retaining its measured dimensions and
cabinet metadata needed by existing door/drawer consumers. Base migration remains
WP5. The common executor consumes explicit parts, joints and local machining.

## Current state

Implementation, focused verification and independent review pass. The full Python
regression is clear after rerunning the local HTTP tests with socket permission.
No fabrication claim; later work packages remain open.

## Work package and tasks

- [x] Inspect configurator generation, feature consumers and regeneration.
- [x] Emit explicit System 32 requests in the editable cabinet specification.
- [x] Route new cabinet and individual-part builds through the shared executor.
- [x] Keep explicit unresolved joint declarations in previews; reject other
  unsupported requests and preserve participant validation.
- [x] Preserve recipe metadata and safe regeneration of generated files.
- [x] Demonstrate configured/custom geometry, machining and inventory parity.
- [x] Demonstrate an authored customization without a new purpose or cutter.
- [x] Run focused regression checks and the `review` skill, fix and recheck findings.
- [x] Record evidence and commit this coherent slice.
- [x] Complete the wider Python regression before landing the stack.

## Audit log

1. Patrick authorized the foundation plan and required review after every work
   package. This slice follows WP3; it introduces no new construction policy.
2. Existing door geometry reads cabinet dimensions from `built.spec`. Retain
   those fields while making configured and custom specifications satisfy the
   same structural construction interface. Do not duplicate dimensions into a
   separate tree or hide them inside an opaque recipe result.
3. The current recipe deliberately declares an unresolved door attachment.
   Explicit preview allowance must retain that declaration and all ownership
   checks; unsupported named tools must still fail. Fabrication checks continue
   to report the unresolved attachment. This preserves preview capability.
4. Saved generated-file hashes already protect authored edits. Use that existing
   conflict mechanism, and retain legacy per-part construction only for base and
   saved builders until their separate migration and compatibility checks pass.
5. Primary review found stale descriptions of per-part execution and grid order
   in two existing references. Updated them to match the shared execution path.
6. The existing taxonomy-generator test is 161 lines. The required independent
   separation review found its generated-output, boundary and regeneration cases
   coherent; no split is warranted for this assertion-only change. Detailed
   revision/upgrade scenarios already have separate files. The repeated fixture
   transformation is a future extraction candidate if that setup changes again.

## Verification and review

- Initial migration regression: **24 passed, 10 subtests passed** (generator,
  flat/Cabineo geometry, revision/upgrade, physical inventory and drawer integration).
- New shared/custom/legacy solid comparison, equal inventory, notched shelf and
  explicit-preview tests: **6 passed**. An initial test expectation omitted the
  fixture's 2 mm fit allowance; corrected the expectation after checking its input.
- Independent specialist: five generation/revision/door-lighting tests passed;
  the sloped four-cabinet case rebuilt all six miters; direct generated part access
  matched the complete cabinet's specification and volume. No findings.
- Packaged skill/link verification passed (nine skills). Primary review covers
  the whole WP diff against `9ab790f`; prior slices remain separate checkpoints.
- Full Python run: 556 passed, 72 subtests passed, five skipped; five HTTP tests
  failed solely because the sandbox prevented binding `127.0.0.1`. Re-running
  both affected files with local socket permission passed all six tests (one
  overlaps the full run): **561 unique tests passed, 72 subtests passed, five
  skipped**. No production changes were needed. Dependency checks also pass.
- `review` completed, logged against `76ce13a`, with the documentation correction
  above and no outstanding findings. This is local verification, not remote CI
  or a fresh model-led furniture acceptance run (WP7).
