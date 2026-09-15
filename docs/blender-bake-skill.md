# Blender bake skill

## Scope

Package the approved exact-geometry presentation workflow in aikea-review-unit.
Blender is required and automatically provisioned by the skill, including a
compatible isolated Python runtime; an existing desktop installation is not a
prerequisite. The assembled output keeps the accepted lighting and texture
coverage correction. The original GLB remains the source for open/exploded views.

## Work packages

### WP1 — Provision the engine
- [x] Add automatic isolated Python/Blender setup and a real engine probe.
- [x] Verify setup from an empty runtime without using the installed Blender app.

### WP2 — Package the validated bake
- [x] Generalize the tested studio, padded UV packing, coverage bake, lighting
  bake, source preservation, export and independent geometry verification.
- [x] Add a single command with bounded resource defaults and explicit outputs.
- [x] Run the packaged command on the approved dresser and check its artifacts.

### WP3 — Skill routing and review
- [x] Document the required setup, source material contract, assembled/open view
  boundary, visual checks and host capability limits.
- [x] Run focused tests, skill validation and review the complete diff.
- [ ] Commit a coherent local checkpoint; publication remains separate.

## Current state

Implemented on `codex/blender-bake-skill`, stacked on trial commit `723e410`.
The engine-only installation downloaded Python 3.13.3 and official bpy 5.2.1;
Cycles and glTF import/export passed without the installed Blender application.
The missing-uv bootstrap path downloaded its own uv binary and executed it.
Re-running setup reused the installed engine. Runtime and generated Blender files
are ignored; the private dresser and its outputs are not distributed.

The full packaged dresser command passed with 99 physical parts, unchanged source
UVs, identical world-space triangle connectivity, maximum export rounding
0.00042147 mm, and zero missing samples across 330,080 panel triangle centroids.
The 5066 padded islands fit one 4096² atlas at broad-surface scale 0.9, retaining
the six-pixel minimum. The packaged GLB was loaded in the single browser tab;
whole-piece and tabletop/frame close-ups preserve the approved continuous edges.
Evidence is under ignored `local-evidence/packaged-dresser/`.

Four rectangle-layout tests passed. The real-engine independent three-part fixture
also passed through baking and export, then rejected a 10 mm moved part and a
changed input file. Its physical source roundover tests narrow surface coverage.
The fixture required a 1024² atlas; the attempted 512² atlas correctly refused
to shrink the required padding away. Skill metadata and all package links passed.

Verified platform: macOS ARM64. Other published wheels are not platform-tested.
The agent still prepares the material-bearing source according to the active
design's stock/finish; this slice does not select materials or alter CAD. Open
and exploded inspection uses the retained source GLB, with the agent switching
the existing tab; automatic viewer switching and downloadable HTML packaging
are separate outstanding features. No push or merge has been performed.

## Audit log

1. 2026-09-15: Patrick approved the corrected browser appearance and requested
   that the complete flow come with the skill. Reuse its actual geometry and
   appearance checks, rather than leaving a dresser-specific experiment.
2. 2026-09-15: Patrick corrected optional Blender availability: setup belongs to
   the skill. Bundle executable dependency provisioning and test the engine-only
   package from an empty directory. No fallback presented as equivalent quality.
3. 2026-09-15: Executed clean engine-only provisioning, the complete dresser bake,
   independent fixture/negative checks, and missing-bootstrap/reuse paths. These
   verify the required automatic setup instead of relying on the prior app trial.
4. 2026-09-15: Retained the accepted diffuse appearance, 4096² budget and coverage
   correction. Appearance work introduces no construction primitives or renderer
   bevels. Input/output checksums bind the resulting report to its real assets.

## Responsibility review

`review-code-boundaries`: PASS. All production files are new (previous LoC 0);
existing construction, inventory, viewer and server code did not acquire Blender
policy. The feature-owned job coordinates only this rendering workflow. CLI and
worker are separate because provisioning runs outside the isolated engine.

| File | LoC | Coherent responsibility |
| --- | ---: | --- |
| blender_engine_runtime.py | 50 | Isolated dependency provisioning and reuse |
| probe_blender_engine.py | 20 | Required engine capabilities |
| setup_blender_engine.py | 17 | Standalone setup entry point |
| bake_furniture_presentation.py | 38 | CLI, immutable job configuration and worker launch |
| run_blender_bake.py | 16 | Engine-process entry point |
| blender_bake_job.py | 88 | Assemble the feature's stages and deliver checked output |
| blender_furniture_source.py | 91 | Source identities, bounds, mesh/placement/UV preservation |
| blender_furniture_studio.py | 86 | Bounds-scaled lighting, floor and native presentation |
| lighting_atlas.py | 72 | Separate bake coordinates and baked material binding |
| bake_uv_coverage.py | 66 | UV island extraction and pixel-space assignment |
| texture_shelf_layout.py | 37 | Pure rectangle packing independent of Blender |
| panel_bake_pass.py | 95 | Temporary bake mesh and measured coverage |
| blender_export_verification.py | 61 | Independent world-space export comparison |

No production file reaches the 150-line trigger. No extra catch-all exceptions,
speculative recovery loops or duplicated construction rules were introduced.
The material-bearing input remains the material-identity/provenance authority;
the output's shared panel material is an assembled lighting atlas.
