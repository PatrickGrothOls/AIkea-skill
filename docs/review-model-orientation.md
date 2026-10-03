# Preserve exported model orientation

## Scope and current state

Branch `fix/review-model-orientation`, based on `7c4109d`. Fix one demonstrated
viewer defect: CadQuery already converts native Z-up to glTF Y-up. The extra
scene rotation made native height become browser depth. Implemented, built and independently reviewed locally.

## Work package and tasks

- [x] Confirm the exported root transform independently with the real GLTF loader.
- [x] Remove the extra model rotation; retain the studio floor's own plane rotation.
- [x] Review the viewer's responsibility boundary before editing.
- [x] Check native axes and actual exported dimensions after loading in Three.js.
- [x] Build the packaged viewer and inspect a fresh standing-model page.
- [x] Complete the review skill and resolve findings.

## Audit log

1. The lighting browser trial exposed an inherited viewer problem outside lighting
   construction. Both direct inspection and the independent reviewer confirmed
   native Z maps to Three Y at the exported root, then incorrectly to Three -Z
   after the viewer's extra rotation.
2. The inherited viewer file is 144 lines and has a coherent loading/material/
   framing lifecycle. The independent scope review requires no refactor for this
   one-line fix. Keep material loading, camera policy and studio-floor geometry
   unchanged; reload the page rather than relying on a cached hot-reload scene.

## Verification

The real nested GLB's host, light body and emitter bounds each match the native
construction report under the required mapping `(x, z, -y)`, within 0.01 mm.
Its native 400 mm height is 400 mm in the browser's vertical axis, and one emitter
remains one light. A fresh app-browser page shows the panel standing upright;
orbiting exposes the horizontal light on its correct face. No console errors.

The review skill's independent testing review exported a known 600×500×2200 mm
cabinet and a 600×500×100 mm base through the unchanged exporter. Three.js loads
them as 600×2200×500 and 600×100×500 mm respectively. Raycasting from the viewer's
top/bottom cameras hits the correct native top/bottom faces. All repo GLB producers
use this exporter; no consumer needs a second rotation. Review is clean.

The packaged Vite build passed. This one-line presentation correction changes no
manufacturing geometry or saved assembly placement. Current-axis evidence is local;
remote CI and workshop approval are separate.

3. The actual browser and independent analytic cabinet/base checks agree. Close
   this viewer correction before continuing the component migration.
