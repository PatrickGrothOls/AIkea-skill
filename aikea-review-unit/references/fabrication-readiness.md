# Fabrication readiness

`fabrication-ready` is a machine-verifiable release state, not a visual claim.
The closed recursive assembly is the authority. Open doors, extended drawers,
lighting effects, and review overlays never grant manufacturing authority.

The gate requires all of the following:

1. Every manufactured tree item has positive-volume geometry and an explicit
   accumulated placement.
2. Every purchased item has exact verified geometry and an explicit placement.
3. Every multi-part assembly declares resolved joints, and every resolved joint
   has matching part-owned machining.
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
10. The client has approved the exact checksum of the canonical closed wardrobe
    GLB regenerated from the current built tree. Its default scene must contain
    reachable mesh geometry. The viewer serves immutable startup bytes and
    serializes the one-way decision across processes. Any changed tree, model,
    path, proposal, or decision checksum requires a new approval.

Run the gate with:

```sh
python <skill-directory>/scripts/check_fabrication_readiness.py <project>/aikea.yaml
```

The command always writes `manufacturing/fabrication-readiness.json` and exits
nonzero while any requirement is missing, invalid, or cannot be evaluated. A
failed invocation replaces any prior ready report. Never describe a blocked
report as fabrication ready.
