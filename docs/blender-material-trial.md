# Blender material and lighting trial

## Scope

Use the installed Blender 5.2.1 to prepare the existing 99-part dresser, produce
an actual Cycles image, save an orbitable Blender scene, and test lighting baking
and GLB export. Stacked on `0527473` from viewer-material-fidelity; origin/main
was refreshed before creating this isolated trial. No CAD finishing may be added.
The assembled view is the realism target; simple exploded shading is acceptable.
Keep one viewer and one Blender process at a time, with bounded render settings.

## Work packages

### WP1 — Exact model and Blender presentation

- [x] Confirm source model, material provenance, installed Blender, and free space.
- [x] Import the exact dresser and record its geometry before presentation work.
- [x] Set up materials, photographic lighting, camera, and a simple studio floor.
- [x] Render an actual image and save a packed, orbitable Blender scene.
- [x] Verify unchanged furniture geometry and review responsibility boundaries.

### WP2 — Bake and browser preparation

- [x] Bake lighting on the assembled CAD geometry with a bounded texture budget.
- [x] Export a material-bearing GLB and verify it can be imported again.
- [x] Compare geometry/part identity and document appearance limitations.
- [x] Review the trial and record the next reusable skill implementation slice.

### WP3 — Client inspection

- [x] Show actual Blender render images in this conversation.
- [x] Load the baked GLB in the existing Three.js tab and visually verify orbiting.
- [ ] Open the prepared Blender scene and verify orbiting when the Mac is unlocked.
- [ ] Match camera, colour handling, and lighting for a controlled Blender/browser comparison.

## Current state

The installed Blender produced a 1100 x 800 Cycles render in approximately
34 seconds, using three CPU threads, 48 samples, and denoising. The packed
`local-evidence/dresser-studio.blend` is saved (about 31 MB); its 99 furniture
meshes, with 925,484 vertices and 974,096 faces, pass the before/after geometry
check. Only units, materials, lighting, camera, and the separate studio floor are
presentation concerns. The source GLB remains unchanged. The bake completed on
59 panels into one 4096 x 4096 atlas (4.3 MiB compressed PNG). The bake and first
reference render took approximately eight minutes; this is a preparation cost,
not a measurement of interactive rendering. The exported GLB is 33.6 MiB.
Reimport verification passed: 99 physical parts, identical world-space triangle
connectivity, maximum vertex rounding difference 0.000438 mm. No additional
Blender or bpy package has been downloaded.
Patrick returned and unlocked the Mac. The baked GLB is now displayed in the
existing Three.js tab at `http://127.0.0.1:58686/?render=interactive&title=Dresser%20%E2%80%94%20Blender%20bake`.
Browser orbiting was visually verified from front/right to the right side, then
returned to a useful front angle. Only one in-app browser tab is open. Native
Blender viewport interaction and sustained browser performance remain untested.
The package-only bpy installation test remains separate from this installed-engine
trial, following Patrick's instruction to show the Blender outcome first.

## Evidence and limits

All trial scripts and generated assets are kept in ignored `local-evidence/`;
this branch records an experiment, not a shipped rendering feature.

| Evidence | What it establishes |
| --- | --- |
| `dresser-cycles.png`, `dresser-cycles-second-angle.png` | Actual installed-Blender rendering of the assembled source geometry |
| `dresser-studio.blend` | Packed original material scene for Cycles presentation |
| `dresser-baked.blend`, `assembled-lighting.png` | Separate baked diffuse-lighting presentation; original material scene remains available |
| `dresser-baked-study.glb` | Embedded baked texture and 99 individually identifiable furniture meshes; no studio floor/camera/lights exported |
| `blender-geometry-check.json`, `bake-geometry-check.json` | Original mesh coordinates, topology, and placements unchanged by styling and UV/bake preparation |
| `export-geometry-check.json` | Independent Blender reimport and world-space triangle comparison |

The photographed oak texture represents unselected stock, not a supplier-approved
finish. It remains visually busy; successful rendering is not proof of a convincing
finished product. The atlas stores diffuse color and direct/indirect lighting at
one assembled configuration. It does not preserve view-dependent specular response,
normal-map detail, or correct lighting after opening/exploding parts. Export uses
an emissive texture over black PBR base; it is not a verified browser light-map
integration or `KHR_materials_unlit` export. Hardware retains its own material.
The native baked reference uses Eevee so baked radiance is not traced again as
new emitted light onto other objects. Keep the full material scene as the quality
reference, and treat the bake as a transport experiment. The first browser import
visibly retains grain and baked shading, but appears darker and flatter than the
Cycles render. Different camera framing, tone mapping, environment, floor, and
live hardware lighting prevent assigning a numerical quality loss. Browser shader
matching remains a separate step; the current result is deliberately the existing
viewer displaying the unchanged baked export.

The next reusable slice should accept a source GLB and an explicit material
specification, preserve geometry/part identity, and produce an assembled-only
presentation asset. Qualify browser shading and compare orbiting before enabling
it in the skill. Do not change the approved construction/CNC pipeline for styling.

## Boundary review

WP1 **PASS**, using review-code-boundaries. Source import and geometry fingerprinting
belong to `dresser_source.py`; lighting, floor, and camera belong to
`dresser_studio.py`; `render_dresser.py` only sequences the trial. No scene styling
was added to the reusable construction runtime. All are new ignored experiment
files under 150 lines. No existing production code was changed.

WP2 **PASS for the isolated experiment**, using review-code-boundaries.
`lighting_atlas.py` owns unique UVs, bake targeting, and the baked material;
`bake_dresser.py` sequences scene loading, baking, and selected-furniture export;
`verify_blender_export.py` independently verifies imported world-space triangles;
`prepare_presentation.py` owns saved viewport settings and comparison images.
No reusable core learned dresser-specific material or rendering policy. Production
code line counts are unchanged (zero production files modified). Every new trial
script remains below 150 lines. This verdict covers responsibility placement,
not interactive quality or manufacturing approval.

## Audit log

1. Patrick requested a test using installed Blender and a direct Blender presentation
   that can be rotated. The exact source CAD and purchased hardware remain fixed.
2. Photorealism is required for the assembled presentation; exploded inspection
   may use simpler shading. No UI-only physical finishing is permitted.
3. Use small, bounded renders first because the Mac previously ran out of memory.
   No new browser tabs or competing render jobs will be started.
4. WP1 passed with a real Cycles render and a saved scene. The oak texture remains
   representative of unselected stock; no coating, bevel, or machined feature was
   added. The first actual render was shown in the conversation.
5. Baking and GLB reimport passed. Preserve the measured geometry result separately
   from appearance: fixed diffuse radiance is an incomplete substitute for live
   material response. Keep the full material scene for the requested Blender test.
6. Patrick confirmed he is away from the Mac. Complete offline artifacts and mobile
   images; leave native orbit and browser presentation verification unresolved.
7. Save bounded Cycles preview settings (24 samples, denoising) and a separate Eevee
   baked scene. A second real Cycles camera angle is generated without changing CAD.
8. Patrick requested the next test in the 3D viewer and confirmed the Mac is unlocked.
   Reused the existing tab for the baked GLB, visually verified rotation, and left
   the assembled view open. No extra renderer tab or Blender process was started.
   No code or geometry changed; only this experiment record was updated.
