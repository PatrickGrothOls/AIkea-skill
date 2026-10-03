# Interactive README wardrobe previews

## Scope

Add two interactive GitHub STL previews: assembled and exploded. Keep the
existing photographs of the digital design and the installation guidance.

## Work packages

- [x] Create an isolated branch from the fresh public repository.
- [x] Locate the corresponding saved CAD assembly.
- [x] Produce small panel-only preview meshes from that assembly.
- [x] Add both interactive previews and explain their limitations.
- [x] Verify geometry, privacy, and GitHub rendering; review the diff.
- [x] Commit and open a pull request.

## Current state

Two interactive previews are available on `codex/readme-3d` in PR #1 (unmerged).
Each contains 80 simplified panels and 1,002 triangles; four doors are hidden.
Both native GitHub viewers render, and rotation and zoom were exercised in
Chrome. Geometry and privacy checks pass. No runtime dependencies, source
project files or manufacturing outputs ship.

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
