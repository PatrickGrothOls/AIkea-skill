# White painted wardrobe preview

## Scope

Show the latest CNC-sized wardrobe in white paint, as Patrick requested. Add an
optional viewer finish while preserving the source model and purchased materials.
The drawing's RAL 9010 note guides a warm-white screen approximation.

## Current state

The viewer previously replaced all furniture surfaces with plywood textures.
`finish=white` now selects a smooth satin material for faces and edges. The
existing source-material exclusions are shared by the paint and plywood modes.
This changes appearance only, without changing construction or coating readiness.
The real current wardrobe was inspected in the white viewer, including its
plinth, side panels, framed fronts, drawers and niche. The screenshot is saved at
`/private/tmp/aikea-full-pdf-cnc-test/reviews/screenshots/wardrobe-white.jpg`.
The source GLB checksum is unchanged. All 23 existing viewer checks and the
portable viewer build pass. The change is committed locally, not merged.

## Work packages

- [x] Inspect existing material presentation and current wardrobe artifact.
- [x] Add an optional white-paint surface and share material ownership rules.
- [x] Run the existing viewer checks and rebuild the portable viewer.
- [x] Inspect the actual white wardrobe and save a viewer screenshot.
- [x] Review and commit the focused change locally.

## Audit log

1. Patrick asked to paint the shown wardrobe white. Use the current 113-part
   CNC-sized model and the drawing's white-finish direction.
2. Preview satin warm white in the viewer; keep photographic plywood as the
   default for other views. Preserve purchased hardware and lighting materials.
3. Browser inspection showed the plywood exposure clipped the white highlights.
   Lower the white preview's camera exposure so its recesses remain legible.
4. Interactive inspection exposed missing tone mapping after contact shading:
   the installed EffectComposer disables renderer tone mapping. Add its supported
   ToneMapping effect after ambient occlusion so white surfaces retain detail.
