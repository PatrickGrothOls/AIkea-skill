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
