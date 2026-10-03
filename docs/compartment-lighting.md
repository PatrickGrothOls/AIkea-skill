# Readable compartment lighting

## Scope

Improve the current wardrobe's interior illumination using the existing LED
diffusers and plausible external room lighting. Preserve all furniture geometry,
plywood surface choices and hardware. Do not invent hidden lights per shelf.

## Current state

The emitting faces point into the cabinets. Their representative emission
strength was 5, while the studio key/fill are high and partly behind the openings.
A small Blender study confirms the interiors remain readable with stronger
existing emitters and broad frontal room light. The reusable studio uses that
setup; the source records representative LED output. The exact purchased strip's
photometry is not yet verified; the render must not be presented as a lux/lumen
simulation or proof of supplier output. The full bake passed all four checks:
123 parts, zero uncovered samples and maximum vertex error 0.000780341 mm.
The existing viewer serves the new checked artifact and was visually verified
while rotating. The 1300 by 1100 overview is rendered and inspected: back panels
and shelves remain readable. Skill validation, Python compilation and diff checks
pass. The user approved the appearance and requested it as the shared default;
no fabrication claim is added. The bake command now applies representative LED
defaults before taking the source hash. It preserves calibrated output, explicit
overrides and the original input. Its returned inspection path identifies the
prepared source so inspection and bake remain paired. These changes are local
on this branch, not published to the installer yet.

## Work packages

### WP1: Inspect and tune

- [x] Inspect actual emitter directions, saved light placement and source settings.
- [x] Render and inspect a small study without changing the furniture.
- [x] Apply the verified room-light setup to the reusable Blender studio.
- [x] Retain representative emitter settings and their provenance in the source.

### WP2: Deliver

- [x] Run the full bake with coverage and export-geometry verification.
- [x] Show the result in the existing single viewer tab.
- [x] Render and inspect the full-resolution overview with compartments visible.
- [x] Review the diff, document validation and commit the focused change.

### WP3: Make the approved appearance the default

- [x] Apply representative LED output in the shared bake entry point.
- [x] Preserve calibrated brightness, explicit overrides and non-emitter materials.
- [x] Document default lighting and the exact prepared inspection-model path.
- [x] Test source preservation, idempotence and CLI source hashing: 27 tests pass
  including the existing runtime and verified-presentation checks.
- [x] Verify the shared studio placement and scaling in Blender 5.2.1: PASS.
- [x] Review the focused diff and record the default-lighting checkpoint.

## Audit log

- 2026-09-21: User requests better illumination inside the compartments. The
  existing strips face inward correctly, so the initial correction targets
  their rendered output and external studio light placement, not cabinetry.
  The material and geometry remain the same. A small study avoids repeating a
  full bake if this lighting choice is ineffective.
- 2026-09-21: The small study confirmed that frontal room fill and inward strip
  emission make the recesses readable. Source comparison proves all geometry,
  UVs, embedded textures, transforms and non-LED materials unchanged. The full
  bake passed the same geometry tolerance; source emission alone changes from
  5 to representative 40. Studio sources remain outside the furniture.
- 2026-09-21: User approves this appearance and explicitly asks that it always be
  the viewer default. Reuse the existing room setup and normalize explicitly
  representative emitters to 40 before source hashing. This removes the remaining
  project-local brightness dependency without replacing product calibration or
  changing the existing approved render. Retain the simple live inspection mode;
  moved parts must not carry stale assembled shadows.
