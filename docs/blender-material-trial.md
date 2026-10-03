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
- [x] Confirm the browser quality target: Patrick accepts the current appearance;
  a controlled Blender/browser comparison is no longer required for this trial.

### WP4 — Explain black edge lines

- [x] Locate the black values in the exported atlas at tabletop edge coordinates.
- [x] Isolate texture coverage from illumination with a constant-white emission bake.
- [x] Measure the affected UV strip and identify the missing texel coverage.
- [x] Give narrow edge islands sufficient texture coverage and padding, rebake,
  and visually verify the correction without changing furniture geometry.

### WP5 — Apply reliable coverage across the dresser

- [x] Allocate a minimum usable width to every panel's narrow bake UV islands.
- [x] Prove constant-white coverage before the full lighting bake.
- [x] Rebake the approved materials and lighting within the existing texture budget.
- [x] Verify exported geometry and inspect the repaired edges in the one browser tab.
- [x] Review responsibility boundaries and record the verified result.

## Current state

Whole-dresser correction is complete and visually checked. Explicit packing fits 5,066 padded UV
charts in one 4096-square atlas, with at least six pixels of content width and
eight pixels of padding per side. Independent rectangle checks find no overlap
or out-of-bounds allocation. Broad-surface texel density is 90% of the first study;
the stock grain scale and source UVs are verified unchanged. The constant-
white regression bake passes all 330,080 triangle-centre samples across 59 panels,
with zero uncovered samples. Full lighting rebake, export, and browser close-up
verification passed. The prior 48 front-edge and 42 back-edge black samples are
both zero in the corrected exported tabletop. All 99 parts retain identical
triangle connectivity with maximum world-space rounding error 0.000438 mm.
The viewer's tabletop and frame edge strips are visibly continuous at close range;
actual drawer reveals and contact shadows remain.

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
existing Three.js tab at `http://127.0.0.1:60693/?render=interactive&title=Dresser%20%E2%80%94%20corrected%20edges`.
Browser orbiting was visually verified from front/right to the right side, then
returned to a useful front angle. Only one in-app browser tab is open. Native
Blender viewport interaction and sustained browser performance remain untested.
Patrick explicitly approved the current browser appearance as the desired quality
level. Further photorealism or material-style refinement is not a prerequisite.
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
| `dresser-covered.glb`, `dresser-covered.blend`, `dresser-covered-reference.png` | Corrected whole-dresser presentation and its native comparison image |
| `covered-uv-packing-check.json`, `all-panel-coverage.json` | Padded rectangles have no overlap; all 330,080 triangle-centre coverage samples pass |
| `covered-source-uv-check.json`, `covered-export-geometry.json` | Original grain UVs unchanged; all 99 exported parts retain source geometry |
| `covered-edge-regression.json` | Formerly black tabletop-edge samples drop from 48 + 42 to zero |

The photographed oak texture represents unselected stock, not a supplier-approved
finish. Patrick accepts its current appearance; the earlier subjective concern
about busy grain is not a blocker. The atlas stores diffuse color and direct/indirect lighting at
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

## Black edge diagnosis

The reported tabletop line is a missing-coverage artifact in the baked texture.
It is present in the exported image itself, not a newly created CAD gap. A local
diagnostic sampled the actual exported tabletop triangles and their UV coordinates.
On the upper front round, 48 of 86 sampled triangle centroids read black. The upper
back round has 42 of 86; the two broad top-face triangles are correctly coloured.

A second headless Blender bake replaced the tabletop shader with constant white
emission. This removes lighting, shadow, and material colour as explanations.
The same 48 front-edge and 42 back-edge centroids remained black. The affected
front-edge UV strip spans x=1286.68396 to 1287.48682 in a 4096-pixel atlas: only
0.80286 pixels wide, entirely between pixel centres 1286.5 and 1287.5. No pixel
centre covers that strip. The bake's five-pixel margin did not recover it.

Evidence: `local-evidence/edge-coverage-comparison.json`,
`local-evidence/subpixel-edge-proof.json`, `local-evidence/top-uv-coverage.png`,
and `local-evidence/top-uv-coverage.log`. The probe modifies no saved scene, CAD,
viewer asset, or current browser view. The source atlas remains unchanged.
`inspect_bake_seams.py` owns reading/sampling the GLB; `probe_top_uv_coverage.py`
owns the separate constant-white bake. Both are ignored trial scripts below
150 lines; no production file or geometry changed.

Minimum-width UV allocation/packing and suitable padding, followed by rebaking,
now pass the coverage, geometry, and browser checks described above. Do not remove actual drawer reveals or joints
as a cosmetic workaround. Other similar fine rounded-edge lines have the same
visual signature, but the white-bake isolation above specifically proves the
tabletop case; it does not classify every dark line on the assembly.

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

WP5 **PASS for the isolated experiment**, using review-code-boundaries.
`texture_shelf_layout.py` (37 lines) owns padded rectangle placement;
`bake_uv_coverage.py` (66) owns connected chart coordinates and pixel allocation;
`panel_bake_pass.py` (94) owns the temporary combined bake and coverage sampling;
`prepare_covered_bake.py` (35) and `run_covered_bake.py` (19) are entry points;
`export_covered_dresser.py` (74) restores original objects, checks source UVs, and
exports their materials and verifies source grain UVs. The independent export verifier is 72 lines and the
sampling inspector is 69. No existing production runtime changed, and no trial
file exceeds 150 lines. The source UV, coverage, geometry, and actual browser
close-up gates all passed. This remains local trial tooling; the reusable skill
has not yet been shipped with a packaged Blender bake command.

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
9. Patrick approved the current browser quality and requested an explanation of
   black edge strings. The tabletop case is traced to subpixel UV coverage and
   independently reproduced with constant-white emission. Record the correction
   as pending; this request was diagnosis, not a new material or CAD design.
10. Patrick asked how to solve coverage for the whole piece. Apply the diagnosed
    correction to every panel, preserve approved geometry/materials/lighting, and
    verify the actual corrected export. Keep the texture budget bounded instead
    of increasing resolution globally without addressing narrow islands.
11. Expanding thin islands then using Blender's rescaling packer did not retain the
    required width (measured minima below one pixel). Replace that attempt with
    explicit padded pixel rectangles. The first fitting layout uses 90% broad-
    surface density and a six-pixel minimum; actual white coverage passes for
    every sampled triangle. No blanket resolution increase or CAD change is used.
12. Full rebake passed. Reimport preserves 99 parts and source triangle connectivity;
    original grain UV hashes match. The former 90 black tabletop-edge samples are
    zero. The same browser tab shows the corrected export; close-up inspection
    confirms continuous tabletop/frame edges with real drawer gaps retained.
