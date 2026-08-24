# Overall wardrobe measurements and settings

Use this file when starting a cabinet run or changing measurements that affect more than one cabinet.

## Contents

- Finish the global specification first
- Guide the client in plain language
- Format questions for short replies
- Allowed project sources
- Orientation and units
- Plan useful measurements from the labelled outline
- Record confirmed design decisions
- Required measured space
- Apply the fitting allowance
- Required internal design values
- Translate relative cabinet widths
- Decide the next response
- Write the global project file
- Require the deterministic check

## Finish the global specification first

`aikea.yaml` is the global specification. Questions and user answers are the means of completing it, not a replacement for it.

Remain in this step while any required value is missing, contradictory, or rejected by the calculator. When the complete `aikea.yaml` passes, present the calculated overall dimensions and stop.

## Guide the client in plain language

Act like a carpenter helping a client plan a wardrobe, not like software asking someone to complete a data structure.

1. Begin warmly: "Great, let's build an awesome wardrobe. First thing is to get
   the units aligned." Then offer centimetres, millimetres, and inches as three
   numbered choices.
2. Default to one topic per response: unit; front-view shape; labelled-edge fit;
   whether depth has a required flush line; each measurement topic; then each
   wardrobe choice.
3. If the client wants to gather everything at once, adapt `assets/wardrobe-measurement-sheet.md` and let them return the completed sheet. Ask only about missing or conflicting answers afterward.
4. Establish the front-view shape before asking for dimensions. Draw its outline,
   label every edge clockwise from `A` at the left edge, and give each top flat,
   slope, or step its own label and parenthesized plain name.
5. Ask one placement question after showing the labels. Offer `1. Every labelled
   edge is fitted` and `2. Some labelled edges are open`, with the named labels
   repeated so a response such as `2: C (sloped top)` is sufficient. The wardrobe
   front is always open and is never part of this question.
6. Ask one separate flush-depth question with `1. Yes` and `2. No`. A yes means
   the depth must fit between the back and that front line; it does not mean the
   wardrobe front is enclosed.
7. Then ask about the wardrobe itself: number of sections, whether they should be
   equal or which should be wider or narrower, fit at the walls and ceiling, base
   height, door spacing, and chosen material thicknesses. Format each topic as
   numbered choices or one numbered value line.
8. Translate the answers into the global specification privately. Do not expose filenames, schema fields, width shares, formulas, calculator commands, validation terminology, or the fitting allowance unless the client asks.
9. Give the client calculated cabinet sizes and positions, not the internal values used to derive them.

## Format questions for short replies

Make the response easy to scan on a phone and easy to answer without copying the
question.

- Pair every edge letter with its plain name whenever it appears in client-facing
  text: `A (left side)`, `B (top flat)`, `C (sloped top)`, `D (right side)`, and
  `E (bottom)`. Do not later shorten these to bare letters.
- Write a junction by naming both edges, for example
  `B (top flat)-C (sloped top) junction`.
- Put every requested reading on its own numbered line, even when the topic needs
  only one reading. Keep one measurement topic per response.
- End a measurement request by showing the reply form, such as
  `Reply 1: 250 cm, 2: 249.8 cm, 3: 250.1 cm.`
- Put every design decision into numbered choices. The client may answer with only
  the option number. If the decision requires a value, use one numbered line such
  as `1. Base height: ___` and invite `1: 100 mm`.
- Restart numbering at `1` for each response. Interpret a short numbered reply
  against the immediately preceding question only.
- Offer only meaningful choices. Do not invent a typical value or silently turn a
  missing answer into a default.

Example measurement request:

1. `A (left side)` to `D (right side)`, just above `E (bottom)`: ___
2. `A (left side)` to `D (right side)`, halfway up their shared height: ___
3. `A (left side)` to `D (right side)`, just below the
   `C (sloped top)-D (right side)` junction: ___

Example design question:

1. All cabinet sections should be equal.
2. One or more sections should be narrower or wider.
3. Recommend a section arrangement after hearing what I need to store.

Say that the client can reply with `1`, `2`, or `3`.

## Allowed project sources

Accept measurements only from the user's messages, a source the user identifies, or the active project's `aikea.yaml`. Never reuse dimensions found in this skill, eval cases, development documentation, legacy wardrobe code, or a different project.

## Orientation and units

- View the wardrobe from the front.
- Interpret left and right as the user's left and right while facing the wardrobe.
- Measure horizontal positions from the inside-left edge of the available space.
- Measure ceiling heights upward from the finished floor.
- Label front-outline edges clockwise, starting with `A (left side)` on the left
  vertical edge. A rectangle therefore uses `A (left side)`, `B (top)`,
  `C (right side)`, and `D (bottom)`. Insert another letter and plain name for
  every additional top segment.
- Record one unit in `units`: `mm`, `cm`, or `in` for inches.
- Preserve the unit the user supplied when all values use that unit. Let the calculator normalize calculations to millimetres.
- Ask for clarification when the user mixes units ambiguously.

## Plan useful measurements from the labelled outline

Keep the labelled outline as the shared measuring map. After drawing it, every
measurement question must name:

- the two boundaries the tape or laser spans;
- the labelled edge or edge junction that locates the reading;
- the fit problem the repeated position helps reveal, when that is not obvious.

Use junction descriptions such as `B (top flat)-C (sloped top) junction`. Do not
revert to a bare letter or an unqualified "top," "middle," "left," or "right"
once labels exist.

Choose lines that reveal the actual space:

- Repeat a measurement only where it compares the same two relevant surfaces.
  Place repeated lines so they can reveal lean, bow, taper, or a surface that is
  out of square.
- Do not measure to a slope and call it a wall-width check. Move that check to a
  height where both side boundaries exist, or replace it with a measurement that
  records the slope itself.
- Measure every corner where a flat, slope, or step starts or ends. Add a useful
  point along a long segment when it helps verify that the real surface follows
  the intended straight line.
- If access makes a proposed line impractical, choose another reachable line that
  tests the same surfaces. Briefly explain the change instead of forcing the
  standard position.

For a rectangular outline `A (left side)`, `B (top)`, `C (right side)`, and
`D (bottom)`, describe width checks as between `A (left side)` and
`C (right side)`, located just above `D (bottom)`, midway up the shared wall
height, and just below `B (top)`. Describe height checks as vertical from
`D (bottom)` to `B (top)`, beside `A (left side)`, midway between
`A (left side)` and `C (right side)`, and beside `C (right side)`.

For an outline `A (left side)`, `B (top flat)`, `C (sloped top)`,
`D (right side)`, and `E (bottom)`, compare `A (left side)` and
`D (right side)` only below the `C (sloped top)-D (right side)` junction where
both side walls exist. Locate the top change at the
`B (top flat)-C (sloped top)` junction. Record vertical heights from
`E (bottom)` to the top boundary at every named junction, plus useful points
along `C (sloped top)` when needed to represent or verify the slope.

For depth, locate readings from the front-view map as well. A freely chosen depth
can be measured from the back to the intended front midway along the floor edge.
A required flush depth is measured from the back boundary to the fixed front line
near the left edge, at the centre of the floor edge, and near the right edge.

## Record confirmed design decisions

Treat the client's explicit description of the intended geometry as evidence, not
as an unverified assumption. A measurement checks an unknown physical condition;
it is unnecessary when the client has directly settled the design property and an
extra reading would reveal nothing useful.

Use `design_decisions` for a confirmed statement that changes how geometry is
interpreted or which readings are required, and that is not already represented by
a normal measurement or setting. Each record contains:

- `subject`: the labelled design element, such as `front_outline.edge_C`;
- `decision`: the confirmed property, such as `straight`;
- `design_effect`: the action this permits, such as `use_measured_endpoints`;
- `client_statement`: the client's statement that supports the decision.

For example, if the client confirms that slope edge `C` is straight and a useful
intermediate reading cannot be taken, preserve that statement and use the measured
`B-C` and `C-D` endpoints. Do not ask for another reading merely to prove the
straightness they have confirmed.

Do not duplicate cabinet count, material thicknesses, clearances, or other values
that already have dedicated fields. If the client changes a decision, replace the
record for that subject; do not retain conflicting decisions.

## Required measured space

Collect the raw readings without subtracting any allowance. The installation
arrangement and labelled shape decide how many readings are useful:

1. `width_measurements`: if both sides are fixed, normally record `bottom`,
   `middle`, and `top` between the same side boundaries at three useful heights;
   otherwise record one `single` width from the fixed or intended left edge to the
   fixed or intended right edge. These internal names do not override the labelled
   measurement plan shown to the client.
2. `depth_measurements`: when the depth is freely chosen, record one `single`
   intended depth from the back to the wardrobe front. When the front must finish
   flush with a fixed line, record `left`, `middle`, and `right` readings from the
   back boundary to that required line.
3. `height_measurements`: if the wardrobe reaches the ceiling, record the useful
   left-to-right positions that define and check the top boundary, including every
   place where a flat, slope, or step begins or ends. If it is open above, record
   one intended height.

Each height measurement contains:

- `distance_from_left`: horizontal distance from the inside-left edge;
- `height_from_floor`: vertical height from the finished floor.

Translate ceiling descriptions directly when height is fitted:

- A flat ceiling normally uses left, centre, and right readings; preserve small differences rather than flattening them.
- One continuous slope uses its labelled endpoints plus useful intermediate readings that can verify the real surface.
- A flat section followed by a slope requires the exact labelled junction where the slope begins plus the other readings needed to define and check both sections.
- Additional flats, slopes, or steps require a reading at every stated change.

Require the first distance to be `0`, the final distance to cover the calculated usable width, and all distances to increase from left to right. Preserve every raw reading and measured change point. Never average readings, reorder points, extend a section, or infer a missing endpoint to make the outline pass.

## Apply the fitting allowance

Keep the raw measurements unchanged. Translate the labelled-edge and flush-depth
answers into whether each dimension must fit between fixed boundaries under
`fitted_dimensions`:

- `width` is true only when both the labelled left and right edges are fitted. One
  fitted side and one open side is not enough.
- `height` is true only when the labelled floor edge and every labelled top edge
  are fitted. An open top edge makes height false.
- `depth` is true only when the wardrobe must fit between its back boundary and a
  required finished-front line. The front remains open.

Store the template's positive `fit_allowance` value of `2 mm`. Subtract it once only from dimensions fitted at both ends:

- fitted width uses the smallest width reading minus 2 mm;
- fitted height uses the measured or interpolated height minus 2 mm before base height and chosen ceiling clearance are removed;
- flush depth uses the smallest depth reading minus 2 mm;
- a freely chosen dimension uses its measured value without the 2 mm subtraction.

This is built-in AIkea fitting knowledge, not a client design question. If the
project uses centimetres, store the same allowance as `0.2 cm`. If it uses inches,
store it as `0.0787401575 in`.

## Required internal design values

The template supplies `fit_allowance`. Collect the remaining internal values:

- `fitted_dimensions.width` and `fitted_dimensions.height`, derived from the
  labelled-edge answer, plus `fitted_dimensions.depth`, derived from the separate
  flush-depth answer;
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

Never use the term `width shares` with the client. Ask one natural numbered
question:

1. All sections should be the same width.
2. One or more sections should be narrower or wider.
3. Help choose the widths from what the client needs to store.

If the client chooses `2`, ask the narrower-or-wider relationship as the next
single topic.

Translate the answer to shares internally and present the resulting cabinet widths back to the client.

## Decide the next response

Build one checklist containing every required measured-space field and shared setting. Count explicit zeros as present.

- **Missing measured space:** Ask for only the next missing measurement topic. Do not ask about wardrobe choices yet.
- **Missing wardrobe choices:** Once the measured space is complete, ask for only the next missing choice topic in client-facing language. The shape and labelled-edge fit must already be settled before asking about the section layout. Do not re-ask supplied values or expose internal field names.
- **Contradictory:** Name the exact conflict and ask only for the correction required. Retain all non-conflicting values.
- **Complete:** Do not ask another question. Save the global specification and run the calculator privately. A valid result completes this step and permits later cabinet design.

When the user corrects one value, change only that value unless the correction necessarily changes a dependent measurement such as the right-edge ceiling distance after a width change.

## Write the global project file

Use `assets/aikea.yaml` as the exact schema.

- Copy it only when `aikea.yaml` does not already exist.
- Update an existing file in place and preserve values the user did not change.
- Fill only user-supplied measured facts and confirmed shared design settings.
- Preserve confirmed geometry interpretations under `design_decisions`, including
  the client's supporting statement and the effect AIkea may apply.
- Keep height measurements in their measured left-to-right order.
- Preserve every supplied width and depth measurement. Store `single` for a freely
  chosen dimension and the three named readings for a fitted one.
- Record width and height fit from the labelled-edge answer. Record depth fit from
  the separate flush-depth answer. Never infer a fitted dimension from one fixed
  edge alone or from the fact that a wardrobe front is open.
- Preserve the template's 2 mm fitting allowance unless the user explicitly changes the project policy.
- Do not add calculated cabinet dimensions to `aikea.yaml`.
- Do not add fields that are absent from the template.

## Require the deterministic check

Run the bundled calculator only after the checklist is complete. Require all of these to pass:

- every required input is present and numeric;
- all lengths and thicknesses are positive, except confirmed clearances and gaps may be zero;
- the number of width shares equals `cabinet_count` and every share is positive;
- a fitted width has three named readings, while an open width has at least one;
- a flush depth has `left`, `middle`, and `right` readings, while a freely chosen
  depth has one `single` reading;
- a fitted height has at least three measurements covering the usable width in increasing order, while an open height has at least one;
- the 2 mm fitting allowance leaves every fitted dimension positive;
- clearances and cabinet gaps leave positive cabinet width;
- the base and ceiling clearance leave positive cabinet height;
- door and back thicknesses leave positive cabinet and inside depth.

On success, tell the client that the measurements and shared choices are saved and checked, then summarize calculated cabinet widths, left/right positions, left/right heights, door widths, cabinet depth, and inside depth. Do not mention the file path or checking mechanism unless asked. Stop after presenting these overall results.
