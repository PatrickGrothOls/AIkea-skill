# Viewer corner branding

## Scope

Add the requested large AIkea wordmark to the reusable viewer, with room for the
cabinet and compact controls on desktop and mobile. No CAD or material changes.

## Current state

Implemented and bundled. The existing cabinet viewer shows the logo; normal and
narrow viewport checks passed. Independent boundary review passed, with the help
popup offset corrected to clear the enlarged desktop header.

## Work packages

- [x] WP1: Add a prominent upper-right wordmark using the existing green palette.
- [x] WP1: Keep the title and help alongside it, truncating long titles on narrow screens.
- [x] WP2: Build the distributed viewer and inspect the existing cabinet tab.
- [x] WP2: Review the focused diff and commit the reusable viewer change.

## Audit log

- 2026-09-16: Patrick requested a large AIkea logo in a corner. Implemented a
  typographic wordmark in the top right, scaled from 40 to 72 pixels; it requires
  no external asset, does not capture orbit gestures, and adds no rendering load.
- 2026-09-16: Browser checks confirmed the logo, title and help fit a narrow
  354 CSS-pixel viewport. Restored normal viewport and retained one viewer tab.
  Review identified the old help popup offset; it now follows the header height.
