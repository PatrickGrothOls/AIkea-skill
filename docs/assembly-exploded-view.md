# Shared exploded assembly viewer

## Scope

Add the exploded-view feature Patrick requested and show the current reference
dresser. The feature is a presentation of existing named parts, not a new CAD
build, assembly sequence, joint change or machining proof.

## Current state

- Isolated branch `feat/assembly-exploded-view`, based on `72f4073`.
- Refreshed `origin/main` is an ancestor; the original checkout is preserved.
- The reviewed dresser has 65 physical part nodes and encoded assembly/part names.
- Existing CAD geometry, unresolved hardware and fabrication status remain authoritative.
- Viewer controls, grouped poses, part picking and exact reset are implemented.
- The bundled viewer and review-skill instructions are ready. All 35 viewer tests,
  10 viewer integration checks, and 11 skill-package/link checks pass.
- Actual-model acceptance confirms 65 intact pieces, eight drawer scopes,
  17 whole-view groups and seven pieces in an isolated drawer. Original vertices
  and exact assembled transforms are preserved.
- Desktop and mobile browser checks pass, including picking, reset, photo-mode
  transitions and approval-control isolation. Actual screenshots are saved.
- Nothing has been pushed or merged.

## Work package — Explode and inspect existing assemblies

- [x] Inspect the actual model, naming contract, viewer and review boundaries.
- [x] Keep original transforms; derive readable separation from group bounds.
- [x] Add whole-assembly and nested-assembly selection with a separation slider.
- [x] Show the clicked part's exported ID and restore the exact assembled view.
- [x] Prevent visual approval while an isolated or exploded pose is displayed.
- [x] Cover nested/grouped parts, transformed parents, reset and hidden-part picking.
- [x] Build the bundled viewer and document the feature in the review skill.
- [x] Inspect the actual dresser and an isolated drawer in the browser and on mobile.
- [x] Review boundaries using the review skill and commit the coherent slice.

## Responsibility plan

The model scene owns loading, materials and camera framing. A separate presentation
model owns the immutable starting transforms and selection of named subassemblies.
A layout class calculates group separation from their original bounds. React
controls own only input/display state. The viewer shell composes those concerns;
it does not learn dresser, drawer-hardware or machining recipes.

Use the existing exported `assembly__part` name convention for presentation
grouping and display the exact exported name for a selected part. Flat models can
still separate their parts. These viewer names are not new manufacturing identities.
The layout is a visual separation, not an assertion about collision-free removal
or assembly order. Keep the server's existing approval/evidence rules unchanged.

## Validation boundary

Require a successful bundle, focused model/control tests, existing viewer tests,
and a real browser check using the current dresser GLB. Verify that exploring and
resetting preserve every source vertex, rotation, scale and assembled transform.
Keep approval controls unavailable for nonassembled or isolated views. Preserve
the input GLB hash, show an actual screenshot, and leave the live viewer running.

### Completed evidence

- Source: the unchanged `reference-cold-start/project/reviews/dresser_01.glb`.
  SHA-256: `be61b7f1ada5d70db1c57a0b5ed926f02462670ae19a3ac8109e65f9275a3461`.
- Actual-model report: `local-evidence/dresser-explosion.json`.
- Browser reports and screenshots: `local-evidence/exploded-view/`.
  HTTP 200 for the viewer and model; no browser errors at 1280 and 390 pixels.
  A clicked drawer panel resolves to `left_drawer_01__bottom`.
- Photo/inspection/reset smoke checks at 1280 and 360 pixels pass. Approval
  controls disappear for exploded or isolated views, including an isolated
  drawer at 0%. They return only for the complete assembled view. Review data
  was stubbed in the test; zero approval requests were sent.
- The mobile handoff uses actual CAD images, with whole-dresser and drawer tabs.
  All 12 combinations of view, light/dark appearance and 320/360/736-pixel width
  pass image-loading, interaction and overflow checks.
- These are local viewer checks. They do not resolve the dresser's outstanding
  exact hardware, attachments, materials, motion/load or fabrication gates.

## Work-package boundary review

Applied the `review-code-boundaries` skill to the complete affected viewer path.
**PASS:** the shell composes scene and controls; `ReviewModel` owns the rendering
lifecycle; `ReviewPartCatalog` owns the GLTF primitive/physical-part boundary;
`AssemblyPresentation` owns original transforms and named groups; the layout class
owns geometric spacing; camera framing and effective visibility remain generic.
No carcass recipe, drawer dimensions, hardware inference or machining rules enter
the viewer. The GLTF catalog is needed because a physical part is not a leaf mesh.
It is distinct from how named parts are grouped or moved.

The original shell decreases from 143 to 93 lines; camera controls change from
140 to 142. Other changed production files are 10–73 lines, and the changed
Python test file is 123 lines. No hand-written affected file exceeds the 150-line
review threshold. Generated bundles are build output. No generic plugin framework,
unneeded fallback branches or duplicated manufacturing identities were introduced.

## Audit log

1. 2026-09-12 — Patrick authorized adding the proposed reusable exploded viewer
   and showing the current dresser. The word “vessel” is treated as that same
   dresser, which is the assembly under discussion.
2. 2026-09-12 — Use the saved dresser model directly. No CAD regeneration or
   hardware substitution is required to move existing meshes for inspection.
3. 2026-09-12 — Keep hierarchical selection and part identification in the shared
   viewer. This should serve other assemblies without dresser-specific scripts.
4. 2026-09-12 — The first actual-GLB test rejected a leaf-mesh count of 1,970.
   Added a GLTF part catalog using loader associations, so each physical panel
   retains all its material/face primitives. Added a regression for this boundary.
5. 2026-09-12 — Hidden ancestors are excluded from ray picking and zoom. An
   isolated drawer must not hit or zoom toward its invisible parent carcass.
6. 2026-09-12 — Actual-model and browser acceptance passed. Inspected whole-dresser,
   drawer and restored-photo views. Inspection poses remain explicitly separate
   from assembly-order and manufacturing evidence.
7. 2026-09-12 — Boundary review passed for this one viewer feature. Keep private
   dresser evidence outside the distributable skill; ship the reusable code,
   tests, instructions and generated viewer assets together.
8. 2026-09-12 — Save the coherent implementation as a local feature commit.
   Leave the tested viewer running for inspection; no push or merge is included.
9. 2026-09-12 — Patrick observed that every drawer lacks runners. Inspection
   confirms they are absent from the source assembly, rather than hidden by the
   exploded viewer. The 45 passing tests cover the viewer; they do not establish
   a complete drawer installation. Record the construction follow-up below.

## Construction follow-up — Missing drawer runners

### Confirmed current state

All eight `runner_installation` requirements remain unresolved. The saved design
uses a proposed 350 mm sizing input and 13 mm side reservations, with no selected
runner or purchased geometry. Its box is 651 × 382 × 145 mm; the saved opening
depth used by the planner is 418 mm. The verified 500 mm runner profiles currently
in this checkout do not fit that opening. No runner has been added or mounting
hole declared during this investigation.

The drawer sides already have inner-face Cabineo operations. Blind runner pilots
entered from the opposite outer face would violate the requested one-face CNC
process. A complete attachment solution must be checked before calling these
drawers finished. Undeclared mounting holes cannot count as a setup pass.

### Proposed next work package

- [x] Confirm whether runner geometry was missing or merely hidden.
- [x] Trace the saved box dimensions, nominal allowance and open requirements.
- [ ] Select and verify a complete runner system against depth, width and load.
- [ ] Resolve one drawer's exact cabinet/box attachment and one-face machining.
- [ ] Import the exact left/right components and verify closed fit and travel.
- [ ] Repeat the proved installation across all eight independently owned drawers.
- [ ] Reconcile eight purchased pairs in the BOM and show closed/open/exploded views.
- [ ] Review the completed construction change with the review skill.

### Sourcing investigation, not a selected product

Hettich [KA 4532 Silent System article 9114273](https://shop.hettich.com/de_DE/p/9114273)
provides a 350 mm candidate and an exact CAD entry. Its published minimum cabinet
depth is 354 mm. The [official installation sheet](https://web2.hettich.com/hbh/addon/montage/MS_10547_00_Montageanleitung_KA4532-SiSy.pdf)
also shows a 550 mm maximum-width recommendation, so suitability for the current
651 mm box is unresolved. Do not treat length alone as compatibility.

The vendor portal generated an AP214 download for article 9114273. No local STEP
was recovered: the browser download did not produce a file in Downloads, and
retrieving its observed direct link returned HTTP 403. No alternate-size file,
scaled geometry, source-CAD claim or inferred fixing pattern was substituted.
This candidate does not yet qualify for the current design.
