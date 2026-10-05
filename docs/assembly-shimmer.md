# Assembly shimmer

## Scope
Replace the live-build torch-like wash with continuous energy ribbons flowing
through an active assembly; discrete sparkles were rejected after visual review. Preserve real build status, arrival buffering, camera controls,
and reduced-motion behaviour. This branch stacks on the existing live-build viewer.

## Work packages
- [x] Replace rejected discrete glints with continuous flowing ribbons.
- [x] Verify and record the revised energy effect for Patrick.
- [x] Replace the broad wash with a spatially continuous sparkling surface effect.
- [x] Accelerate upward sweeps and overlap a trailing wave without per-part resets.
- [x] Verify shared coordinates, phase continuity, failure stop, and reduced motion.
- [x] Build and inspect the browser shader; record and verify an MP4 demo.
- [x] Upload the preview to Google Drive after explicit file/destination approval.
- [x] Review the diff and commit this visual refinement.

## Current state
Revised energy effect implemented and recorded. Continuous bending ribbons replace
all discrete sparkles. Bright crests and soft trailing folds flow through the
assembly on the existing accelerating shared clock. 89 viewer tests pass, the
bundle builds, and the browser reports no shader errors. The new video was uploaded
to Google Drive and its metadata verified. Patrick's visual acceptance is pending.
No push, merge, deployment, or fabrication approval was performed.

## Audit log
1. Patrick requested fairy-tale/electric glistening instead of illumination from a
   bulb, faster movement, one continuous flow through the assembly, and acceleration.
   His final upward-flow description guides the dominant direction; trailing glints
   supply secondary movement without a full downward scan.
2. Research supports easing, overlap, and follow-through as ways to give motion life.
   Applying those principles to an accelerating sweep and smaller trailing glints
   is a design interpretation of Patrick's request, subject to his visual review.
   References: [Adobe animation principles](https://www.adobe.com/creativecloud/animation/discover/principles-of-animation.html)
   and [Disney animation](https://www.disneyanimation.com/process/animation/).

3. Visual inspection of the first shader showed a pause between passes. Overlapping
   half-cycle waves removes that gap while preserving the requested upward direction.
4. Removed an unused legacy width uniform; signed falloffs use multiplication rather
   than GLSL pow on negative inputs, whose behaviour is undefined.
5. Automatic approval review blocked the Drive upload of the CAD-derived preview:
   explicit authorization for the video and destination is required. No alternate upload path was attempted before authorization.

6. Patrick explicitly approved the preview upload and future private recording uploads
   to his Google Drive. Upload completed and file metadata was read back successfully.

7. Patrick rejected the separate bright points: the intended effect is energy
   passing through the furniture, not pixels or a torch. Replace the sampled star
   field with continuous bending ribbons and soft trailing folds; no Blender change
   is needed for this browser shader. Visual approval remains outstanding.

8. Verified the continuous-ribbon revision in the actual browser and removed the
   recorder's initial 1.5-second blank startup. The remaining source captured
   29.75 fps with a 93.37 ms maximum gap and no gaps over 100 ms. The H.264 delivery
   file normalizes that verified cadence to 30 fps and decodes cleanly. Uploaded
   privately under Patrick's standing authorization and verified Drive metadata.

## Verification
- Revised ribbon shader: 89 viewer tests passed and production bundle rebuilt.
- Initial glint version: 89 viewer tests passed, including shared phase for delayed/new parts, acceleration,
  off-model wrap, reduced motion, and existing failure/assembly isolation checks.
- Production bundle built; existing large-chunk warning remains. No shader errors
  observed; the pre-existing Three.Clock deprecation warning remains.
- Recorded the actual browser canvas using the screen-recording skill. The synthetic
  seven-panel CAD study demonstrates the effect only; it is not a fresh build or a
  validation pass. 361 captured frames over about 12 seconds; the active 10-second
  interval measured 30.00 fps, 33.3 ms median and 55.57 ms maximum frame gap.
- Inspected sampled frames across the entire clip. H.264/yuv420p delivery normalizes
  the already-verified capture timestamps to 30 fps and decodes without errors.
- Responsibility review: the shimmer class owns spatial shading and phase;
  the surface class retains arrivals/material lifetime. No edited handwritten
  file exceeds 150 lines. Generated viewer bundles remain generated artifacts.
