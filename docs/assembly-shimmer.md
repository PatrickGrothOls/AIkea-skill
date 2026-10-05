# Assembly shimmer

## Scope
Replace the live-build torch-like wash with fine luminous glints flowing across
an active assembly. Preserve real build status, arrival buffering, camera controls,
and reduced-motion behaviour. This branch stacks on the existing live-build viewer.

## Work packages
- [x] Replace the broad wash with a spatially continuous sparkling surface effect.
- [x] Accelerate upward sweeps and overlap a trailing wave without per-part resets.
- [x] Verify shared coordinates, phase continuity, failure stop, and reduced motion.
- [x] Build and inspect the browser shader; record and verify an MP4 demo.
- [x] Upload the preview to Google Drive after explicit file/destination approval.
- [x] Review the diff and commit this visual refinement.

## Current state
Implementation complete; 89 viewer tests pass and the production bundle builds.
Browser shader compilation succeeds. Two overlapping quadratic 1.8-second upward
sweeps carry blue-white glints, rippling filaments, and weaker trailing sparkles.
Every part uses the same assembly bounds and absolute clock. Local video and the verified Google Drive upload are ready. Visual acceptance remains Patrick's decision.
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

## Verification
- 89 viewer tests passed, including shared phase for delayed/new parts, acceleration,
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
