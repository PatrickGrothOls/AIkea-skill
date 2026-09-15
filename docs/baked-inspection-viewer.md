# Baked furniture and detailed inspection in one viewer

## Scope
Use the approved Blender bake for intact furniture and the matching original
material GLB for inspection. Release each model before mounting the replacement;
keep approval bound to the original presentation artifact.

## Work packages
- [x] Add optional immutable inspection snapshot and fixed model manifest routes.
- [x] Select source geometry for any exploded or isolated view; restore bake on reset.
- [x] Dispose model buffers, materials and decoded images when changing assets.
- [x] Keep live inspection lights separate from the already baked illumination.
- [x] Validate viewer lifecycle, restricted HTTP paths, decisions and production bundle.
- [x] Review boundaries and commit the coherent slice.
- [ ] Integrate construction defaults and verify the corrected Vilja cabinet in one tab.

## Active handoff — 2026-09-15 13:28 UTC
Integrated construction defaults plus deck attachment metadata at af631e6. Private
project: ../vilja-skill-trial/local-evidence/project. Fresh build agent is complete;
do not rebuild CAD. corrected-closed-materials.glb and corrected-interior-materials.glb
have passing metadata/material proofs. Independent closed-source audit in
local-evidence/corrected-materials-independent.json confirms174 unique render IDs,
16feet/16plates, only deck/kickboard base panels, seven host-attached emitters and
the original2475×450×2374 outside envelope. All32 base articles follow deck_01.

Final bake is still pending. Attempt01 stopped in the sandbox engine probe with
SIGSEGV; the same installed engine passed its full probe outside the sandbox.
Attempt02 was intentionally interrupted before baking when a separate six-thread
Blender animation render was discovered. At13:27UTC that other job was PID57913,
rendering calm-a-full-installation.blend via render_saved_animation.py; swap was
5.2GB on the8GB Mac. Own bake PIDs58223/58299 were verified stopped. Do not disturb
the other task. Check all active Blender processes before retrying; do not run a
second heavy job. Use a fresh output directory (03) when the slot is free.

Verified runtime: ../blender-bake-skill/local-evidence/engine-only-runtime.
Use bake_furniture_presentation.py with corrected-closed-materials.glb, default
4096 atlas/16samples/3threads, outside sandbox. Require presentation.json PASS
and independent geometry/coverage checks before final display.

Port63332 currently serves corrected-closed-materials.glb for inspection (server
session89387). The single tab was navigated to the corrected construction view
at65percent explosion. A subsequent screenshot/DOM check timed out under memory
pressure; this is NOT yet a verified visual delivery. The dresser is no longer
the served asset. Once the bake completes, restart this same server with the bake
and --inspection-model pointing to corrected-closed-materials.glb, then reload
the same tab. Verify seven sources during explosion, all-panel groups, one canvas,
no photo renderer, and baked appearance on reset. Mark the tab deliverable.

Automation finish-vilja-cabinet-review remains active every5minutes with explicit
user approval; stay quiet while the other render is running and pause the
automation only after visual delivery. Manufacturing remains incomplete: six
drawers need compatible runner CAD; hinge widths/overlay exceed selected profile;
Korrekt socket fit, screw engagement, clips/loads and15mm deck stock need approval;
lighting wiring/endcaps/supply and full CNC/setup/fabrication checks remain open.

## Current state
Implementation and targeted validation complete. This implements the second
slice of docs/lit-component-inspection.md; visual calibration and actual new bake
remain pending. No source CAD geometry is changed by asset selection.

Evidence:61 viewer tests and10 HTTP/decision/path tests pass; production bundle
build passes. The first HTTP attempt hit the sandbox socket restriction; the
authorized loopback rerun passed. Actual approved99-part dresser switches to its
original material GLB at65 percent explosion and restores the baked GLB. The DOM
confirms one canvas, no photo renderer in either state, and99 visible pieces.
No current browser errors were observed (only the pre-existing Three.Clock warning).
This proves viewer transitions, not the pending corrected cabinet or peak RSS.

## Responsibility review
The existing145-line unit_review_server.py would cross150 with new routes. The
required independent refactor report recommended separating HTTP handling from
server lifecycle. Applied: ReviewRequestHandler owns request/response boundaries;
UnitReviewServer only binds and runs a loopback session. ReviewServerSession owns
immutable snapshots and decision authority. The primary artifact remains the sole
approval target. No per-feature lighting behavior was added to the HTTP layer.
Boundary review PASS: HTTP, immutable session authority, asset selection, cancellable
loading, GPU disposal and React lifecycle have distinct owners. Independent follow-up
review confirms the138-line shell stylesheet coherently owns the loading overlay;
no extra stylesheet is warranted. Each modified production file remains below150.

## Audit log
1. 2026-09-15: Patrick requested the prior finished quality together with detailed,
   illuminated inspection and bounded memory. Created this stacked local slice.
2. 2026-09-15: Applied independent server responsibility report. Client loads one
   uncached GLB at a time; shared small studio textures survive model disposal.
3. 2026-09-15: Automated checks and same-tab transition review passed. Construction
   integration, corrected cabinet bake and illuminated cabinet inspection remain open.
