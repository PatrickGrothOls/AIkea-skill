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
for its equal-thickness miter. Every changing-angle seam derives one shared miter
plane in the assembled frame and returns complementary cuts to the two local panel
frames. The deterministic panel taxonomy resolves these local blanks; generated
builders do not recreate that boundary logic.

The shared panel executor builds these blanks and applies the cuts assigned by
the assembly's explicit joint and machining requests. The generated cabinet part
entry point reads its finished part from that complete build. A joint
defines its geometry once and transforms that same geometry into each
participating part's local frame. Verify the finished participants meet with no
gap or unintended material overlap, and that any blind feature remains within its
intended material depth. Assembly placement and manufacturing placement remain
separate transformations.

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

## Machine the cabinet hardware grid

Both standard cabinet recipes and custom cabinet compositions default to one
versioned System 32 grid on each inside side panel, over the full usable height.
Declare the operation explicitly with `PartMachiningSpec(..., "system_32")` and a
`ConstructionRequirementSpec` referencing that panel and machining ID. Reuse
`System32SidePanelGridProfile`; do not recreate the grid from shelf positions.
The shared builder applies the request after joint cuts and checks that every
blind bore fits retained material. A role name alone never requests machining.

Before omitting, shortening or moving the grid, record a deliberate design override
in the active project's design decisions: affected panel IDs, changed dimensions
or omitted rows, reason, and replacement support/hardware arrangement. Preserve a
specific user choice when supplied. Never infer an override from a custom builder,
a reference image, sparse shelf supports or a machining collision. Unresolved
collisions remain outstanding design work. A local five-hole group around a shelf
does not fulfil the full-height default.

The current bundled profile starts 100 mm from the panel bottom and stops at least
100 mm below its top. These are AIkea profile choices, not a claim that every
manufacturer uses them. Use the panel's actual depth, height, thickness and inside
face. For a sloped boundary, ensure each column's top rows fit real retained stock;
record any required adaptation rather than clipping a cutter or omitting the grid.

Rows share one bottom reference so holes remain level across side panels with
different top heights. The rows repeat every 32 mm; front and rear columns sit
37 mm from their respective panel edges. Every 5 mm hole is blind from the inside
face. A panel too thin to preserve its outside face must fail construction instead
of receiving a through hole.

Construction capabilities consume this saved grid rather than creating another
panel-hole system. A shelf selects one row. A compatible hinge plate selects two
adjacent rows. A selected drawer-runner profile declares which grid positions it
uses and owns any additional preparation, vertical placement, and clearances.
Recessed shelves may require additional support columns; those do not replace the
cabinet's default front/rear grid. Plan the complete grid together with the
lighting channel, Cabineo cuts and hinge/runner preparation. Keep every blind hole
on the chosen CNC face; a shared partition requiring two faces needs a deliberate
construction solution rather than an unrecorded second setup.

Before declaring the cabinet complete, reconcile expected rows and columns with
the declared operations and actual removed material on both sides. Check matching
world-height rows, bore depth and retained outside skin, hardware alignment and
collisions. Review the current exported geometry with doors hidden. A passing
check on the few holes actually declared does not prove the full grid exists.

## Build adjustable shelves

Treat each supplied shelf as a real local part rather than viewer-only geometry.
Its blank spans the clear width between the side panels and the clear depth to the
front face of the back panel. Select its support row from the bottom-aligned rows
present on both sides, then preserve that row and the shelf's assembled height in
the local assembly specification. This keeps an unequal or sloped top from giving
the two sides mismatched supports while allowing the shelf count and placement to
change locally without changing the measured-space specification.


`SurfacePocketSpec` uses the same part-local surface frame as a groove and adds
`corner_radius_mm`. Its shared builder makes a rectangular or rounded rectangular
pocket; set depth to the panel thickness for a through-opening. For example,
`SurfacePocketSpec("frame_opening", "frame", surface, 400, 600, 6, 4)` makes a
400×600 mm opening with 4 mm internal radii in a 6 mm frame. Give `surface` an
origin at one end's center (+X along length, +Z into stock). The complete opening
must enter an actual panel face, fit retained stock, and avoid earlier cuts.
Square corners, remaining walls, hold-down and final tooling still need deliberate
fabrication decisions. Use this same operation for a configured or authored part.
