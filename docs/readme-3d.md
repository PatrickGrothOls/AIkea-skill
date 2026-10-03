# Interactive README wardrobe previews

## Scope

Provide assembled and exploded wardrobe inspection from the README, with real
machining visible in a white interactive viewer. Preserve the existing images
and installation guidance. The audit below records the superseded STL approach.

## Work packages

- [x] Create an isolated branch from the fresh public repository.
- [x] Locate the corresponding saved CAD assembly.
- [x] Produce small panel-only preview meshes from that assembly.
- [x] Add both interactive previews and explain their limitations.
- [x] Verify geometry, privacy, and GitHub rendering; review the diff.
- [x] Commit and open a pull request.

## Current state

The detailed white CAD viewer supersedes the simplified inline STL previews.
It includes assembled and exploded views plus a door toggle. All machining stays
in the model; the page instructs visitors to zoom in to see it.
The demo is published on GitHub Pages. The simplified two-view interface is
being verified before updating that deployment. PR #1 remains unmerged.

## Audit log

1. Patrick requested an assembly preview and an exploded preview in the README.
2. Use native GitHub ASCII STL blocks for rotation and zoom without a hosted
   service. Simplified panel surfaces omit purchased hardware, machining,
   materials and illumination; the existing images retain the visual detail.

3. Matched all 84 authored parts against the saved part manifest, then omitted
   the four doors and all 641 purchased components. Convex panel hulls preserve
   the overall silhouettes while filling holes and rebates for a small preview.
4. Used the existing viewer explosion layout at amount 0.14. Only translations
   differ between the two meshes; this does not establish removal paths.
5. ASCII structure, finite coordinates and triangle counts passed. Both blocks
   are recognized by GitHub's Markdown renderer; no new runtime dependency or
   fabrication output is included. Private extraction intermediates stay ignored.
6. Live GitHub rendering exposed an axis mismatch: its viewer uses Y-up.
   Rotated both display meshes from CAD Z-up to Y-up; dimensions and relative
   panel positions are preserved. The CAD source is unchanged.
7. Normalize display coordinates to 1:25 scale for the native viewer, keeping
   both poses on the same scale. The README explicitly labels scaled previews.
8. Closer interaction testing superseded the axis assumption in entry 6:
   the native ground plane is Z-up. Restored CAD orientation and normalized to
   1:12.5 instead; the Y-up experiment intersected the viewer ground plane.
   Both meshes have zero degenerate triangles and consistent outward winding.
9. Inspected GitHub's public renderer to resolve display assumptions:
   it uses Z-up and automatically places the model above the grid. No extra
   placement correction was needed. Browser controls successfully frame both
   full models; GitHub controls the initial camera. Local screenshots saved.
10. Final winding checks caught two slender triangles inverted by three-decimal
    display rounding. Increased coordinate precision to six decimals. Both
    1,002-triangle meshes now pass finite, nondegenerate, outward-winding checks;
    edge vectors and shared-layout translations match within 0.0000021 units.
    Reviewed prose and generated data. PR #1 contains branch documentation;
    no merge performed.

## Detailed white viewer follow-up

Patrick requested a hosted white viewer because the simplified STL previews hid
machining details. This follow-up supersedes those inline STL blocks.

- [x] Export the 84 authored machined panels without hull simplification.
- [x] Build a static white viewer using the existing shared explosion layout.
- [x] Add assembled, exploded and machining close-up controls.
- [x] Verify exact source/mesh provenance, privacy, desktop and phone layouts.
- [x] Publish a reviewable demo and replace the README links.

Current follow-up state: local implementation and browser verification complete. Purchased vendor hardware
remains excluded. Machining geometry is design evidence, not fabrication approval.

11. Patrick approved trying the detailed white viewer. Reused the existing
    inspection layout and exact panel tessellation instead of convex hulls.
    All 84 authored panels remain; purchased hardware stays excluded.
12. Exported at 0.1 mm linear and 0.1 rad angular tolerance: 775,824 triangles.
    Primitive packing passed bitwise attribute and transform verification.
    Lossless gzip reduces the GLB from 28,112,572 to 5,634,050 bytes. Safe source
    and mesh hashes are recorded in `viewer/showcase/model-info.json`.
13. Added a static Three.js entry point without new dependencies. A render pass
    feeds ambient occlusion; its radius is expressed in model metres. Camera
    framing uses projected bounds, with a separate close-up of the door recess.
14. Inspected actual rendered assembled, exploded, door-toggle and machining
    views in Chrome. A requested 390 × 844 viewport measured 433 CSS pixels wide
    because of browser zoom; no horizontal overflow occurred. This checks the
    responsive layout, not performance on a physical phone. Real screenshots
    remain local except the deliberately selected public machining image.
15. The disk filled during dependency installation. No unrelated cleanup was
    performed; an existing installation with an identical lockfile was reused
    through an ignored local symlink. Production build and viewer tests passed.

## Build and publication

Run `direnv exec . npm --prefix viewer ci`, then
`direnv exec . npm --prefix viewer run build:showcase`.
The static output is `viewer/showcase-dist/`; only that output plus the project
license belongs on the Pages publishing branch. No server, credentials, analytics,
CNC source files or private evidence are required. The model is inspection geometry,
not an approved manufacturing package. New source modules each stay under 150 lines.

Live demo: https://patrickgrothols.github.io/AIkea-skill/

The simplified interface builds successfully and all 74 viewer tests pass.
The model asset is byte-for-byte unchanged. Updated README imagery shows
ordinary zoom in the exploded view, with no separate machining control.

16. Patrick clarified that machining should not appear optional. Removed the
    separate detail button and its camera/isolation mode, retaining all original
    geometry. Added the exact instruction: “Zoom in to see the machining details.”
    Old detail links now open the assembled model. README links follow the same UX.
