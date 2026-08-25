---
name: aikea-build-units
description: Generate populated local assembly, part, builder, and joint folders from a completed AIkea assembly run. Use immediately after unit arrangement or when rebuilding or checking a project's local unit taxonomy.
---

# AIkea build units

## Goal

Turn the completed overall project and ordered unit run into self-contained local
building specifications. Every supported unit must receive its exact allocated
boundary, owned parts, physical joint relationships, and importable build-plan
entry points so later construction work starts from resolved project facts.

## Generate the local units

1. Resolve the active project folder and require its completed `aikea.yaml`.
2. Read [references/unit-taxonomy.md](references/unit-taxonomy.md) completely.
3. Run `python <skill-directory>/scripts/generate_unit_taxonomy.py <project>/aikea.yaml`.
4. Use only the generated local specifications and build plans for later work.
5. Describe the completed physical unit boundaries in client-facing language and
   continue automatically to the next unfinished construction stage.

The bundled profile registry currently supplies the full-height tall-storage
taxonomy. A different purpose proceeds when its own local design facts and
construction taxonomy are available; the shared boundary calculation and folder
writer remain unchanged.

## Responsibility boundary

This stage materializes local boundaries, part ownership, build-plan entry points,
and one joint list per unit. Later construction capabilities turn those plans into
machining features and CAD geometry. Keep that work in its owning capability so
generated unit files remain local, stable, and free of global imports.
