---
name: aikea-build-units
description: Generate populated local assembly, part, builder, and joint folders from a completed AIkea assembly run. Use immediately after unit arrangement or when rebuilding or checking a project's local unit taxonomy.
---

# AIkea build units

Before any client-facing message, including progress commentary, read
[../aikea/references/client-conversation.md](../aikea/references/client-conversation.md)
completely and apply it throughout this stage.

## Goal

Turn the completed overall project and ordered unit run into self-contained,
executable local assemblies. Every supported unit must receive its exact allocated
boundary, owned parts, physical joint relationships, and builders that produce
real local CadQuery parts with the construction required by those relationships.
The finished parts must meet without occupying the same material, and machining
shared by a joint must fit both participants without unintended breakthrough.
When the overall project changes, regenerate every affected local result while
preserving any local file that the client has changed since its last generation.

For whole-design composition, follow [$aikea-design-furniture](../aikea-design-furniture/SKILL.md).
This skill supplies optional standard recipes within that common protocol.
Apply its [manufacturing process](../aikea-design-furniture/references/manufacturing-process.md)
before generating or adapting a recipe; standard components still need one-face
compatibility across every connection and hardware opening.

## Shared construction inputs

Read [shared panel construction](references/shared-construction.md) when composing
explicit panels, connections and machining or adapting a configurator's output.
Use its common builder and checks; furniture-purpose names do not select machining.
The standard cabinet and structural-base recipes below emit the same editable
inputs and call the shared builder. Older saved builders require explicit migration.
For the base's input, placement and evidence contract, read
[the base recipe](references/base-recipe.md).

## Generate the local units

1. Resolve the active project folder and require its completed `aikea.yaml`.
2. Read [references/unit-taxonomy.md](references/unit-taxonomy.md) and
   [references/panel-construction.md](references/panel-construction.md) completely.
3. Run `python <skill-directory>/scripts/generate_unit_taxonomy.py <project>/aikea.yaml`.
4. Use only the generated local specifications and built results for later work.
5. Describe the completed physical unit boundaries in client-facing language.
6. Complete the first cabinet's configured fitted door before asking the client
   to approve that cabinet. A hinged door is complete only when
   `$aikea-build-doors` has produced its purchased hinge system, matching work in
   both participating panels, and checked closed and open positions.
7. Load `$aikea-review-unit`, show that complete first cabinet, and ask for the
   client's visual approval before producing other units. Use the plain cabinet
   review only for an assembly that is intentionally doorless.

The generator automatically copies the saved material decisions onto every
standard part: carcass stock for sides, shelves, tops, base decks and kickboards;
the door choice for doors; and the back choice for backs. It writes these as
`PartSpec.material_id`, preserving the selected description and each part's
separate thickness. Users never need to supply internal material identifiers.
Record their accepted defaults and overrides once in `aikea.yaml`, then generate.
Do not replace saved choices with a hardcoded material or use viewer appearance
as the material source. A family-level choice remains a family-level choice;
supplier product and fit qualification are separate checks.

For authored or additional parts, carry the same selected stock into their typed
`PartSpec` inputs before building. Keep explicit per-part exceptions, including
drawer bottoms, with their owning configurator. On material revision, regenerate
through the normal writer, which preserves hand-edited files, and repeat the
affected checks; never just relabel an already approved export.

The default floor-standing cabinet base uses Korrekt 61854 plates and 70151
adjustable feet, a deck, and a front kickboard. Never substitute a rail-and-brace
base when hardware, height or installation evidence is missing. Read the
[base recipe](references/base-recipe.md) and [Korrekt mounting contract](references/korrekt-mounting.md).
Check the required overall base height minus deck stock against both the product
adjustment range and the available exact CAD pose; report a conflict instead of
silently changing the room envelope. Exact source files are supplied through
`$aikea-source-hardware-cad`.

Ordinary storage shelves default to four adjustable supports with matching blind
holes and distinct purchases. Read [storage shelf construction](references/storage-shelves.md).
Fixed Cabineo storage shelves require a recorded `FixedShelfChoice`; their pockets
belong on the hidden underside. Structural cabinet floors and tops are separate
parts, with their own structural connections. Shelves use nearly the full usable
depth and rest on pins in the cabinet's shared System 32 rows. They may visually
cross the lighting line; reduce depth only for an actual physical clearance need.
Check protruding lighting hardware, hinges and the intended drawer route; requested but unsourced drawers remain required work, not permission to replace the intended installation.

Every cabinet defaults to full-height System 32 rows on its inside side panels,
including custom compositions. Follow [the cabinet grid contract](references/panel-construction.md#machine-the-cabinet-hardware-grid).
Omitting, shortening or moving those rows requires a deliberate recorded design
override; a few holes around a shelf are not the default grid. Declare the grid
machining and its construction requirement explicitly. The common panel executor
still applies declared machining only; this is a design default, not a role-based
side effect in the cutting engine.

Requested hanging sections require a complete [hanging-rail installation](references/hanging-rails.md):
rail, both supports, their fastening bores, cut length and purchases. Use
`HangingRailFeature` on the existing assembly. Missing CAD or fixing evidence
remains active sourcing work; never omit the rail or call a bare box complete.

## Responsibility boundary

This stage materializes local boundaries, part ownership, executable builders,
and one joint list per unit. The assembly builder resolves each supported joint
once, including the matching work required on every participating part. Each
generated cabinet and base part entry point reads its finished part from the common
assembly build. The complete assembly builder remains the stable entry point.
`$aikea-review-unit` consumes that built result without reconstructing its
geometry.

For the default adjustable feet, reuse the [Korrekt mounting operation](references/korrekt-mounting.md) through shared construction.

For a straight rectangular panel groove, use `SurfaceGrooveSpec` through the
common machining list. Its surface frame points +Z into the material, with +X
along the length and Y centered across the width. The complete groove must fit
the panel and avoid prior machining. Tool radii and end-access assumptions still
need fabrication review. Lighting supplies this operation from its saved run.
