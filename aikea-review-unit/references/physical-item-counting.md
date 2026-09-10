# Count an assembly's parts and purchased hardware

Run in the installed CAD runtime on the current generated project:

```bash
python <skill-directory>/scripts/count_physical_items.py <project-directory>
```

The command defaults to the canonical closed `wardrobe_01`. Use
`--assembly furniture_legs_01` (or the actual root ID) for an authored assembly.
It writes
`manufacturing/item-counts.json`. It leaves the fabrication `bom.json`, cut list,
machining records, and design files unchanged. Exit 2 means the draft contains
unresolved items; a builder failure leaves an invalid report. Exit 0 means the
declared inventory had no reported gaps, not that the furniture is approved.

Use `manufactured_parts` for one row per physical panel, with full assembly path,
local dimensions and outline. `hardware_components` preserves every modeled
component. `purchased_units` links those components into installed purchase units;
`purchased_summary` aggregates exact products. Supplier packs are separate from
installed quantity.

- Count one Cabineo from each layout position with exactly matching source and
  receiver cuts. Emit one separate brass insert per verified Cabineo, Häfele
  267.91.314, as selected by Patrick. Its listing's 100-piece pack does not round
  the installed count. The counter does not revalidate insert compatibility.
- KA 5332: one pair per declared drawer installation. KA 4532: one pair across
  the two fixed and two moving members, plus two separately installed spacers.
- Count selected hinges, plates and handles. New Hettich and Riex generators
  declare purchase membership explicitly. For other hardware, preserve modeled
  components and report missing purchase declarations; do not infer sets from
  names, meshes, or raw CAD solid counts.
- Expect mounting fasteners to come with purchased parts. Do not add screw
  purchase lines from mounting holes. Explicit exceptions remain unresolved
  until their separate supply is specified.

Read `unresolved` before presenting totals. Damaged Cabineo evidence and incomplete
purchase groups are excluded from verified quantities and reported as gaps.
Missing material IDs, support products, product identities, placement, and
unresolved base/door relationships prevent a complete priced order.

This first counter inventories what the generated tree declares. It cannot yet
prove that every intended handle, shelf support, base fixing or other feature is
present. Cabineos currently derive from machining; if a design also models them
or their inserts as purchased hardware, resolve that duplicate representation
before using the purchasing summary. Do not quote an unverified sum.

Existing generated hardware without purchase declarations remains visible as
unresolved. Updating a feature with the current generator adds its declarations;
do not hand-edit quantities or regenerate approved geometry merely to suppress a
gap. New purchase declarations use the shared runtime contract and also work in
projects whose local hardware contract predates this counter.

## Estimate standard sheet requirements

After producing the inventory, calculate sheet requirements with:

```bash
python <skill-directory>/scripts/calculate_sheet_requirements.py \
  <project-directory>/manufacturing/item-counts.json --allow-rotation
```

Defaults are 1220 × 2440 mm sheets, 10 mm edge margins and 8 mm gaps, taken from
the earlier Vilja nesting workflow. State those assumptions. `--allow-rotation`
allows 90-degree turns; omit it to retain each part's local orientation. Confirm
material and grain rules before treating the layout as purchasing guidance.
Use `--width`, `--height`, `--edge-margin` and `--part-gap` for agreed overrides.

The command needs only Python's standard library and the saved inventory. It
groups by material ID and thickness and writes `sheet-requirements.json` plus a
standalone `sheet-requirements.html` with diagrams and full part paths. Present
the total and per-thickness/material breakdown, linking the HTML for inspection.
The JSON retains the input hash. Refresh the inventory and rerun after changes.

The estimate uses bounding rectangles and compares two deterministic orientation
preferences. It is a feasible layout, not a proven minimum or a CAM file. Unknown
materials are provisionally pooled within each thickness and explicitly labeled.
Missing grain direction, stock allowances and design completeness remain open.
If any panel is oversized, status is `incomplete`, exit is 2, and `sheet_count`
counts only sheets with placed panels: do not present it as the complete order.
Exit 0 is a successful provisional estimate, not fabrication approval.

### Compare stock scenarios with actual geometry

Use `--scenario-thickness 16 --scenario-material MDF` to estimate the saved
panel rectangles in the requested stock. This does not regenerate construction:
clearances, internal dimensions, hardware fit, grooves and joint depths still
belong to the original geometry. Report the actual thicknesses separately.

Use `--non-sheet-part <full-instance-path>` for an explicitly identified rod or
other item made from separate stock. It stays in the source inventory and is
listed in the sheet report's `stock_scenario.non_sheet_parts`. Never drop it
from the eventual quote. Unknown paths and repeated selections fail.

An oversized panel remains a blocker even in a thickness scenario. If comparing
an agreed panel split, save a separate derived inventory with original source
hash, parent part paths and an explicit seam-construction limitation. Do not
edit the canonical inventory or label that proposal regenerated CAD.
