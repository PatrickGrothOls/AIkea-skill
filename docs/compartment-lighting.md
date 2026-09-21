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
pass. User appearance approval remains pending; no fabrication claim is added.

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
