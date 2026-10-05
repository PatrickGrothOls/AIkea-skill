# Live construction preview

## Scope

Prioritise the user-approved live building experience over the broader skill
restructure: open early, publish actual completed parts, preserve the camera,
fade new geometry and shimmer only while building or checking. Final review and
fabrication approval retain their existing immutable evidence contracts.

## Work packages

- [x] Publish placed parts from the shared panel builder and generated child frames.
- [x] Watch saved construction inputs; retain geometry and report failed builds.
- [x] Serve a local, read-only live preview with immutable part assets.
- [x] Animate arrivals and active assembly work; support reduced motion.
- [x] Document the early-viewer workflow and custom-builder integration.
- [x] Test actual CAD events, updates, failures and the browser experience.
- [x] Review the final diff and prepare the coherent implementation for commit.

## Current state

Implementation and verification complete; prepared for branch review. No deployment or fabrication
approval changes. The existing final-review viewer remains separate from the
draft preview. Older/custom builders without hooks update at the complete-tree
checkpoint; current panels stream individually. Feature modifications and bought
hardware reconcile at the complete-tree checkpoint.

## Audit log

1. Patrick prioritised live building over restructuring the other skills.
2. Patrick requested updates after each part and a shimmer on the assembly being
   built or checked. The implementation uses real completion events, not a timed
   replay of an already completed cabinet.
3. Preserve the formal review boundary: the live preview is explicitly unfinished
   work and has no approval or ordering endpoint. This follows the existing plan.

## Verification and review

- 36 targeted Python tests and four subtests passed, covering live CAD publication,
  nested placement, stable asset hashes, removal reconciliation, failed edits,
  local HTTP boundaries, existing panel builders, generated wardrobes and packaging.
- Viewer suite passed (83 tests), including the native-fetch receiver regression.
- Production viewer bundle builds with locked dependencies. The pre-existing large
  JavaScript chunk warning remains; no dependency versions changed.
- Browser verification used an explicitly synthetic seven-panel cabinet. Saving an
  added shelf changed the visible model from six to seven parts without navigation;
  orbit worked and the view persisted. Shimmer was visible during real build events
  and stopped at failed checks. Stopping the process retained geometry and displayed
  disconnection. Expanded check details identify unassessed construction/materials.
- Synthetic delays existed only in the temporary test project, never shipped code.
- Reviewed responsibilities: observer hooks, placement, atomic asset publication,
  read-only transport, source watcher, revision feed, scene lifetime, surface effect
  and React presentation have separate scopes. Handwritten changed code stays below
  150 lines per file. Bundled minified outputs are generated, not refactor targets.
- Idle rendering stops after arrival animation; orbit/build animation wakes it.
  Source polling is local and serial. Final approval/upload endpoints are absent.
- Existing projects are not rewritten automatically. Their old/custom builders
  require the documented observation hooks for genuine part-level streaming.
