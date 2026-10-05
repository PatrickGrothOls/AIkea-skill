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
- [x] Refine shimmer to upward-only glints and buffer GPU-ready, eased part arrivals.
- [x] Verify refined motion in the browser and run the updated viewer suite.

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
4. Patrick requested a stronger upward-only shimmer and accepted buffering in
   exchange for smoother presentation. Revisions wait 450 ms; new materials compile
   before reveal, then fade over 950 ms with a bounded 80 ms part stagger. Automatic
   framing eases toward growing bounds and stops immediately on user interaction.
5. The first phone demo captured 136 screenshots over about 26 seconds (roughly
   5 fps). Its 30 fps encoding repeated frames, so that recording cannot establish
   the viewer's actual animation frame rate. Camera snapping was also present in
   the implementation and is addressed directly; no 60 fps claim is made.
6. Buffering finishes in-flight asset preparation and keeps only the latest queued
   revision. This prevents frequent updates from repeatedly cancelling slow loads.
   Build/check/failure status remains immediate while geometry catches up.

## Verification and review

- 36 targeted Python tests and four subtests passed, covering live CAD publication,
  nested placement, stable asset hashes, removal reconciliation, failed edits,
  local HTTP boundaries, existing panel builders, generated wardrobes and packaging.
- Viewer suite passed (83 tests), including the native-fetch receiver regression.
- Motion refinement: 88 viewer tests passed, covering monotonic upward travel,
  off-model wrapping, delayed fades, camera interruption, pre-reveal preparation,
  failure retention, slow-load coalescing and disposal. Production bundle rebuilt.
  The actual synthetic rebuild showed glints on the model with no browser errors;
  its intentional fabrication warning remains. Smooth frame rate on Patrick's
  phone has not been measured. The former low-frame-rate recording is unchanged.
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
