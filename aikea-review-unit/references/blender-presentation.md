# Assembled furniture presentation

Use this flow to give the finished furniture the approved browser appearance:
actual CAD → declared materials → studio lighting baked with Blender → interactive
Three.js view. Blender is a required provisioned dependency, not an optional
application the client must already own. The agent runs setup and rendering.

## Runtime comes with the workflow

`scripts/bake_furniture_presentation.py` reuses its existing provisioned runtime
or an installed `blender` CLI, with the same exact-version/background/Cycles/glTF
probe before baking. `--blender-executable <path>` selects a known installation
outside PATH. It needs no GUI interaction, including on a locked Mac.
If neither runtime exists, it automatically provisions an isolated
Python 3.13 and Blender's official `bpy==5.2.1` engine package. It uses `uv`,
installing the pinned bootstrap tool into the runtime directory if absent. This
does not modify the project's CadQuery environment or require Blender's UI.
Choose a writable runtime directory in the active workspace and reuse it.

To prepare the engine independently, run:

```bash
python <review-skill>/scripts/setup_blender_engine.py <workspace>/.aikea-runtime
```

The probe requires background execution, Cycles and glTF import/export. Setup is
idempotent for a working runtime. The pinned official package provides macOS ARM64,
Windows x64/ARM64 and Linux x64 wheels; actual acceptance is currently verified
on macOS ARM64. A compatible Linux system also needs the native libraries required
by Blender. Do not claim a successful installation from a package download alone.

The host must permit code execution, network downloads and a writable directory.
If installation or execution is blocked, explain the specific missing capability
and retain the unfinished presentation task. Do not silently substitute the old
appearance or ask the client to operate Blender when the agent can do the work.
The engine runs wherever the assistant has execution access; this does not grant
a hosted chat access to the client's computer.

Official sources: [Blender Python module](https://docs.blender.org/api/main/info_advanced_blender_as_bpy.html)
and [pinned Blender package](https://pypi.org/project/bpy/5.2.1/).

## Source contract

First apply [material appearance](material-appearance.md). Exposed cores and
edge treatments must match the saved physical build before a material GLB is
baked; a passing geometry/coverage report cannot validate an invented finish.

Start from the active design's checked, assembled GLB with its actual materials
and part-local texture UVs. Every mesh needs unique
`extras.aikea.inspection_path` and `kind: panel|hardware`. All panels need material
slots and UVs. The command derives part counts from the input; it has no dresser,
wardrobe, panel-count or hardware-count preset. CadQuery review coordinates are
normally millimetres; use `--units m` only for a source actually expressed in metres.

Prepare the material-bearing GLB from the active design's saved selections:

- Give each panel its selected stock and finish. Bind oak, MDF, HDF and hardware
  separately; a material study must not turn everything into wood veneer.
- Wood, MDF and HDF require explicit nonmetallic source materials. Raw CadQuery
  colours now receive `metallicFactor: 0` for identified panels because omitting
  it imports as fully metallic in Blender and produces an empty diffuse bake.
  This is a placeholder default, not material selection. Preserve declared
  metal finishes and hardware materials; do not force real metal into a wood bake.
- Scale grain in physical units and orient it to that panel's selected direction.
  Keep broad veneered faces distinct from exposed sheet cores. Use the bundled
  `assets/viewer/materials/oak-veneer/SOURCE.md` for optional map provenance.
- Keep unselected products/coatings explicitly representative. Retain that
  provenance alongside the input; a good render does not select a supplier.
- Preserve original position, normal and index buffers, transforms, part identity
  and count when adding material and UV data. Verify that first conversion too.

Roundovers, bevels, grooves and edge profiles must already exist in the CAD and
its machining or secondary-finishing plan. Never add them as render modifiers.
The bake preserves the input meshes and all existing source UV coordinates.
It cannot prove the input already matches an earlier CAD file unless that
upstream conversion has been checked.

## One command

The approved default is broad frontal room fill, soft ambient illumination and
low-contrast AgX, already installed by `BlenderFurnitureStudio` on every bake.
For installed LED emitting faces without verified output, retain the chosen light
colour and set material `extras.aikea.appearance_status: representative_output`
and `photometric_calibration: false`, with a nonzero `emissiveFactor`. The command
automatically applies the approved representative emission strength of 40 before
hashing its source. This is a presentation value, not a wattage or lumen claim.
Do not assign emission to wood, hardware housings or nonexistent lights.
Calibrated output is preserved. An explicitly requested representative override
uses `extras.aikea.preserve_emission: true`; record the user's choice in the brief.

When defaults change a material, the command writes `inspection-materials.glb`
and `lighting-defaults.json` inside the new presentation directory. All geometry,
textures and non-emitter materials are preserved, and the original input is
untouched. Always use the `inspection_model` path from the resulting
`presentation.json` when serving; it identifies the exact source used for baking.
Existing presentations keep their recorded appearance until deliberately rebaked.

First consolidate the static material GLB for efficient import and inspection:

```bash
python <review-skill>/scripts/pack_review_meshes.py \
  <assembly>/review/materials.glb <assembly>/review/materials-packed.glb
```

Require the adjacent packing report to pass. This combines compatible surfaces
within each part and material; it preserves indexed positions, normals and UVs
bitwise, plus node transforms and identities. It does not simplify geometry.
Use the packed result as the bake source and matching inspection model. Static,
unskinned, embedded-buffer triangle GLBs are supported; animated or unsupported
primitive data must use a compatible export, never be silently discarded.

Run using the host's activated environment (`direnv exec .` in this repository):

```bash
python <review-skill>/scripts/bake_furniture_presentation.py \
  <assembly>/review/materials-packed.glb <assembly>/review/presentation-01 \
  --runtime-directory <workspace>/.aikea-runtime
```

Use a new output directory per run. The command provisions the engine, sets up a
studio scaled to the furniture bounds, keeps a native material scene, then:

1. Creates separate bake UVs without changing the source material UVs.
2. Reserves at least six content pixels across each UV island, plus eight pixels
   of padding on every side. This prevents the observed subpixel edge streaks.
   Packing cannot rescale these minimum widths away. If the atlas cannot fit,
   stop and resolve the layout instead of claiming successful quality.
3. Bakes constant white and checks every panel triangle's UV centroid. Missing
   coverage stops the flow before the expensive lighting bake.
4. Bakes diffuse colour, direct and indirect illumination. Only the temporary bake
   mesh is joined; export reloads the original separate furniture objects.
5. Checks source meshes, placements and UVs, exports the baked GLB, independently
   reimports it and compares world-space triangles and part identities.
6. Requires finite, nonzero lighting at actual panel triangle samples. An empty
   atlas writes failed `lighting-signal.json` and cannot produce a PASS summary.
   This check detects the black-bake failure; it does not prove interior readability
   or replace the visual inspection below.

Defaults are one 4096² atlas, one CPU thread and 16 lighting samples. Keep
one Blender job and one 3D browser tab at a time. Lower atlas sizes and samples
are available for small acceptance fixtures; they are not the approved dresser
quality setting. Do not increase render budgets in response to a memory crash.

On a restricted host, a Blender CLI crash before Python at Metal/device discovery
can be an execution-permission problem. Retain the log and try the same tiny
background engine probe through the host's authorized execution flow. Do not
duplicate the installation, change lock/security settings, or bypass a rejection.
Check free disk before provisioning or accumulating another bake. The previous
artifact remains the review reference until all checks for its replacement pass.

## Delivery checks

Inspect interior lighting as well as the exterior. The studio uses broad frontal
room light so deep compartments remain readable. Verify each installed diffuser
emits toward the usable interior, rather than merely showing a bright line.
Keep emitter geometry and placement tied to the actual light component; do not
hide invented lamps inside compartments to conceal a poor physical layout.
Use the selected product's output when it is known. Otherwise retain explicit
representative-output provenance and do not claim measured lux, lumens or a
supplier-calibrated lighting simulation. Adjust illumination before baking, not
the wood colour or a finished screenshot to make the interior look brighter.

The shared viewer enforces this contract before binding a port or opening a tab.
It requires the adjacent `presentation.json`, all five detailed check reports,
and `--inspection-model`. Both model hashes must match the snapshotted files;
coverage and geometry evidence must pass at the existing 0.002 mm tolerance.
The presentation must use the approved 4096 atlas and at least 16 samples.
Reduced-budget engine probes remain installation tests and cannot be shown as
furniture presentations. Supplying a second GLB does not establish a bake.
Older presentations without `lighting-signal.json` require a fresh bake through
the updated command. Do not manufacture a report for an existing atlas.
Keep these reports beside `assembled.glb` when moving or packaging a presentation.
Do not edit reports to make a raw or stale model pass; regenerate the bake.
Decision records remain bound to the exact primary GLB displayed. If an existing
record names an earlier CAD export, regenerate its proposal through the existing
review-record workflow for the verified presentation while retaining the current
construction evidence. Do not manually substitute approval hashes.

Require `presentation.json` with `status: PASS`, matching input/output hashes,
zero uncovered triangle centroids, and the same physical part identities and
world-space triangle connectivity. The comparison permits only export rounding
below 0.002 mm. The detailed reports and `bake.log` stay next to the result.
The centroid check detects the reproduced streaks; also inspect edge close-ups
visually, since it does not prove every texel at every viewing angle.

Export verification reads the GLB's world transforms directly and requires a
one-to-one correspondence of oriented triangles within the same 0.002 mm limit.
It preserves triangle multiplicity and winding. A nearest-vertex map alone is
insufficient: nearly coincident hardware vertices can collapse at float32
precision and produce a false mismatch. Failed checks still block delivery;
never increase the tolerance to make an export pass.

Show `assembled.glb` with `serve_unit_review.py assembled.glb --inspection-model
<matching-source-materials.glb> --no-open` and `?render=interactive`. Reuse the
existing browser tab. Check the full piece and a
close-up of rounded edges, frames and real drawer gaps. The assembled material
contains baked illumination, so do not stack extra edge outlines or ambient
occlusion over it. `source-studio.blend` retains the original materials;
`assembled.blend` contains the packed bake for native inspection.

The browser remains interactive: rotate, pan and zoom the whole furniture.
Opening/exploding parts invalidates the assembled shadows. The viewer automatically
switches to the matching original material GLB supplied with `--inspection-model`.
Reset restores the bake; each switch disposes the previous model's resources.
Inspection keeps the actual emitters and modest live lights without running a
path tracer. Metallic hardware retains
its source material; the panel bake is diffuse and does not recreate all of
Blender's view-dependent reflections.

When a hosted chat cannot expose a local server, retain the model and native
files as downloadable artifacts. An HTML delivery route requires its own tested
asset packaging; a loopback URL inside the hosted runtime is not a client link.
Visual approval and all these appearance checks remain separate from CNC and
fabrication approval.
