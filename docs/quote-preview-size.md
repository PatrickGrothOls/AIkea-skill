# Bounded quote preview

## Scope
Make current-scene PNG previews fit the hosted intake limits on large/high-DPI displays.

## Work packages
- [x] Reproduce a 3840 by 2100 PNG rejected after upload by the hosted validator.
- [x] Scale captures before submission without changing the model or viewer canvas.
- [x] Bound encoded bytes before the request can freeze.
- [x] Run all 73 viewer regressions and rebuild committed assets.
- [x] Complete fresh independent review: round 3 passes all lanes.
- [x] Publish and merge.

## Current state
Captures retain aspect ratio within 1600 pixels per side and 800,000 pixels total. PNGs over the 4 MB transport cap cannot be submitted. Server limits stay unchanged. All 73 viewer tests and the production build pass; independent round 3 passes all lanes.

## Audit log
- 2026-10-01: Under Patrick's authorized review/fix loop, accepted the reproduced high-DPI preview failure. Resizing only the quote thumbnail preserves source geometry and reduces upload bytes.

Release evidence and remaining limits: [desktop4-release.md](desktop4-release.md).
