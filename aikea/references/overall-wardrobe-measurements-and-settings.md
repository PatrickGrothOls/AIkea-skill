# Overall wardrobe measurements and settings

Use this file when starting a cabinet run or changing measurements that affect more than one cabinet.

## Finish the global specification first

`aikea.yaml` is the global specification. Questions and user answers are the means of completing it, not a replacement for it.

Remain in this step while any required value is missing, contradictory, or rejected by the calculator. Do not begin cabinet layout, local part design, plinth construction, joinery, or manufacturing design. Move to later cabinet design only after the complete `aikea.yaml` has been written and the calculator reports it as valid.

## Allowed project sources

Accept measurements only from the user's messages, a source the user identifies, or the active project's `aikea.yaml`. Never reuse dimensions found in this skill, eval cases, development documentation, legacy wardrobe code, or a different project.

## Orientation and units

- View the wardrobe from the front.
- Interpret left and right as the user's left and right while facing the wardrobe.
- Measure horizontal positions from the inside-left edge of the available space.
- Measure ceiling heights upward from the finished floor.
- Record one unit in `units`: `mm` or `cm`.
- Preserve the unit the user supplied when all values use that unit. Let the calculator normalize calculations to millimetres.
- Ask for clarification when the user mixes units ambiguously.

## Required measured space

Collect:

1. `width`: inside-left to inside-right width available to the wardrobe.
2. `depth`: finished front-to-back depth available to the wardrobe.
3. `ceiling_points`: the ceiling height at the left edge, right edge, and every place where a flat or sloped section begins or ends.

Each ceiling point contains:

- `distance_from_left`: horizontal distance from the inside-left edge;
- `height_from_floor`: vertical height from the finished floor.

Translate clear descriptions directly:

- A flat ceiling becomes `(0, height)` and `(width, height)`.
- One continuous slope becomes `(0, left height)` and `(width, right height)`.
- A flat section followed by a slope becomes `(0, flat height)`, `(slope start, flat height)`, and `(width, right height)`.
- Additional flats or slopes require a point at every stated change.

Require the first distance to be `0`, the final distance to equal `width`, and all distances to increase from left to right. Preserve every measured change point. Never average heights, reorder points, extend a section, or infer a missing endpoint to make the outline pass.

## Required shared design settings

Collect:

- `cabinet_count`;
- `cabinet_width_shares`, one positive number per cabinet from left to right;
- `left_clearance`, `right_clearance`, `cabinet_gap`, and `ceiling_clearance`;
- `base_height`;
- `door_gap`;
- `cabinet_panel_thickness`, `door_thickness`, and `back_panel_thickness`.

Treat an explicit zero as a supplied value. Never replace a missing value with zero or a typical cabinet-making default.

## Translate relative cabinet widths

Store width relationships as shares, not calculated cabinet widths:

- Equal cabinets use equal shares such as `[1, 1, 1]`.
- A cabinet described as half the width of the others uses `0.5` while those cabinets use `1`.
- A cabinet described as twenty percent wider uses `1.2` while the comparison cabinet uses `1`.

Normalize the complete share list only during calculation. Do not ask the user to calculate final cabinet widths, and do not interpret a share as a percentage of the complete wardrobe unless the user explicitly supplied percentages.

## Decide the next response

Build one checklist containing every required measured-space field and shared setting. Count explicit zeros as present.

- **Missing:** Ask for all missing checklist values in one concise response. Group measurements separately from design settings. Do not re-ask supplied values and do not claim the input is valid.
- **Contradictory:** Name the exact conflict and ask only for the correction required. Retain all non-conflicting values.
- **Complete:** Do not ask another question. Save the global specification and run the calculator. A valid result completes this step and permits later cabinet design.

When the user corrects one value, change only that value unless the correction necessarily changes a dependent measurement such as the right-edge ceiling distance after a width change.

## Write the global project file

Use `assets/aikea.yaml` as the exact schema.

- Copy it only when `aikea.yaml` does not already exist.
- Update an existing file in place and preserve values the user did not change.
- Fill only user-supplied measured facts and confirmed shared design settings.
- Keep ceiling points in their measured left-to-right order.
- Do not add calculated cabinet dimensions to `aikea.yaml`.
- Do not add unsupported labels or local construction parameters.

## Keep local construction out

Do not add a value merely because the final build will use it:

- Keep Cabineo cutter dimensions, face selection, edge selection, and pocket coordinates inside Cabineo construction.
- Keep base rail spacing, rail count, braces, and module geometry inside the structural plinth.
- Keep hinge and door-bracket machining inside their matching-cut construction.

Acknowledge a request for a later capability, but state that the current step stores only its global geometry drivers. Do not improvise an implementation that is not bundled with the skill.

## Require the deterministic check

Run the bundled calculator only after the checklist is complete. Require all of these to pass:

- every required input is present and numeric;
- all lengths and thicknesses are positive, except confirmed clearances and gaps may be zero;
- the number of width shares equals `cabinet_count` and every share is positive;
- ceiling points cover the full width in increasing order;
- clearances and cabinet gaps leave positive cabinet width;
- the base and ceiling clearance leave positive cabinet height;
- door and back thicknesses leave positive cabinet and inside depth.

On success, confirm that the global specification is complete, confirm the file path, and summarize calculated cabinet widths, left/right positions, left/right heights, door widths, cabinet depth, and inside depth. Do not generate cabinet geometry during this first step.
