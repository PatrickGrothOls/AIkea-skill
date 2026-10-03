# Interactive README wardrobe previews

## Scope

Add two interactive GitHub STL previews: assembled and exploded. Keep the
existing photographs of the digital design and the installation guidance.

## Work packages

- [x] Create an isolated branch from the fresh public repository.
- [x] Locate the corresponding saved CAD assembly.
- [x] Produce small panel-only preview meshes from that assembly.
- [x] Add both interactive previews and explain their limitations.
- [ ] Verify geometry, privacy, and GitHub rendering; review the diff.
- [ ] Commit and open a pull request.

## Current state

Two ASCII STL blocks prepared: 80 panels and 1,002 triangles each; four doors
hidden. README is approximately 278 kB. GitHub Markdown API recognizes both as
STL render containers. Browser verification is pending.
No deployment or changes to manufacturing geometry are included.

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
