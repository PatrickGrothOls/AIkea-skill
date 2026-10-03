# Viewer glass cards

## Scope

Replace the opaque title, inspection and approval cards in the existing Three.js
viewer with clear glass surfaces. Preserve the model, camera, inspection and
approval behaviour. This is a local presentation change, stacked on the current
drawer runtime at `34ee885`; refreshed `origin/main` is an ancestor (0 behind).

## Work packages

### WP1 — Glass surface
- [x] Inspect existing cards and research GitHub glass implementations.
- [x] Add a shared glass treatment with visible backdrop, reflective rim and sheen.
- [x] Keep text and controls sharp; preserve pointer and keyboard interaction.
- [x] Retain source attribution and license for adapted styling.
- [x] Review responsibility placement using the code-boundaries skill.

### WP2 — Real viewer verification
- [x] Rebuild the skill's bundled viewer and run the existing viewer checks.
- [x] Inspect the real furniture behind the cards on desktop and mobile.
- [x] Check fallback/preference CSS by review and approval UI in the browser.
- [x] Capture screenshots and leave the viewer open for Patrick.
- [x] Review the final diff and commit the coherent presentation change.

## Current state

Completed locally on `codex/viewer-glass-cards`. The title, inspection and approval
cards share a clear surface, reflective rim, subtle backdrop refraction and sharp
foreground controls. Rebuilt the distributed skill assets; no new runtime package.
On mobile, controls float over the full-height canvas, so the model is visible
through the cards. No design geometry or approval semantics changed.

The approved outcome CTA wording is **Make it real**. Source-code packaging,
OAuth, S3 upload and notifications remain a separate, unimplemented workflow;
this presentation change does not repurpose visual approval as a purchase request.

## Verification

- `direnv exec . npm --prefix viewer run build`: passed.
- `direnv exec . npm --prefix viewer test`: 45 passed, 0 failed.
- Actual 99-piece HDF dresser loaded at `http://127.0.0.1:51342/`.
- Desktop 1280 x 800 and mobile 390 x 844 CSS-pixel layouts inspected in the
  Codex Chromium browser. Full-size canvas, no horizontal overflow, glass backdrop
  filter active, foreground text and native controls readable.
- Browser interaction: selected one drawer (9 pieces), changed separation by
  keyboard, restored all 99 pieces at zero separation. Mobile separation hides
  the approval card as before; reset restores it. No browser errors; an existing
  Three.js Clock deprecation warning remains.
- Approval layout inspected with a clearly labeled, temporary `door_openings`
  fixture on port 51343. No decision was submitted and no actual approval changed.
- Reduced-transparency, forced-colors and unsupported-filter fallbacks reviewed
  in CSS; those browser/OS modes were not emulated. Safari was not tested.
- Source and bundled MIT license match. Final whitespace check passed.
- Private screenshots in `local-evidence/glass-desktop.jpg`, `glass-mobile.jpg`
  and `glass-mobile-approval-fixture.jpg`; the last image is a UI fixture only.

## Responsibility review — PASS

Reviewed using `review-code-boundaries` after WP1 and after the mobile layout
adjustment in WP2. The entry point imports presentation styles and composes one
inert filter. The viewer coordinator only composes the filter and controls;
it acquires no optics, transport, persistence or manufacturing policy.

`ReviewGlass.css` owns the shared surface, optical fallbacks and control contrast.
`ReviewGlassFilter.jsx` owns the reusable SVG definition. Existing styles retain
typography and positioning; `AssemblyInspection.css` owns responsive arrangement.
The three cards opt into the same material without duplicating visual rules.
The approval client and CAD/model/camera collaborators are unchanged.

| Source file | Before | After | Responsibility |
| --- | ---: | ---: | --- |
| AssemblyInspection.css | 43 | 47 | Responsive control layout |
| AssemblyInspectionPanel.jsx | 35 | 35 | Inspection input UI |
| AssemblyReviewViewer.jsx | 93 | 97 | Viewer composition |
| ReviewApprovalPanel.jsx | 105 | 105 | Existing review decision UI |
| ReviewGuidanceCard.jsx | 11 | 12 | Title and interaction guidance |
| main.jsx | 12 | 13 | Entry point and style loading |
| styles.css | 135 | 125 | Canvas, typography and card layout |
| ReviewGlass.css | 0 | 97 | Shared glass material and fallback |
| ReviewGlassFilter.jsx | 0 | 18 | Backdrop optics definition |

No edited maintained source file crosses the 150-line review trigger. Generated
Vite bundles are built outputs, not independently authored responsibility owners.

## Audit log

1. Patrick requested glassmorphic cards in the existing Three.js viewer and
   explicitly asked for GitHub references, rejecting a milky/frosted appearance.
2. Reviewed `rdev/liquid-glass-react` and `dpawlikowski/liquid-glass`. Adapt the
   latter's surface layering and reflective edges under its MIT license, with a
   restrained live-backdrop filter. This implements Patrick's requested visual
   treatment without adding a second renderer or importing a component framework.
3. Keep the current drawer build as the branch foundation: origin/main is already
   included, and this viewer must retain the newer exploded inspection behaviour.
4. Browser inspection exposed the old mobile grid placing controls below the
   canvas. To fulfill the requested see-through surface, put them over the canvas
   in a bounded, scrollable control stack. Preserve desktop positions and all
   existing inspection/approval conditions.
5. Review caught two presentation interactions: scope secondary-text coloring to
   the guidance card so approval errors retain their warning color, and keep
   mobile cards positioned so their decorative layers stay inside each card.
6. Rebuilt assets, passed all 45 existing viewer checks, and verified real desktop
   and mobile interaction. Kept the optional approval fixture separate from the
   deliverable viewer and saved visual evidence. This is local browser evidence,
   not cloud upload, manufacturing approval, or a production deployment.
