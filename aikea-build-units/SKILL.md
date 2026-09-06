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

The bundled construction now supplies full-height tall storage and the structural
base beneath the complete run. The base inherits the cabinet footprint, divides
long panels into CNC-sized modules, and owns its decks, rails, braces, and module
relationships. Each brace-to-rail relationship resolves the brace pockets and
matching blind rail receivers together. Every cabinet side also owns one System
32 hardware grid that shelves, hinges, drawer runners, and later compatible
fittings can share without recalculating their own panel holes. A different furniture purpose proceeds
when its own local design facts and construction taxonomy are available; the
shared boundary calculation and folder writer remain unchanged.

## Responsibility boundary

This stage materializes local boundaries, part ownership, executable builders,
and one joint list per unit. The assembly builder resolves each supported joint
once, including the matching work required on every participating part. Each
generated part builder owns its local part and applies the resolved work in that
part's canonical frame through reusable AIkea construction code. The assembly
builder is the stable entry point that executes all owned part builders.
`$aikea-review-unit` consumes that built result without reconstructing its
geometry.
