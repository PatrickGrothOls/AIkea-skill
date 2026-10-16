# Progressive README images

## Scope
Serve lightweight progressive JPEG previews in the README while preserving the
existing PNG originals, composition, materials, lighting and interactive viewer.

## Work packages
- [x] Confirm published image URLs work and measure the existing payload.
- [x] Encode four progressive JPEG previews and link each to its PNG original.
- [x] Verify progressive encoding, image dimensions, links and visual detail.
- [x] Review the diff.
- [x] Prepare the branch for review.
- [ ] Merge and verify public README loading.

## Current state
The four existing 3600 x 2700 PNG images total 25,803,532 bytes. Previews use
1800 x 1350 pixels, JPEG quality 88, no chroma subsampling and progressive encoding.
The README links previews to the unchanged originals; explicit viewer links remain.
The four previews total 952,396 bytes, a 96.3% reduction in inline image payload.
All four decode with progressive encoding and expected dimensions; README image
links resolve locally. Visual inspection confirms the machining, frames, hardware
and exploded parts remain visible. The original PNGs are unchanged.
The branch has not been merged.

Progressive JPEG can display an initial coarse scan followed by finer detail.
Actual incremental painting depends on browser and delivery buffering; it is not
an automatic replacement with the original PNG. See [MDN progressive images](https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Formats/Support_issues#progressive_images).
No browser connection is currently available, so GitHub visual loading is unverified.

## Audit log
1. 2026-10-16: Patrick requested a smaller initial image that improves afterwards.
   Use native progressive JPEG decoding for the README, keeping full-resolution
   originals on click. This implements the requested behavior without scripts.
2. The sharing thumbnail is a separate repository setting. Live metadata currently
   advertises the default GitHub card; this image-encoding change does not restore it.
