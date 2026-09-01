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
5. `manufacturing/bom.json` covers every manufactured and purchased tree item,
   including material or product identity and quantity.
6. `manufacturing/cut-list.csv` covers every manufactured part with material,
   thickness, quantity, and blank dimensions.
7. `manufacturing/machining.json` declares the operations for every manufactured
   part, including an explicit empty list when no machining is required.
8. Every registered assembly feature at any depth supplies a valid,
   manufacturing-authority evidence record under its owning
   `fabrication-evidence/` folder. The record lists the full path and exact STEP
   checksum of every affected manufactured part.
9. The complete closed wardrobe position report has versioned, non-empty passed
   checks and covers every direct child of the wardrobe root.
10. The client has approved the exact checksum of the current closed wardrobe
    GLB. Rebuilding different bytes automatically requires a new approval.

Run the gate with:

```sh
python <skill-directory>/scripts/check_fabrication_readiness.py <project>/aikea.yaml
```

The command writes `manufacturing/fabrication-readiness.json` and exits nonzero
while any requirement is missing or invalid. Never describe a blocked report as
fabrication ready.
