# Overall wardrobe inputs

Use this file when starting a cabinet run or changing measurements that affect more than one cabinet.

Accept measurements only from the user's request, a source the user identifies, or the active project's `aikea.yaml`. Never reuse dimensions found in the AIkea skill, eval fixtures, development documentation, legacy cabinet code, or a different project.

## Orientation

- View the wardrobe from the front.
- Left and right always mean the user's left and right while facing the wardrobe.
- Measure horizontal positions from the inside-left edge of the available space.
- Measure ceiling heights upward from the finished floor.
- Record the unit once in `units`. Use `mm` or `cm`; calculations are normalized to millimetres.

## Ask for measured space

Ask for:

1. `width`: inside-left to inside-right width available to the wardrobe.
2. `depth`: finished front-to-back depth available to the wardrobe.
3. `ceiling_points`: the ceiling height at the left edge, right edge, and every place where a flat or sloped section begins or ends.

Each ceiling point contains:

- `distance_from_left`: horizontal distance from the inside-left edge;
- `height_from_floor`: vertical height from the finished floor.

The first point must have `distance_from_left: 0`. The last point must equal `width`. Distances must increase from left to right.

A flat ceiling needs two points with equal heights:

```yaml
ceiling_points:
  - distance_from_left: 0
    height_from_floor: 2400
  - distance_from_left: 3000
    height_from_floor: 2400
```

A flat section followed by a slope needs three points:

```yaml
ceiling_points:
  - distance_from_left: 0
    height_from_floor: 2400
  - distance_from_left: 1000
    height_from_floor: 2400
  - distance_from_left: 3000
    height_from_floor: 1200
```

Add more points for additional flat or sloped sections. Do not reduce a measured outline to a fixed "left height, right height, slope start" shape.

## Ask for shared design settings

These are confirmed design choices because they control several cabinets or assemblies:

- `cabinet_count`;
- `cabinet_width_shares`, one positive number per cabinet from left to right;
- `left_clearance`, `right_clearance`, `cabinet_gap`, and `ceiling_clearance`;
- `base_height`;
- `door_gap`;
- `cabinet_panel_thickness`, `door_thickness`, and `back_panel_thickness`.

Equal cabinet widths use equal shares, for example `[1, 1, 1, 1]`. A cabinet with share `0.5` receives half as much of the distributable width as one with share `1`. The calculator normalizes the complete list so all cabinets still close against the available width.

Record an intentional zero explicitly. Do not replace a missing value with zero or a typical cabinet-making default.

## Keep local settings out

Do not add a value merely because the final build uses it. In particular:

- Cabineo cutter dimensions, face selection, and edge selection belong to Cabineo construction.
- Base rail spacing and rail count belong to the base.
- Hinge and door-bracket cutout dimensions belong to their matching-cut construction.

The overall file supplies the space and shared settings. Each later assembly calculates its own subparts from those values.

## Required checks

Before continuing, run the bundled calculator and require all of these to pass:

- every required input is present and numeric;
- all lengths and thicknesses are positive, except confirmed clearances and gaps may be zero;
- the number of width shares equals `cabinet_count` and every share is positive;
- ceiling points cover the full width in increasing order;
- clearances and cabinet gaps leave positive cabinet width;
- the base and ceiling clearance leave positive cabinet height;
- door and back thicknesses leave positive cabinet and inside depth.
