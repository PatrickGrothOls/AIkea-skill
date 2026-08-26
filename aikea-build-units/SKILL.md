---
name: aikea-build-units
description: Generate populated local assembly, part, builder, and joint folders from a completed AIkea assembly run. Use immediately after unit arrangement or when rebuilding or checking a project's local unit taxonomy.
---

# AIkea build units

## Goal

Turn the completed overall project and ordered unit run into self-contained,
executable local assemblies. Every supported unit must receive its exact allocated
boundary, owned parts, physical joint relationships, and builders that produce
real local CadQuery parts with the construction required by those relationships.

## Generate the local units

1. Resolve the active project folder and require its completed `aikea.yaml`.
2. Read [references/unit-taxonomy.md](references/unit-taxonomy.md) and
   [references/panel-construction.md](references/panel-construction.md) completely.
3. Run `python <skill-directory>/scripts/generate_unit_taxonomy.py <project>/aikea.yaml`.
4. Use only the generated local specifications and built results for later work.
5. Describe the completed physical unit boundaries in client-facing language.
6. Load `$aikea-review-unit`, build the first cabinet as a visual mock-up, open its
   viewer, and ask for the client's visual approval before producing other units.

The bundled profile registry currently supplies the full-height tall-storage
taxonomy. A different purpose proceeds when its own local design facts and
construction taxonomy are available; the shared boundary calculation and folder
writer remain unchanged.

## Responsibility boundary

This stage materializes local boundaries, part ownership, executable builders,
and one joint list per unit. The assembly builder resolves each supported joint
once, including the matching work required on every participating part. Each
generated part builder owns its local part and applies the resolved work in that
part's canonical frame through reusable AIkea construction code. The assembly
builder is the stable entry point that executes all owned part builders.
`$aikea-review-unit` consumes that built result without reconstructing its
geometry.
