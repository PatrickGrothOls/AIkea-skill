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
The default structural carcass preserves the outside top boundary on its full-height
sides and back. A flat top fits between the side panels, while a confirmed angled
boundary keeps the material needed for its equal-thickness miter. The deterministic
top-panel taxonomy resolves these local blanks; generated builders do not recreate
that boundary logic.

The generated local part builder owns this call, applies the cuts assigned by the
assembly's joint definitions, and returns the real local CadQuery part. A joint
defines its geometry once and transforms that same geometry into each
participating part's local frame. Before applying the joint, verify that the
uncut participants meet with no material overlap. After applying it, verify that
the shared feature aligns in assembly space and remains within its intended
material depth. Assembly placement and manufacturing placement remain separate
transformations.
