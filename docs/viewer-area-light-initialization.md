# Cabinet area-light illumination

## Scope and current state

The user requested visible neutral-white illumination of cabinet interiors, rather than a dim golden strip. Viewer area lights were created without Three.js's required WebGL LTC uniform initialization. Added that initialization once at module load; retained one area light per exported emitter and no per-strip shadow maps. The project worker owns the 4300 K product selection and emitter export.

## Tasks

- [x] Inspect the current viewer and installed Three.js initialization requirements.
- [x] Initialize the area-light lookup textures and rebuild the bundled viewer.
- [x] Run focused lighting and exploded-panel tests: eight passed.
- [x] Visually verify neutral-white illumination in the live cabinet preview: shelves and back panels visibly lit with doors hidden in the existing tab.

## Audit log

- User requested white light visibly illuminating shelves and cabinet interiors.
- Confirmed missing `RectAreaLightUniformsLib.init()` in the viewer; vendor source documents it as mandatory for WebGL area lights. Fixed the lighting setup rather than increasing light count or adding shadow maps.
- Bundle build passed; Vite reports the main bundle exceeds its 1500 kB warning threshold after adding the required lookup textures. No CAD geometry changed by this viewer fix.
- Initialization alone was insufficient at the old luminance of 15. Set inspection luminance to 600 for the narrow diffusers; this is a visual review setting, not measured lumens/lux or a product brightness promise. Kept one area light per emitter without shadow maps.
- Excluded the strip lights from the studio-backdrop material to prevent unoccluded light appearing as under-cabinet lighting. Furniture still receives the strip contribution; full inter-panel shadow accuracy belongs to the assembled bake.
- Updated the explosion test to require unchanged positive finite luminance across movement, replacing its obsolete arbitrary sub-100 limit. All eight focused tests pass after the final changes.
- The same loopback viewer now serves furniture_01-white.glb with neutral-white emitter materials and unchanged CAD buffers. Hinge replacement and full manufacturing/motion qualifications remain with the build worker.
