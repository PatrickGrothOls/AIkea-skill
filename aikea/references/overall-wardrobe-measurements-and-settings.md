# Overall wardrobe measurements and settings

Use this file when starting a cabinet run or changing measurements that affect more than one cabinet.

## Finish the global specification first

`aikea.yaml` is the global specification. Questions and user answers are the means of completing it, not a replacement for it.

Remain in this step while any required value is missing, contradictory, or rejected by the calculator. When the complete `aikea.yaml` passes, present the calculated overall dimensions and stop.

## Guide the client in plain language

Act like a carpenter helping a client plan a wardrobe, not like software asking someone to complete a data structure.

1. Begin warmly. With no supplied details, say: "Great, let's build an awesome wardrobe. First thing is to get the units aligned. Are you using cm, mm, or inches?"
2. Default to one topic per response: unit; left and right sides; top; back and
   front; each measurement topic; then each wardrobe choice. Never combine the
   three installation questions into one response.
3. If the client wants to gather everything at once, adapt `assets/wardrobe-measurement-sheet.md` and let them return the completed sheet. Ask only about missing or conflicting answers afterward.
4. Establish how the wardrobe will sit before asking for dimensions: freestanding or fitted, walls at the left or right, whether it reaches the ceiling, and whether its front is open.
5. Then ask about the wardrobe itself: number of sections, whether they should be equal or which should be wider or narrower, fit at the walls and ceiling, base height, door spacing, and chosen material thicknesses.
6. Translate the answers into the global specification privately. Do not expose filenames, schema fields, width shares, formulas, calculator commands, validation terminology, or the fitting allowance unless the client asks.
7. Give the client calculated cabinet sizes and positions, not the internal values used to derive them.

## Allowed project sources

Accept measurements only from the user's messages, a source the user identifies, or the active project's `aikea.yaml`. Never reuse dimensions found in this skill, eval cases, development documentation, legacy wardrobe code, or a different project.

## Orientation and units

- View the wardrobe from the front.
- Interpret left and right as the user's left and right while facing the wardrobe.
- Measure horizontal positions from the inside-left edge of the available space.
- Measure ceiling heights upward from the finished floor.
- Record one unit in `units`: `mm`, `cm`, or `in` for inches.
- Preserve the unit the user supplied when all values use that unit. Let the calculator normalize calculations to millimetres.
- Ask for clarification when the user mixes units ambiguously.

## Required measured space

Collect the raw readings without subtracting any allowance. The installation
arrangement decides how many readings are required:

1. `width_measurements`: if both sides are fixed, record `bottom`, `middle`, and
   `top`; otherwise record one `single` width from the fixed or intended left edge
   to the fixed or intended right edge.
2. `depth_measurements`: if both back and front are fixed, record `left`, `middle`,
   and `right`; otherwise record one `single` depth from the back to the intended
   wardrobe front.
3. `height_measurements`: if the wardrobe reaches the ceiling, record at least
   left, centre, and right plus every place where a flat, sloped, or stepped section
   begins or ends. If it is open above, record one intended height.

Each height measurement contains:

- `distance_from_left`: horizontal distance from the inside-left edge;
- `height_from_floor`: vertical height from the finished floor.

Translate ceiling descriptions directly when height is enclosed:

- A flat ceiling still requires left, centre, and right readings; preserve small differences rather than flattening them.
- One continuous slope requires at least left, centre, and right readings.
- A flat section followed by a slope requires the usual three readings plus the exact place where the slope begins.
- Additional flats, slopes, or steps require a reading at every stated change.

Require the first distance to be `0`, the final distance to cover the calculated usable width, and all distances to increase from left to right. Preserve every raw reading and measured change point. Never average readings, reorder points, extend a section, or infer a missing endpoint to make the outline pass.

## Apply the fitting allowance

Keep the raw measurements unchanged. Store whether each dimension is enclosed at both ends under `enclosed_dimensions`:

- `width` is true only when the run is trapped between fixed boundaries on both the left and right. One wall and one open side is not enclosed.
- `depth` is true only when the run is trapped between fixed boundaries at both the back and front. An ordinary wardrobe against a back wall with an open front is not enclosed.
- `height` is true when the wardrobe is fitted between the floor and ceiling. A freestanding wardrobe with open space above is not enclosed.

Store the template's positive `fit_allowance` value of `2 mm`. Subtract it once only from dimensions marked as enclosed:

- enclosed width uses the smallest width reading minus 2 mm;
- enclosed depth uses the smallest depth reading minus 2 mm;
- enclosed height uses the measured or interpolated height minus 2 mm before base height and chosen ceiling clearance are removed;
- a dimension that is not enclosed uses its smallest or measured value without the 2 mm subtraction.

This is built-in AIkea fitting knowledge, not a client design question. If the
project uses centimetres, store the same allowance as `0.2 cm`. If it uses inches,
store it as `0.0787401575 in`.

## Required internal design values

The template supplies `fit_allowance`. Collect the remaining internal values:

- `enclosed_dimensions.width`, `enclosed_dimensions.depth`, and `enclosed_dimensions.height`, derived from the client's installation description;
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

Never use the term `width shares` with the client. Ask natural questions such as:

- "Should all sections be the same width?"
- "Should any section be narrower or wider than the others?"
- "Roughly half-width, twenty percent wider, or another relationship?"

Translate the answer to shares internally and present the resulting cabinet widths back to the client.

## Decide the next response

Build one checklist containing every required measured-space field and shared setting. Count explicit zeros as present.

- **Missing measured space:** Ask for only the next missing measurement topic. Do not ask about wardrobe choices yet.
- **Missing wardrobe choices:** Once the measured space is complete, ask for only the next missing choice topic in client-facing language. Ask how the wardrobe is enclosed before asking about its section layout. Do not re-ask supplied values or expose internal field names.
- **Contradictory:** Name the exact conflict and ask only for the correction required. Retain all non-conflicting values.
- **Complete:** Do not ask another question. Save the global specification and run the calculator privately. A valid result completes this step and permits later cabinet design.

When the user corrects one value, change only that value unless the correction necessarily changes a dependent measurement such as the right-edge ceiling distance after a width change.

## Write the global project file

Use `assets/aikea.yaml` as the exact schema.

- Copy it only when `aikea.yaml` does not already exist.
- Update an existing file in place and preserve values the user did not change.
- Fill only user-supplied measured facts and confirmed shared design settings.
- Keep height measurements in their measured left-to-right order.
- Preserve every supplied width and depth measurement. Store `single` for a
  one-reading open dimension and the three named readings for an enclosed dimension.
- Record all three enclosed-dimension decisions from the client's installation description; never infer a fully enclosed dimension from one wall alone.
- Preserve the template's 2 mm fitting allowance unless the user explicitly changes the project policy.
- Do not add calculated cabinet dimensions to `aikea.yaml`.
- Do not add fields that are absent from the template.

## Require the deterministic check

Run the bundled calculator only after the checklist is complete. Require all of these to pass:

- every required input is present and numeric;
- all lengths and thicknesses are positive, except confirmed clearances and gaps may be zero;
- the number of width shares equals `cabinet_count` and every share is positive;
- an enclosed width or depth has three named readings, while an open width or depth has at least one reading;
- an enclosed height has at least three measurements covering the usable width in increasing order, while an open height has at least one;
- the 2 mm fitting allowance leaves every enclosed dimension positive;
- clearances and cabinet gaps leave positive cabinet width;
- the base and ceiling clearance leave positive cabinet height;
- door and back thicknesses leave positive cabinet and inside depth.

On success, tell the client that the measurements and shared choices are saved and checked, then summarize calculated cabinet widths, left/right positions, left/right heights, door widths, cabinet depth, and inside depth. Do not mention the file path or checking mechanism unless asked. Stop after presenting these overall results.
