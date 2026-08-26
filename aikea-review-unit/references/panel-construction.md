# First panel construction

## Goal

Begin every panel as one calculated, reproducible sheet blank that later panel
construction can shape and position.

## Build the blank

Use the packaged `BlankSheetBuilder` with the panel's calculated local face
dimensions and material thickness:

```python
from blank_sheet_builder import BlankSheetBuilder

workpiece = BlankSheetBuilder(
    width_mm=part_width_mm,
    height_mm=part_height_mm,
    thickness_mm=material_thickness_mm,
).build()
```

The blank begins at the local XY origin and its material thickness extends along
positive Z. Continue the panel's construction from the returned `workpiece`.
Shaping, construction features, assembly placement, and manufacturing placement
remain later responsibilities operating on that same part.
