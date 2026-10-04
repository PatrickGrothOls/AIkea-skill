# Door frame shadows

## Scope

Make the raised door frames easier to distinguish with oblique studio light and
real mesh shadows. Keep the approved wood finish, CAD geometry and warm LEDs.
Patrick requested shadows to reveal the door details.

## Work packages

- [x] Inspect the existing lighting and confirm that shadows are disabled.
- [x] Add a shadow-casting key light and enable mesh shadow participation.
- [x] Fit the shadow volume to each furniture pose and cache it during orbit.
- [x] Build and visually check closed doors, interior and exploded poses.
- [x] Review the diff and publish the viewer adjustment.

## Current state

Production build and all 78 viewer tests pass. Closed-door frame shadows, orbit,
interior and exploded poses were visually checked locally; no browser warnings or
errors were observed. Published and verified live. One 2048px shadow map is updated on
pose changes, not camera orbit. No geometry or LED changes. README images are
unchanged; this request concerns the interactive viewer.

## Audit log

1. Use Patrick's requested directional shadows to reveal the existing frame
   depth. Keep studio lighting separate from the recessed LED lighting so the
   approved interior appearance can remain independently controlled.
2. Cache the shadow map between poses because camera motion does not alter
   light-to-object geometry; this avoids repeated CAD shadow rendering on orbit.
3. Use PCFShadowMap supported by the installed Three.js version; its former
   PCFSoftShadowMap alias is deprecated. Keep the existing ambient fill so
   shadows show relief without obscuring the wood grain.
4. Published Pages commit `0ab17ed`; deployment `37201463211` succeeded.
   Reloaded the live viewer and confirmed the closed-door shadows. Source PR #4
   remains open; the viewer publication is separate from merging source to main.
