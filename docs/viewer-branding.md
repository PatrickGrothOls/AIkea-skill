# Viewer corner branding

## Scope

Add the requested large AIkea wordmark to the reusable viewer, with room for the
cabinet and compact controls on desktop and mobile. No CAD or material changes.

## Current state

The selected 2026-09-18 image is now the source of the upper-right logo.
Its exact silhouette is retained through an SVG luminance mask, with the pale
background and letter cutouts transparent over the scene. No font substitution
or newly drawn letter contours. The source JPEG is bundled locally (157 KB).
Production build passed; the actual header was visually checked in an isolated
browser preview. The previous wardrobe GLBs and server are absent, so this check
covers branding placement, not a restored cabinet scene.

## Work packages

- [x] WP1: Add a prominent upper-right wordmark using the existing green palette.
- [x] WP1: Keep the title and help alongside it, truncating long titles on narrow screens.
- [x] WP2: Build the distributed viewer and inspect the existing cabinet tab.
- [x] WP2: Review the focused diff and commit the reusable viewer change.
- [x] WP3: Preserve the selected original logo and add petrol/gold compositing.
- [x] WP3: Make kea translucent over the scene without changing CAD or materials.
- [x] WP3: Rebuild and verify the logo and alpha settings in the existing tab.
- [ ] WP3: Inspect cabinet detail passing directly behind kea during manual zoom.
- [x] WP4: Match the actual viewer typography and palette after user review.
- [x] WP4: Remove the superseded raster asset and colour-extraction filters.
- [x] WP4: Rebuild and visually verify the sans-serif logo in the existing tab.
- [x] WP4: Restore the shared I/k counterform after user review.

- [x] WP5: Bundle Patrick's selected image and retain its exact silhouette.
- [x] WP5: Preserve upper-right placement and transparent cutouts.
- [x] WP5: Build and visually check the actual header component.
- [ ] WP5: Check over the cabinet when its preview assets are restored.

## Audit log

- 2026-09-16: Patrick requested a large AIkea logo in a corner. Implemented a
  typographic wordmark in the top right, scaled from 40 to 72 pixels; it requires
  no external asset, does not capture orbit gestures, and adds no rendering load.
- 2026-09-16: Browser checks confirmed the logo, title and help fit a narrow
  354 CSS-pixel viewport. Restored normal viewport and retained one viewer tab.
  Review identified the old help popup offset; it now follows the header height.
- 2026-09-16: Patrick specified a blue A, a blue-and-white striped I, and white
  kea. Split the lettering into styled spans while retaining a single accessible
  AIkea label. Rebuild and browser verification accompany this visual change.
- 2026-09-17: Patrick chose the petrol/champagne concept and explicitly requested
  gold-tinted letters that reveal the scene during zoom. Replaced text spans with
  a small SVG compositor using the approved original silhouette as two masks.
  Petrol ink remains opaque; gold uses a 48–60% opacity gradient. Masking is confined
  to the logo and pointer events pass through it; no extra 3D rendering is added.
- 2026-09-17: Patrick rejected the serif/petrol/gold logo in context because it
  conflicts with the surrounding UI. His correction supersedes the earlier logo
  study: use the inherited sans-serif family and exact CTA green, with warm-white
  translucency matching the glass controls. Native SVG text supplies both the
  field cutout and tinted lettering, avoiding image masks and their download.
- 2026-09-17: Patrick identified that switching to ordinary SVG text lost the
  shared I/k idea. Replaced the separate I and k glyphs with a single field whose
  custom k cutout also defines the I's right contour. Kept the UI font for A/ea,
  CTA green, translucency and gesture pass-through. Build and browser check passed.

- 2026-09-18: Patrick selected the attached lowercase-ea logo and requested it in
  the top-right corner. This supersedes the generated uppercase/striped E trials
  and the earlier hand-drawn lettering. Bundled the exact JPEG as a mask source,
  retained the viewer green and transparent letter cutouts, and verified the
  header in-browser after a successful production build. Existing preview GLBs
  were absent; no furniture regeneration or geometry changes were made.
