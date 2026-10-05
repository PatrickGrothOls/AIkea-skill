# Assembly shimmer

## Scope
Replace the live-build torch-like wash with continuous energy ribbons flowing
through an active assembly; discrete sparkles were rejected after visual review. Preserve real build status, arrival buffering, camera controls,
and reduced-motion behaviour. This branch stacks on the existing live-build viewer.

## Work packages
- [x] Extend the halo downward with a long fade; verify and record it.
- [x] Widen the approved white band and fading halo; verify and record it.
- [x] Straighten the energy line and add a white halo, preserving approved motion.
- [x] Verify and deliver a recording of the straight-line revision.
- [x] Replace rejected discrete glints with continuous flowing ribbons.
- [x] Verify and record the revised energy effect for Patrick.
- [x] Replace the broad wash with a spatially continuous sparkling surface effect.
- [x] Accelerate upward sweeps and overlap a trailing wave without per-part resets.
- [x] Verify shared coordinates, phase continuity, failure stop, and reduced motion.
- [x] Build and inspect the browser shader; record and verify an MP4 demo.
- [x] Upload the preview to Google Drive after explicit file/destination approval.
- [x] Review the diff and commit this visual refinement.

## Current state
Patrick requested a longer downward-fading halo, approximately five times the
height of the bright band, and clarified that it should not become brighter.
The core, emission weights, colour, and motion remain unchanged. The trailing
halo falloff is 0.140 of assembly height (five times the core's 0.028 nominal
full width); a faint 0.180 aura softens the end. The leading edge stays narrow.
All 89 tests pass and the production bundle builds. Browser inspection confirms
the downward fade with no shader errors; a new 720p recording is ready.
Visual acceptance remains pending.
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

9. Patrick approved the motion but requested a straight, white lightning-like line
   with a halo. Remove all bending, folds, colour, and lateral modulation; preserve
   the existing accelerating travel. Height-only shading keeps the line aligned
   across all parts. Removed the now-unused shader time uniform.

10. Browser recording confirms the straight white core and halo. Trimmed the first
    half-second of capture startup. Remaining raw footage measures 29.99 fps,
    33.33 ms median gap and 52.20 ms maximum, with no gaps over 100 ms. The H.264
    delivery file decodes cleanly. No new geometry, render passes, or dependencies.

11. Patrick confirmed the straight white halo looks much better and requested a
    taller band fading into its halo. Widen only the three vertical falloffs;
    preserve colour, emission strength, and the approved motion.
12. Verified 89 tests and the production build. Recorded the actual viewer using
    the existing synthetic cabinet, then trimmed the first 0.5 seconds containing
    capture startup delay. The retained source measures 29.95 fps, with a 52.47 ms
    maximum frame gap and no gaps over 100 ms. The 720p H.264 delivery file decodes
    cleanly and was uploaded to the previously authorized Drive destination.
    This is an effect preview, not evidence of a new CAD build or validation.

13. Patrick clarified "longer", not "stronger": extend only the downward halo
    and fade it out below the moving band. Preserve brightness and upward motion.

14. Recorded the actual viewer with the existing synthetic cabinet. Removed the
    first 0.5 seconds containing the blank capture startup frame. The retained
    raw interval measures 30.0 fps, with a 46.27 ms maximum gap and no gaps over
    100 ms. Sampled frames show the long downward fade; the delivery MP4 decodes
    cleanly. This remains an effect preview, not a new CAD validation.

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
