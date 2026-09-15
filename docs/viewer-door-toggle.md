# Viewer door visibility

## Scope

Add Hide doors / Show doors to the existing viewer so the interior can be
inspected without exploding the cabinet. Branch `codex/viewer-door-toggle`
builds on the current Vilja viewer and sourcing work at `e9b8045`.

## Current state

Implemented and verified in the existing Vilja viewer. The action is reversible presentation-only removal,
not a claim of checked hinge motion. Door-mounted fittings hide with their door;
cabinet-mounted fittings and lights remain. No CAD or manufacturing files change.

## Work packages

### WP1 — Visibility and controls

- [x] Filter door parts and their attached fittings using inspection ownership.
- [x] Provide a visible button even when mobile explosion controls are collapsed.
- [x] Select lit inspection materials when hidden and restore the baked finish.
- [x] Preserve explosion state and restore original visibility with Show doors.

- [x] Reduce title and CTA to compact helpers; use only a separation slider beside door visibility.

### WP2 — Verify and deliver

- [x] Test hidden doors, mounted fittings, unrelated parts and restoration.
- [x] Build the viewer and verify the actual Vilja model in the existing tab.
- [x] Save an interior screenshot and commit the focused change locally.

## Audit log

1. Patrick requested a door remover/opener button. Implement Hide/Show doors as
   the requested removal option; swinging requires a checked hinge-motion state.
2. Existing Vilja metadata attaches hinge bodies to door panels and mounting
   plates to side panels. Reuse that ownership rather than hiding all hinges.
3. Use the existing inspection asset for the exposed interior, where assembled
   baked shadows would otherwise retain the removed doors' occlusion.

4. Patrick requested much smaller helper cards and clear cabinet-first hierarchy.
   Replaced permanent full cards with a quiet title/help disclosure, compact
   inspection toolbar and standalone CTA; detailed controls open only on request.
5. All 67 viewer tests passed, including door/hinge ownership, exact restoration,
   empty focused-door framing and baked/inspection asset selection. Build passed.

6. Actual Vilja hide state: 152 visible parts (four doors and eighteen attached
   hinge bodies hidden), seven lights, no explosion, one canvas. Reset returns
   174 parts and the baked asset. No source GLB changed.
7. Tested narrow viewport and default size. Fixed resize-driven camera reframing
   after the narrow screen initially cropped the model. Detailed controls remain
   collapsed by default; both toolbar and reset were exercised in the browser.
8. Final viewer test suite: 67 passed. Production bundle rebuilt. All changed
   authored code files remain below 150 lines. Screenshots: /tmp/vilja-compact-controls.png
   and /tmp/vilja-compact-interior.png.

9. Patrick simplified Inspect further: no menu, labels, selectors or reset button.
   The final toolbar contains only Hide/Show doors and the separation slider.
   The earlier expanded-menu checks above describe an intermediate state.

10. Final slider-only toolbar built successfully and verified in the existing browser tab. Hide doors selects the inspection asset, and the native slider changes separation; one canvas remains. Screenshot: `/tmp/vilja-slider-controls.png`.
