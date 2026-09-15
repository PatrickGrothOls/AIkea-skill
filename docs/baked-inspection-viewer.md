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
- [x] Integrate construction defaults and verify the corrected Vilja cabinet in one tab.

## Current delivery — 2026-09-15
The corrected Vilja baked viewer has been delivered and visually inspected in the
existing tab at http://127.0.0.1:63332/?render=interactive&title=Vilja%20%E2%80%94%20finished%20review.
Server session52701 serves local-evidence/vilja-finished-attached.glb with
local-evidence/vilja-inspection-attached.glb as the matching inspection source.
The tab is marked deliverable. Assembled DOM: baked=true,174parts,1canvas,no photo
renderer. At20percent explosion: inspection.glb,7live lights,174parts,1canvas.
Restore returns to the bake; finished appearance and actual separated panels were
visually checked. The right-side strip and shelf supports were inspected separately.

All174 exported parts pass oriented triangle correspondence; maximum error is
0.000794331mm at the unchanged0.002mm limit. Zero uncovered panel centroids.
Manifest: local-evidence/vilja-presentation-03/presentation-rechecked.json. Original
failed bake log is preserved; the corrected verifier and hash chain are documented
in docs/bake-geometry-verification.md. No geometry was simplified or regenerated.

The explicitly authorized delivery heartbeat can now be paused. Manufacturing is
still unresolved: six drawers need compatible runner CAD; selected hinge fit and
overlay, Korrekt socket/screw/deck qualification and electrical/CNC checks remain
open. Source fixes remain local branches, not main or installed global skills.
The small full-engine acceptance fixture rerun remains a pre-merge check because
another task's Blender render was active. Actual Vilja verification and native
runtime verifier smoke pass. Do not start another render for this delivered viewer.

## Previous handoff — geometry revalidation in progress
Current branch is codex/bake-geometry-verification, stacked on inspection97e4ed4
and integrated hinge metadatafa16d9d. See docs/bake-geometry-verification.md.
Bake03 FINISHED; exec85208 exited1 only at final geometry comparison. The old
float32 nearest-vertex check rejected cabinet_01/hinge_04_hinge. Independent
direct-GLB diagnosis proves all73,632 triangles match bijectively with winding
and max0.000543457mm error, below unchanged0.002mm tolerance. Do not rebake.

Full revised verification IS RUNNING in exec session68332 (plain activated Python,
no Blender runtime). It writes local-evidence/vilja-presentation-03/export-geometry-rechecked.json
only after every part passes. It has passed the base, lights, cabinets04/03/02 and
is checking cabinet01 hinges. Nine focused verifier tests and three packing tests
pass. Check this session/report, not obsolete bake85208. No presentation PASS yet.

When it passes, run `direnv exec . python local-evidence/finalize_verified_presentation.py`.
This checks the original source/export hashes and all four reports, packs the
finished model, applies the exact36hinge ownership mapping to a new derivative,
checks inspection identities match, and writes presentation-rechecked.json.
It preserves the original failed bake.log and records the revalidation explicitly.
Outputs are local-evidence/vilja-finished-attached.glb and matching
local-evidence/vilja-inspection-attached.glb. Use these as primary and inspection.
The original assembled.glb is not changed. Do not weaken comparison tolerance.

Server session9114 still serves construction inspection on63332; single existing
tab1/browser1 is currently focused on the right-side lighting panel. Replace that
server only after verification/derivation PASS, restore whole furniture, check
finished quality and explosion/reset. Keep automation ACTIVE until visual delivery.
Another task had a Blender background animation PID65443 (GPU, six threads) while
our direct-GLB diagnostic ran. Never stop it or launch a competing bake.
All fabrication gaps in the previous handoffs remain open. No push/merge/global
skill install was performed. The reusable changes are local stacked branches.

## Previous handoff — 2026-09-15 14:07 UTC
Current branch is codex/compact-review-geometry in this same worktree. See
docs/compact-review-geometry.md. It adds static GLB packing and fixes inspection
lighting for consolidated solids plus panel-normal separation with attached hardware.
64 viewer tests and three packing tests pass; bundle built and live inspection checked.

Bake attempt03 IS RUNNING (exec session85208; observed engine PID60238, parent60191).
It started around13:40UTC. Do not start a duplicate. Output directory:
local-evidence/vilja-presentation-03. Immutable input remains the source described
below, SHA659cb44a25c198dc6a50880f762b3b48a628e8802762577d89db6cef8e8a4b13.
White coverage passed:40panels,344104triangle centroids, zero uncovered. Lighting
bake is active; no presentation.json yet as of14:06UTC. Last process check showed
the one engine using173percentCPU. Do not treat the quiet bake.log as a hang.

New inspection delivery candidate is local-evidence/vilja-inspection-attached.glb
(SHA b7b061da9f61bac2a6da7ac4796013329e61afbbc13b75d31c8e48607621e7fb).
Packing reduced18,181 to174draw primitives, preserving indexed attributes bitwise;
local-evidence/packed-independent.json verifies envelope and seven host emitters.
The attached derivative updates36hinge/plate inspection paths from exact saved
host declarations, with all binary chunks and other JSON unchanged. Source of
mapping: ../vilja-skill-trial/local-evidence/project/reviews/hinge-attachment-mapping.json.
Child reusable source fix is commit9c0c9c4 on codex/cabinet-defaults (not yet
cherry-picked here); five tests pass. No existing CAD/GLBs changed by that fix.

Once bake03 reports PASS, run local-evidence/apply_hinge_ownership.py with its
assembled.glb, a NEW output path, and that mapping. This produces a metadata-only
proof; never edit the original bake reports or source. If baked output has many
primitives, pack it to another new file first, requiring its packing proof.
Then serve the derived finished model with --inspection-model pointing to the
attached inspection derivative above. Current server session9114 on port63332
serves the attached inspection model only. Stop that session before replacing it.
Same tab1/browser1 is open; CUA binding viljaReviewTab. Use playwright.evaluate
for DOM diagnostics; locator('main').evaluate repeatedly timed out despite working
screenshots. DOM proved7lights/174pieces/1canvas/no photo renderer. Latest visual
check focused cabinet03/right_side at0percent: actual strip and shelf pins visible.
Restore whole assembly on final delivery. No final baked visual delivery yet.

Automation remains ACTIVE. Resume existing render, finish checks/one-tab delivery,
then pause it. Do not regenerate CAD. Manufacturing gaps below remain open.

## Previous handoff — 2026-09-15 13:28 UTC
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
Viewer implementation, corrected Vilja bake, detailed inspection and same-tab
switch/reset validation are complete; see Current delivery above for the actual
asset hashes and fabrication limits. No source CAD geometry is changed by asset selection.

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
