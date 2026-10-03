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
It includes all 84 original panels, 17 applied frame pieces and 507 saved hardware
components (Cabineos excluded), plus four proposed brass pulls, with assembled and
exploded views plus a door-panel toggle. All machining stays
in the model; the page instructs visitors to zoom in to see it.
The demo is published on GitHub Pages. The simplified two-view interface and
zoom instruction were verified on the live deployment. PR #1 remains unmerged.

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

Current follow-up state: local implementation and browser verification complete. The hardware follow-up below supersedes the initial panel-only export.
Machining geometry is design evidence, not fabrication approval.

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

17. Published the simplified UI to the existing Pages branch without rewriting
    history. Deployment succeeded; live browser verification confirms the exact
    zoom instruction and only Assembled/Exploded controls. Privacy check: zero
    findings. All 74 tests pass; production build passes.

## Hardware completeness follow-up

Patrick identified missing hinge and other purchased CAD. Restore all 641 saved
hardware components alongside the 84 machined panels. The source STEP remains
unchanged. Use authored mounting ownership for exploded placement, never
proximity guesses. Door visibility hides only the wood so hinges remain inspectable.

- [x] Export and verify all 725 source components.
- [x] Preserve authored hardware-to-panel ownership during explosion.
- [x] Display metal hardware separately from white panels.
- [x] Verify visible hinges, runners and base fittings in the browser.
- [x] Update the live demo, tests, README and branch documentation.

18. The earlier panel-only export caused the missing hardware. Restore the saved
    source assembly. Exact manufacturer hinges/runners coexist with illustrative
    connectors and screw shapes already present in that source; do not claim
    every fixing is an exact manufacturer model or a fabrication-approved fit.

19. Exported all 725 saved STEP components without mesh simplification. The model
    has 1,849,872 triangles and compresses to approximately 13.8 MB. Retrieved all
    641 mounting-panel identities from the original authored builder; every one
    resolves to an exported panel. Only inspection metadata changed after the
    bitwise-verified packing step; the mesh binary payload remained identical.
20. Automated verification confirms every fitting receives the same exploded
    translation as its authored mounting panel, and restoration returns all 725
    original transforms. All 74 viewer tests pass. Local browser inspection shows
    the real hinges, drawer runners and feet; hiding door wood retains hardware.
    Updated model metadata passes the private-data guard with zero findings.
21. Published the full hardware model from source commit `49b8cd5` through the
    existing Pages branch (`e7de96f`). Pages deployment succeeded. Live browser
    verification shows the 641-component hardware caption and visible hinge CAD
    with door panels hidden; a zoomed screenshot was saved as private evidence.
    The source PR remains open and unmerged. Physical phone performance remains
    unverified.

## Cabineo exclusion follow-up

Patrick requested that Cabineos alone be excluded. Remove the 134 components
identified as Lamello Cabineo in the source inventory. Retain every panel and
all other fittings, including the separate threaded inserts and machining.

- [x] Remove only the inventoried Cabineo meshes from the public asset.
- [x] Verify remaining geometry, ownership and viewer transitions.
- [x] Update documentation, publish and verify the live viewer.

22. The exclusion is limited to Cabineo connector bodies, per Patrick's request.
    The remaining 507 hardware components and all 84 machined panels stay in the
    demonstration; the source assembly and fabrication files remain unchanged.

23. Removed the 134 inventory-identified Cabineo bodies and their mesh buffers.
    Independent comparison confirms every retained component has byte-identical
    geometry and unchanged transforms and ownership. All 74 viewer tests and the
    production build pass. Local browser checks confirm retained hinges/runners
    in exploded view; the README screenshot now reflects the exclusion.

24. Cabineo exclusion published as Pages commit `b99ba9c`; deployment succeeded
    and the live page shows 507 hardware components and the explicit exclusion.

## Framed-door appearance follow-up

Patrick requested frames like the supplied entrance elevation. Use plain white
65 mm-wide applied borders, 6 mm thick, following each current door outline.
These are separate real CAD pieces bonded to the unchanged 18 mm backing.
The proposed total door thickness is 24 mm; attachment, hinge load, operating
clearance and the additional 6 mm front projection remain unqualified.
The private reference drawing is not part of the public repository.

- [x] Build explicit frame parts using the shared panel construction contracts.
- [x] Verify geometry, closed placement and door visibility/grouping.
- [x] Show the framed doors for appearance review and record limitations.

25. Chose separate flat applied strips to match the reference's plain recessed
    centre appearance while retaining existing hinge machining. This is a draft
    aesthetic choice within the requested frame addition, not fabrication approval.

26. Rebuilt the complete draft parent with 17 separate applied strips through
    PanelAssemblyBuilder. Applied-operation checks pass; every strip is one valid
    solid, touches its backing and has no volumetric overlap with backing or other
    strips. Explicit strip blanks fit the current 2497 by 1247 mm usable rectangle.
    Existing base mounting extension qualifications remain unresolved; no full
    fabrication clearance is claimed. The first frame export encountered unhydrated
    base hardware, so the additive export now selects panels from the checked tree
    and retains all previously verified hardware bytes from the saved viewer asset.
27. Appended only the new frame geometry to the viewer. The existing binary buffers
    remain identical, including all machining and the 507 retained fittings.
    Seventeen strips add 204 triangles and about 1 kB compressed. The complete
    model has 608 components. Saved editable frame specifications with the asset.
28. All 74 viewer tests pass, including frame-to-door movement and restoration.
    Local browser checks verify complete front visibility, attached exploded frames
    and hidden wood with hinges retained. Subtle edges identify the actual frame
    solids in the white CAD inspection view. Attachment, added mass and full motion
    still require qualification; the additional front projection is 6 mm.

29. Published the appearance preview from `9578b31` through Pages commit
    `fdf7126`. Deployment succeeded. Live browser verification shows the white
    framed fronts with Show doors enabled and the 101 panel-piece / 507 hardware
    caption. Saved live screenshots; privacy scan reports zero findings. The PR
    remains unmerged and all fabrication limitations above remain open.

## Brass handle appearance follow-up

Patrick requested golden/brass handles on the framed doors. Add one slim vertical
brushed-brass pull on each free-edge stile. Use a 160 mm bar with 128 mm post
centres, 10 mm diameter and 32 mm projection as an explicitly illustrative design.
Place the first three at 1100 mm above the floor and the short door at 500 mm.
No product has been selected and no fixing holes or fabrication approval are implied.

- [x] Build four valid CAD handle concepts and retain the existing model geometry.
- [x] Verify placement, brass appearance and door-owned visibility/explosion.
- [ ] Publish, capture the live result and record validation.

30. A slim round pull adds the requested brass accent without obscuring the frame.
    All four doors are left-hinged, so pulls sit on their right-hand stiles. The
    shortest door needs a lower pull; its outline limits the available height.

31. Each handle is one valid CAD solid. The original mesh buffers remain unchanged.
    All 74 viewer tests and the production build pass. Local browser inspection
    confirms four brass pulls, aligned first-three placement, and handles hiding
    with their doors. Tests verify door-owned explosion and exact restoration.
    No fixing holes were added; the product and mounting remain to be selected.
