# Hanging rails

A requested hanging section must contain a rail, two supports, their fastenings
and machined host holes in the complete saved assembly. A missing recipe is work
to resolve, never permission to omit the hanging section.

## Shared installation

Use `HangingRailFeature` on the existing built cabinet, after its other features.
Keep the wrapper in that cabinet's normal builder so inspection, STEP export and
inventory all consume the same result. Do not put rails only in viewer code.

```python
from hanging_rail_feature import HangingRailFeature
from hanging_rail_layout import HangingRailLayout

rail = HangingRailFeature(HangingRailLayout(
    rail_id='hanging_01',
    left_side_id='left_side', right_side_id='right_side',
    depth_position_mm=300, lower_screw_height_mm=1700,
    pilot_diameter_mm=3, pilot_depth_mm=13,
))
result = rail.apply(existing_assembly)
cut_list = rail.cut_list(existing_assembly)
```

The dimensions above illustrate the API, not a room design. Choose height from
clothes/drop and shelf clearance; choose depth from the actual hanger envelope,
back and closed door. Coordinates belong to the owning cabinet. The height datum
is the lowest support screw; the rail centre sits 11.3 mm above it. Both hosts
must be vertical and have their inside broad face declared as `>Z`.

The helper preserves previous panels, joints, children and hardware. It adds two
support purchases, one cut-stock purchase and six real blind pilot bores. Save
`cut_list` in the manufacturing pack: one installed cut piece is not one purchased
5000 mm stock rail. Aggregate lengths, saw kerf and usable offcuts before pricing.

## Product and fixing authority

Hettich SL 322 support **70664**, for 30 x 15 mm oval rail, uses three 4 mm
countersunk wood screws per support. From the lowest hole, the other holes are
9.5 and 32 mm above it. Cut rail length is clear inside width minus 7 mm.
[Official drawing, printed page 972](https://catalog.hettich.com/General/TA_2025/en_DE/catalogs/TA_2025_en_DE/pdf/save/bk_974.pdf).
The cut-stock profile is [Hettich 9000894](https://shop.hettich.com/us_EN/Further-products/Interior-Fittings/Wardrobe-interior-organisation/Oval-wardrobe-rails-and-wardrobe-rail-supports/Cabinet-rails/Wardrobe-rails%2C-oval%2C-30-x-15-mm%2C-5000-mm%2C-matt-nickel-plated/p/9000894),
30 x 15 x 0.6 mm, 5000 mm.

A 4 mm screw is not a 4 mm pilot. The 3 x 13 mm default is a proposed workshop
pilot for 16/18 mm sheet stock, not a universal manufacturer recommendation.
Select and record the screw length, actual material and load before release.
The support's mounting plate is 3 mm thick. Include six screws explicitly when
the supplier does not include them; the inventory reports the unconfirmed fixing
supply instead of silently charging zero. No load rating has been inferred.

The layout checks opposite faces, complete support margins and blind pilot depth.
The feature rejects collisions with existing panels and modeled fittings. The
common cut executor checks that holes remove the expected stock without
unintended overlap with earlier machining. Keep the one-face policy and check rail/hanger
clearance against shelves, hinges, lighting and door movement before repeating.

## Source geometry

The built-in support is a **dimensioned envelope preview**, not manufacturer CAD.
Its pending construction requirement is deliberate; drilling uses the official
drawing independently. For the final installation load exact SL 322 geometry and
pass `support_geometry` and its registered `support_asset_id`. Native axes are X
away from the mounting face, Y across the support and Z upwards, with the lowest
fixing at (0,0,0). Never rescale a support to fit the cabinet.

Follow [SL 322 sourcing](../../aikea-source-hardware-cad/references/hettich-sl322.md).
Do not consider downloading a source file to be completion: import it, check its
native frame, complete the screw/load record and rerun the full cabinet checks.
