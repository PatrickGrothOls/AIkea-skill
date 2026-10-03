# Interactive material fidelity

## Scope

Improve the actual rotating dresser while preserving its manufacturing geometry.
Stacked on `2bd3c1d` from `codex/viewer-photo-quality`; refreshed origin/main.
Patrick explicitly requires every physical edge detail to exist in CAD and the
manufacturing process. No display-only bevel, displacement, or artificial joints.
Use one browser tab and retain the inherited render budget.

The realism target is the assembled furniture while the camera orbits it.
Patrick accepts a simpler, plastic-looking exploded view. Keep inspection
lightweight; matching its lighting to the assembled presentation is not required.

## Work packages

### WP1 — Preserve declared materials
- [x] Inspect the actual dresser's source material declarations and GLB.
- [x] Source a photographed oak-veneer texture with redistribution permission.
- [x] Respect supplied glTF materials instead of overwriting them with plywood.
- [x] Prepare a material-bearing copy of the exact dresser and verify geometry.
- [x] Review material ownership and fidelity with the code-boundaries skill.

### WP2 — Interactive presentation
- [x] Improve real-time grounding and small contact shadows.
- [x] Build and run focused tests for material and geometry preservation.
- [x] Verify rotation, drawer inspection, restoration, and memory in one tab.
- [x] Save actual screenshots and review/commit the completed slice.

## Current state

Implementation and live interactive checks passed; local checkpoint complete.
The viewer respects authored glTF surfaces, including explicitly untextured HDF.
The material study of the existing dresser carries photographed oak veneer,
untextured sheet cores/rails, and eight 6 mm HDF bottoms. Its original 59 panels
and 40 hardware items are intact. The saved design proposes oak-veneered panels;
exact supplier stock and coating remain unselected. This is a representative
material study, not a supplier color match or fabrication approval.

The single existing tab serves the material study on port 51344 in interactive
mode. The source exporter does not yet automatically assign these material IDs:
this slice supports authored materials and proves them with the existing dresser.
Study preparation scripts and generated models remain under ignored
`local-evidence/`, separate from the reusable viewer and licensed material assets.
Blender 5.2.1 headless Python execution is now verified locally; the lighting-bake
and browser-export pipeline itself remains unimplemented and untested.

## Validation and evidence

- `direnv exec . npm --prefix viewer test`: 55 passing tests. New coverage checks
  authored wood, untextured HDF, and the legacy fallback; existing inspection and
  bounded photo-session tests remain green.
- `direnv exec . npm --prefix viewer run build`: passed. No new dependencies.
- An independent read of the saved GLBs compared all 10,274 surface primitives.
  Original binary data (12,108,048 bytes), positions/normals/indices, hierarchy,
  transforms, and all hardware geometry/materials are identical. Only panel
  materials and appended texture/UV data differ. Evidence:
  `local-evidence/geometry-comparison.json` and `material-provenance.json`.
- Browser: rotated a drawer, inspected left drawer 01 and right drawer 04,
  restored all 99 pieces twice, and reloaded the assembled view. HDF remains
  distinct and fittings remain visible. Actual screenshots are
  `local-evidence/dresser-materials-final.png` and `drawer-materials.png`;
  no generated image is used as proof.
- One viewer tab/server was used. Observed likely viewer renderer RSS was about
  198 MiB after inspection (pid 32634), versus about 178 MiB after initial loading.
  This is a process snapshot, not a GPU-memory measurement or long-duration leak
  test. Live photo mode was not exercised in this slice.

## Code-boundaries reviews

WP1: **PASS**. `ReviewMaterialSurface` owns the generic choice between authored
surface and legacy fallback, plus bounded texture filtering. `ReviewModel`
composes it without learning dresser part names, oak/HDF rules, or stock choices.
The model-specific study stays outside shipped production code. The review skill
reference now explains material identities, geometry fidelity, and finish limits.

WP2: **PASS**. Studio lights own key/fill placement and their shadow camera;
renderer configuration owns shadow-map settings; contact shading owns small
screen-space occlusion. None owns physical furniture geometry or material policy.
No new defensive branches or exception wrappers were added.

| Production file | Before | After |
| --- | ---: | ---: |
| ReviewMaterialSurface.js | 0 | 20 |
| ReviewModel.jsx | 69 | 71 |
| AssemblyStudioLights.jsx | 67 | 88 |
| AssemblyContactShading.jsx | 18 | 19 |
| ReviewRenderer.js | 10 | 12 |

All changed production files remain below the 150-line review trigger. The new
material test is 45 lines. No subagent size-refactor report is required.

## Audit log

1. Patrick approved material/light improvements while requiring full CAD fidelity.
   Use the existing 99-part HDF-bottom dresser; do not substitute another design.
2. Source `captured-drawer-bottom/local-evidence/project/assemblies/dresser_01/`
   declares oak-veneered 16/22/24 mm panels, prepared plywood rails, and HDF bottoms.
   Existing 0.8/1/2 mm edge finishing is already in the CAD and remains untouched.
3. Downloaded Poly Haven Oak Veneer 01 by Jenelle van Heerden through its public
   page, which specifies CC0 and a 1.8 m texture width. Only diffuse, normal, and
   roughness maps are used; no displacement or baked assembled shadows.
4. Reuse the existing browser tab for material sourcing and review. The original
   interactive screenshot is saved under ignored `local-evidence/`.
5. Preserve standard glTF PBR data rather than applying a blanket plywood material.
   The prototype copies source binary geometry unchanged and adds UV/material data.
   This implements Patrick's approved CAD-fidelity requirement without a Blender
   dependency or renderer-only edge treatment.
6. Reduced the key-light intensity and broad ambient-occlusion halo; added a bounded
   2048-square real-time shadow map. Replaced a deprecated Three.js shadow setting
   observed during live checking with its supported equivalent.
7. WP1/WP2 boundary reviews passed, 55 tests and the production build passed,
   and saved-file geometry comparison and interactive drawer restoration passed.
   Exact finish selection and general exporter material assignment remain separate
   work; neither is implied by this visual study.
8. Patrick clarified that exploded inspection may look plastic. Prioritize the
   assembled rotating view. This makes baked assembled lighting a viable candidate
   without requiring those static shadows to stay correct during explosion.
   A scripted Blender preparation stage is being discussed; no bake pipeline
   has been implemented or validated yet.
9. On 2026-09-15, tested installed Blender 5.2.1 with `--background`, factory
   startup, disabled auto-execution, one thread, and a tiny Python expression.
   It reported `bpy.app.background == True` and exited successfully without a UI.
   The restricted run crashed during Metal initialization; the identical command
   passed outside the sandbox. This proves headless execution only, not baking.
   No connected Blender MCP was found; direct Python control is available.
