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
The generated local part builder owns this call, applies the cuts assigned by the
assembly's joint definitions, and returns the real local CadQuery part. A joint
defines its geometry once and transforms that same geometry into each
participating part's local frame. Assembly placement and manufacturing placement
remain separate transformations.
