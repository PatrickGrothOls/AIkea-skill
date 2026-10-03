# Fabrication readiness

All official assembly loaders validate operation results before review/export.
They check declared participants, complete built-in cut occurrences, recomputed
cutter geometry and actual removed material, including for custom root builders.
The fabrication gate repeats those checks on the supplied current tree and reports
unqualified custom operations separately. Select a custom root with
`check_fabrication_readiness.py <project>/aikea.yaml --assembly <root-id>`;
the default remains `wardrobe_01`. These checks do not establish strength or
detect design requirements that have not been declared.

`fabrication-ready` is a machine-verifiable release state, not a visual claim.
The closed recursive assembly is the authority. Open doors, extended drawers,
lighting effects, and review overlays never grant manufacturing authority.

The gate requires all of the following:

1. Every manufactured tree item has positive-volume geometry and an explicit
   accumulated placement.
2. Every purchased item has exact verified geometry and an explicit placement.
3. Every assembly declares assessed construction requirements and every physical
   item has explicit coverage. Required connections/features must exist and cover
   their declared subjects; intentional loose parts or floor contact need a
   rationale. All declared joints are resolved and have matching part-owned
   machining. No blanket joint-count rule forces loose parts to be joined.
4. Every manufactured part has a parseable STEP solid that boolean-matches its
   built local geometry and a closed-face DXF drawing with the same millimetre
   footprint in `manufacturing/parts/`, named from its full tree path joined by
   `__`.
5. Every manufactured part specification declares one non-blank exact
   `material_id`. `manufacturing/bom.json` covers every manufactured and
   purchased tree item; its material or product identity and quantity must equal
   the physical specification exactly.
6. `manufacturing/cut-list.csv` covers every manufactured part with that exact
   `material_id`, thickness, quantity, and blank dimensions. Never infer material
   from role, thickness, BOM prose, or a generic fallback.
7. `manufacturing/machining.json` declares the operations for every manufactured
   part, including an explicit empty list when no machining is required.
8. Every registered assembly feature at any depth declares its exact
   owner-relative manufactured-part paths and supplies a valid authority record
   under its owning `fabrication-evidence/` folder. The record must contain that
   exact set—no missing, duplicate, or unrelated paths—with each current STEP
   checksum.
9. The complete closed wardrobe position report covers every direct root child
   and part with complete coordinates, axes, positive bounds, exact relationship
   structure, unique passed checks, and the fingerprint of every current closed
   tree path and accumulated frame.
   Every root also needs the shared closed construction position record: current
   envelope authority, physical paths/bounds and independently recomputed fit and
   contact checks. Custom roots use this common record without the older wardrobe
   relationship schema. See [closed position evidence](construction-position.md).
10. The client has approved the exact checksum of the canonical closed wardrobe
    GLB regenerated from the current built tree. Its default scene must contain
    reachable mesh geometry. The viewer serves immutable startup bytes and
    serializes the one-way decision across processes. Any changed tree, model,
    path, proposal, or decision checksum requires a new approval. The proposal and
    decision also bind `construction_sha256` to current declared inputs and project
    source, so material, product or requirement changes invalidate an unchanged image.

Custom joint qualification reuses the registered feature record and exact affected
part scope. Both manifest and current report declare `qualified_joint_ids`; the
report must include the current `construction_sha256`, passed applicable checks
and matching STEP checksums for every participant. Shared output checks still run
independently. See the [construction protocol](../../aikea-build-units/references/shared-construction.md).

Run the gate with:

```sh
python <skill-directory>/scripts/check_fabrication_readiness.py <project>/aikea.yaml
```

The command always writes `manufacturing/fabrication-readiness.json` and exits
nonzero while any requirement is missing, invalid, or cannot be evaluated. A
failed invocation replaces any prior ready report. Never describe a blocked
report as fabrication ready.
