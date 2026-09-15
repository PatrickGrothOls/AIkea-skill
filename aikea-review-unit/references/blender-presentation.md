# Assembled furniture presentation

Use this flow to give the finished furniture the approved browser appearance:
actual CAD → declared materials → studio lighting baked with Blender → interactive
Three.js view. Blender is a required provisioned dependency, not an optional
application the client must already own. The agent runs setup and rendering.

## Runtime comes with the workflow

`scripts/bake_furniture_presentation.py` automatically provisions an isolated
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

Start from the active design's checked, assembled GLB with its actual materials
and part-local texture UVs. Every mesh needs unique
`extras.aikea.inspection_path` and `kind: panel|hardware`. All panels need material
slots and UVs. The command derives part counts from the input; it has no dresser,
wardrobe, panel-count or hardware-count preset. CadQuery review coordinates are
normally millimetres; use `--units m` only for a source actually expressed in metres.

Prepare the material-bearing GLB from the active design's saved selections:

- Give each panel its selected stock and finish. Bind oak, MDF, HDF and hardware
  separately; a material study must not turn everything into wood veneer.
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

Run using the host's activated environment (`direnv exec .` in this repository):

```bash
python <review-skill>/scripts/bake_furniture_presentation.py \
  <assembly>/review/materials.glb <assembly>/review/presentation-01 \
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

Defaults are one 4096² atlas, three CPU threads and 16 lighting samples. Keep
one Blender job and one 3D browser tab at a time. Lower atlas sizes and samples
are available for small acceptance fixtures; they are not the approved dresser
quality setting. Do not increase render budgets in response to a memory crash.

## Delivery checks

Require `presentation.json` with `status: PASS`, matching input/output hashes,
zero uncovered triangle centroids, and the same physical part identities and
world-space triangle connectivity. The comparison permits only export rounding
below 0.002 mm. The detailed reports and `bake.log` stay next to the result.
The centroid check detects the reproduced streaks; also inspect edge close-ups
visually, since it does not prove every texel at every viewing angle.

Show `assembled.glb` with the existing `serve_unit_review.py` command and
`?render=interactive`. Reuse the existing browser tab. Check the full piece and a
close-up of rounded edges, frames and real drawer gaps. The assembled material
contains baked illumination, so do not stack extra edge outlines or ambient
occlusion over it. `source-studio.blend` retains the original materials;
`assembled.blend` contains the packed bake for native inspection.

The browser remains interactive: rotate, pan and zoom the whole furniture.
Opening/exploding parts invalidates the assembled shadows, so serve the original
material GLB in the same tab for those inspection requests. Automatic in-viewer
switching between the two assets is not implemented. Metallic hardware retains
its source material; the panel bake is diffuse and does not recreate all of
Blender's view-dependent reflections.

When a hosted chat cannot expose a local server, retain the model and native
files as downloadable artifacts. An HTML delivery route requires its own tested
asset packaging; a loopback URL inside the hosted runtime is not a client link.
Visual approval and all these appearance checks remain separate from CNC and
fabrication approval.
