# Make it real viewer CTA

## Scope

Add Patrick's approved outcome-oriented **Make it real** action to the existing
Three.js viewer. Keep it in the glass-card system with a clear, honest response
while the source-code upload service is unavailable. Stack this small UI slice
on `4a35c36` (`codex/viewer-glass-cards`); refreshed origin/main is included.

## Work packages

### WP1 — Viewer action
- [x] Add the action and agreed outcome copy to the assembled viewer.
- [x] Keep existing visual approval available in a separate card.
- [x] Provide an accessible, dismissible unavailable-service response.
- [x] Review responsibility placement using the code-boundaries skill.

### WP2 — Verify and show
- [x] Build the bundled viewer and run existing viewer checks.
- [x] Verify desktop/mobile layout, click, Escape and return focus.
- [x] Check inspection/reset and the optional approval card.
- [x] Capture mobile-friendly screenshots and leave the viewer open.
- [x] Review the final diff and commit this local UI slice.

## Current state

The missing CTA is implemented and verified locally. It reads **Make it real**
with **Your design, cut to fit and ready to assemble.** It appears in its own
glass card at the lower right on desktop and beneath inspection controls on
mobile. Clicking opens an explicit unavailable-ordering message; Escape and
the return button close it and restore focus to the CTA.

Upload infrastructure remains unconfigured; this slice does not claim an order,
price, upload or production approval. No user files leave the computer. The next
infrastructure slice still needs the selected destination/account, authentication,
source-package upload and notification flow. It must replace the unavailable
message with the automatic source-code handoff previously requested by Patrick.

## Verification and responsibility review

- `direnv exec . npm --prefix viewer run build`: passed; bundled skill assets rebuilt.
- `direnv exec . npm --prefix viewer test`: 45 passed, 0 failed.
- Actual 99-piece dresser tested at 1280 x 800 desktop and 390 x 844 mobile CSS
  viewport sizes in Codex Chromium. No horizontal overflow or browser errors.
- Native modal, initial focus, Escape, return button, and focus restoration checked
  in the browser. No network request or approval submission is made by the CTA.
- Separate approval fixture verified on desktop/mobile: 10px gap between approval
  and CTA, both visible. No fixture decision was submitted. Inspection hides both
  actions; restoring the assembly returns them.
- Screenshots: `local-evidence/make-it-real-mobile.jpg` and
  `local-evidence/make-it-real-desktop.jpg` (private, untracked).
- Deliverable viewer: `http://127.0.0.1:51344/?render=interactive&title=Dresser`.
  Temporary fixture viewer uses port 51345 and is stopped after checking.
- `review-code-boundaries`: **PASS** after both work packages. The coordinator
  only composes the new card and action stack. Availability text and modal behavior
  live in `MakeItRealCard.jsx`; layout and emphasis live in `ReviewActionCards.css`.
  No upload/provider, manufacturing, identity or persistence rules enter the viewer.
  Existing review client, model, geometry and approval conditions are unchanged.

| Maintained source | Before | After | Responsibility |
| --- | ---: | ---: | --- |
| AssemblyReviewViewer.jsx | 97 | 103 | Compose viewer sections |
| MakeItRealCard.jsx | 0 | 28 | CTA and unavailable-service response |
| ReviewActionCards.css | 0 | 54 | Action-card placement and styling |

All maintained source files stay below the 150-line review trigger. No new runtime
dependencies, catch-all error handling, speculative upload configuration or tests
mirroring this small presentation component were added. Browser checks exercise
the native interaction; existing tests retain the geometry and review coverage.

## Audit log

1. Patrick approved **Make it real** as the CTA, asking to sell the outcome, and
   then pointed out that it was absent from the glass-card screenshots.
2. Add it directly to the current viewer. Use a short native dialog to explain
   unavailable ordering when clicked, so the reviewable UI never claims an upload
   has happened. This is the implementation's current limit, not a replacement
   for the intended automatic source-code handoff.
3. Group existing visual approval and the new CTA vertically at the same desktop
   anchor to prevent overlapping cards; use the existing mobile control stack.
   Both follow the existing assembled-view condition so detailed inspection stays
   focused on parts. The CTA does not submit a visual approval.
4. Completed browser interaction, separate fixture coexistence, build and 45 viewer
   checks. Saved screenshots for mobile review and kept the real viewer open.
   No cloud resources, uploads, prices or orders were created.
