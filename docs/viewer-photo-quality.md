# Real-model photo quality

## Scope

Improve the existing dresser's material presentation and photographic rendering,
using the exact GLB. This small branch stacks on `e83cd58`, the completed viewer
CTA and mobile inspection work. Generated UI concepts are aesthetic references,
not model or machining evidence.

## Work packages

### WP1 — Material and light
- [x] Correct panel grain direction and give separate parts stable texture variation.
- [x] Tune the wood finish, directional studio lighting, and photographic resolution.
- [x] Review the changed responsibilities with the code-boundaries skill.

### WP2 — Bound the photo-renderer lifetime
- [x] Find the allocations repeated when returning from drawer inspection.
- [x] Keep the assembly mounted and reuse one closed-assembly photo scene.
- [x] Apply the upstream disposal fix and release the renderer on unmount.
- [x] Cap photo pixels and accumulated samples; pause hidden-tab photo work.
- [x] Test repeated inspection, resumption, resize, sample limits, and cleanup.
- [x] Review responsibilities with the code-boundaries skill.
- [x] Save a local implementation checkpoint; keep live acceptance open.

### WP3 — Compare and verify
- [x] Run the viewer checks and rebuild the packaged viewer.
- [ ] Inspect the actual dresser in assembled and exploded states.
- [ ] Save a real-render screenshot for mobile and compare against the baseline.
- [ ] Review the final diff and commit the coherent rendering change.

## Current state

Recovery verification is pending. All 52 viewer checks pass and the packaged
viewer builds with the lifecycle fix. The local server is running again at
http://127.0.0.1:51344/ with `--no-open`. Only one in-app tab remains, currently
the connection-error page left by the crash. Browser Use rejects that internal
data URL, and native Codex app control is unavailable. A request to reopen the
same tab in interactive mode was queued through the app; Patrick was asked to
reload the existing preview. No new live viewer was opened.

Before the crash the actual 99-piece HDF-bottom dresser loaded and drawer
inspection showed nine parts, but restoring the photo view stalled. The final
photo/inspection round trip, stable-memory observation, and improved screenshot
are still unverified. This branch is not ready to merge based only on unit tests.
The baseline image is in the previous branch's
`local-evidence/actual-dresser-photo-render.jpg`.

## Responsibility review — WP1

`review-code-boundaries`: **PASS**. `PanelTextureCoordinates` owns only the
normal-based UV projection and reproducible offset (34 lines). `PlywoodSurface`
retains eligibility, texture settings, and material assignment (143 -> 114 lines).
It delegates coordinate generation instead of learning new studio or rendering
rules. `StudioBackdropGeometry` owns the floor-to-wall mesh (26 lines), outside
the CAD tree; `AssemblyStudioFloor` only places and shades it (22 -> 27 lines).
The viewer coordinator still only composes the scene and camera settings
(103 -> 100 lines). HDR fill (19 -> 17), area lights (59 -> 67), renderer callback
(9 -> 10), and camera direction (90 -> 90) stay in their existing owners, all
below 150 lines. No manufacturing rules or runtime network services were added.

The 52 viewer checks pass, including three new tests covering horizontal grain
on drawer fronts, vertical grain on tall panels, independent repeatable offsets,
and unchanged position/normal buffers. The existing tests continue to cover
hardware materials, exploded ownership, exact transforms, and inspection reset.

## Responsibility review — WP2

`review-code-boundaries`: **PASS**. `PhotoRenderSession` (65 lines) owns the
renderer allocation, one scene snapshot, pixel/sample budget, camera resets,
pause/resume, and disposal. `AssemblyPhotoRenderer` (22 -> 20 lines) binds that
session to React/Three frame and cleanup hooks. `AssemblyReviewViewer` knows only
when the whole assembly is eligible for photo rendering, retaining the same
model subtree across inspection changes. It does not learn GPU budgeting or
library cleanup details. The four new lifecycle tests use an injected renderer
probe to establish allocation counts and work limits without allocating a GPU.
Live WebGL behavior remains a separate acceptance step.

The unused React wrapper was removed, and the existing underlying renderer was
promoted to a pinned direct dependency, `three-gpu-pathtracer@0.0.24`.
Its upstream changelog records the `WebGLPathTracer.dispose()` fix:
https://github.com/gkjohnson/three-gpu-pathtracer/blob/main/CHANGELOG.md
Generated license notices reflect the installed dependency set.

## Audit log

1. Patrick asked for substantially more realism after reviewing the actual photo
   mode. Improve the real viewer and show evidence from the same model; do not
   substitute generated furniture imagery or change machining geometry.
2. Patrick requested only one browser tab because of rendering memory use. Closed
   the extra drawer viewer and verified only tab 17 remains. Reuse this tab for
   all further comparisons instead of opening another live renderer.
3. Keep changes within material presentation and studio rendering. Use the
   existing licensed texture and rendering libraries before adding new assets or
   dependencies. Grain appearance is a review convention, not a nesting authority.
4. The first material pass showed clearer grain but an artificial floor horizon.
   Replace the finite flat studio floor with a smooth floor-to-wall sweep and
   add a separate backdrop light. Use a less wide-angle camera for the product
   view. The backdrop is not a furniture part and is absent from inspection.
5. Render photo mode at its full drawing-buffer resolution, with a 1.5 device
   pixel ratio cap and 1024 progressive samples. The existing 1K texture remains
   shared. This experimental setting was superseded by item 7 after the crash.
6. Patrick reported a memory-related computer crash during the return from drawer
   inspection. Code inspection found repeated photo-renderer creation without
   wrapper disposal and an upstream disposal error in version 0.0.23. These are
   concrete renderer defects; they do not establish the sole cause of the Mac's
   crash. Preserve the exact GLB and fix the rendering lifetime first.
7. Reuse one photo renderer across inspection changes; no scene rebuild on
   restore. Limit photo output to 750,000 pixels and 512 samples with four bounces.
   Camera changes, resume, and resize restart accumulation without allocating a
   new renderer. A settled photo is still presented each frame, while sampling
   stops. Hidden tabs skip photo work. Use the public fixed upstream disposal.
8. Regression checks pass (52/52), including ten repeated inspection/restore
   cycles in the renderer probe. The production build succeeds. Restarted only
   the matching server with no automatic tab creation. Live visual and memory
   checks remain pending until the existing error tab can be reloaded.
9. Verified the server's GET endpoint serves the new `index-BZ2j7A2w.js` bundle.
   Preserve this tested implementation as a local checkpoint while keeping the
   actual WebGL acceptance tasks open. No push or merge is part of this recovery.
