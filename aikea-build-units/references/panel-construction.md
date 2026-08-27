# Panel construction

## Goal

Begin every generated panel as one calculated, reproducible sheet blank that later
construction capabilities can machine without changing its local frame.

## Build the blank

Use the packaged `BlankSheetBuilder` with the panel's calculated local outline
and material thickness. A rectangular panel has a short form:

```python
from blank_sheet_builder import BlankSheetBuilder

workpiece = BlankSheetBuilder.rectangle(
    width_mm=part_width_mm,
    height_mm=part_height_mm,
    thickness_mm=material_thickness_mm,
).build()
```

For a shaped panel, supply its ordered local outline points:

```python
workpiece = BlankSheetBuilder(
    outline_mm=(
        (0.0, 0.0),
        (part_width_mm, 0.0),
        (part_width_mm, right_height_mm),
        (0.0, left_height_mm),
    ),
    thickness_mm=material_thickness_mm,
).build()
```

The ordered points describe the finished outer shape of the blank's face; the
builder closes that outline and extends its material thickness along positive Z.
The default structural carcass preserves the outside top boundary on its back and
top panels. A flat top spans the complete assembly width and bears directly on side
panels that stop at its underside. A confirmed angled end keeps the material needed
for its equal-thickness miter. The deterministic panel taxonomy resolves these local
blanks; generated builders do not recreate that boundary logic.

The generated local part builder owns this call, applies the cuts assigned by the
assembly's joint definitions, and returns the real local CadQuery part. A joint
defines its geometry once and transforms that same geometry into each
participating part's local frame. Before applying the joint, verify that the
uncut participants meet with no material overlap. After applying it, verify that
the shared feature aligns in assembly space and remains within its intended
material depth. Assembly placement and manufacturing placement remain separate
transformations.

## Keep every panel inside the CNC working area

Resolve manufacturability before creating a panel blank. The manufacturing
profile owns the machine travel and cutter diameter; these are shop capabilities,
not wardrobe measurements. Its usable rectangle subtracts the cutter radius from
each travel axis and permits rotating a panel when that makes it fit.

If a required span exceeds the usable rectangle, divide it into the fewest
manufacturable segments. Prefer breaks at structural boundaries such as a cabinet
gap, retain every break as an explicit assembly relationship, and give every
segment its own local part specification and builder. The packaged
`PanelSegmentPlanner` performs this calculation; construction-specific planners
decide which preferred boundaries and joining method make the segments one stable
assembly.

## Distribute structural connectors

Every Cabineo seam calculates its connector count from the finished joint-edge
length. Adjacent connectors may be no more than 300 mm apart, and the first and
last connector may be no more than 200 mm from their edge. Even a short seam uses
at least two connectors so the sheet cannot rotate around a single fixing.

Use the smallest connector count that satisfies those limits, then distribute
the connectors evenly between the two end positions. The one calculated position
set drives both participating panels, so increasing the count cannot separate a
source pocket from its matching receiver cut.

## Machine universal side-panel holes

Every generated side panel receives the reusable shelf-and-hanger hardware
pattern before its joint cuts are applied. The pattern is construction knowledge,
not a client choice or a project-wide geometry setting. It uses the panel's own
depth, height, thickness, and named inside face.

Rows share one bottom reference so holes remain level across side panels with
different top heights. Place the front and rear columns 37 mm from their respective
panel edges. This gives shelves a broad support footprint and keeps the front row
on the shared System 32 hardware reference. Every hole is blind from the inside
face. A panel too thin to preserve its outside face must fail construction instead
of receiving a through hole.

The front row can provide the reference used by compatible drawer fittings, but it
does not define a complete drawer installation. A selected rail profile must still
own its exact mounting holes, vertical position, clearances, and receiving work.

## Build adjustable shelves

Treat each supplied shelf as a real local part rather than viewer-only geometry.
Its blank spans the clear width between the side panels and the clear depth to the
front face of the back panel. Select its support row from the bottom-aligned rows
present on both sides, then preserve that row and the shelf's assembled height in
the local assembly specification. This keeps an unequal or sloped top from giving
the two sides mismatched supports while allowing the shelf count and placement to
change locally without changing the measured-space specification.
