# Lighting in complete-assembly review

## Scope and current state

Branch `feat/lighting-assembly-review`, based on `8db3ce5`. Implemented and reviewed locally. Make the owned lighting component appear in the common tree viewer,
including nested assemblies. Retire the lighting command's mandatory KA5332
drawer path. Keep view state distinct from removing the physical feature.

## Work package and tasks

- [x] Register a lighting review contribution using the existing feature contract.
- [x] Present one body plus an optional emitter with current owner/parent placement.
- [x] Check current owned-body identity and manufactured-part clearance.
- [x] Route the old lighting command through the generic complete assembly path.
- [x] Recognize emitter/body role markers after nested assembly names in the viewer.
- [x] Verify flat/nested on/off, removal, clearance, exact inventory and CLI output.
- [x] Build the viewer bundle and inspect a real generated model in the browser.
- [x] Review with the review skill and resolve findings.

## Evidence boundary

On/off changes emitted-light presentation while retaining the installed body,
groove and purchase. Unregistering the component removes construction on rebuild.
Body/groove geometry and manufactured-part clearance within the owner subtree are checked; aim/appearance,
parent/sibling manufactured parts, other hardware/movement clearance and electrical installation remain separate
design/fabrication checks. The compatibility report is explicitly a geometry
preview, bound to the generated GLB, rather than a manufacturing approval.

## Audit log

1. Reuse generic owner-frame overlays and source hydration. No runner family,
   cabinet dimension recipe or separate assembly tree is required to view a light.
2. Preserve nested owner names in mesh identity and recognize reserved light-role
   markers in those names. The viewer still derives light position from the actual
   exported emitter geometry.

## Validation and review

The focused Python lighting/construction/review checks passed, including an
inactive retained plan, a changed purchased temperature, an independently restored
uncut host, nested parent placement, on/off/removal and hidden-ancestor overlays.
The viewer's 26 Node checks passed; its packaged Vite build and all nine skill
packages validate. All changed handwritten code files are below 150 lines.

Actual add-lighting and legacy lighting-review CLI commands succeeded on a fresh
custom project with no drawer or hardware-directory input. The common review CLI
exported the same feature under a rotated parent. Three's actual GLTF loader and
the app browser both resolve six emitter primitive meshes to exactly one light.
The browser displayed the model with lighting on/off, with no console errors;
the existing Three.Clock deprecation warning remains.

The review skill's independent testing review is clean after fixes: include the
door provider in CLI imports; group real GLTF primitives; reject inactive host
plans; compare the exact purchase variant; scope clearance claims to the owner
subtree; and hide overlays when their ancestor is removed. These are local
tooling checks, not remote CI or fabrication approval.

The browser also exposed an existing extra model rotation in
`AssemblyReviewViewer.jsx`: CadQuery already converts native Z-up to glTF Y-up.
That correction, native-axis proof and standing-model screenshot are the next
separate viewer slice. Lighting's current owner-frame geometry remains correct.

## Audit log continuation

3. Actual browser evidence found duplicated light sources despite the initial
   synthetic mesh test passing. Grouping now follows the exported parent identity;
   repeated run IDs in different assembly owners remain separate lights.
4. Review identified stale saved plans and variant-only edits. The active saved
   review plan and owned purchase must agree before exporting a lighting preview.
5. Review identified child overlays surviving parent removal. Common rendering
   now applies the same hidden-subtree rule to owner-bound overlays.
6. Keep the owner-subtree collision boundary explicit; whole-design interactions
   and fabrication remain separate checks. Track the pre-existing viewer rotation
   independently so this component slice stays reviewable.
