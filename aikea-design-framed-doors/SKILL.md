---
name: aikea-design-framed-doors
description: Design framed cabinet and wardrobe fronts, including separate backing panels and applied frames. Use when a framed or Shaker-style door, drawer front or decorative panel is wanted, or when splitting its construction into physical pieces.
---

# Framed door design

Offer a convenient construction method while keeping the door design open.
A framed appearance may come from a routed single board, an applied continuous
frame, separate rails and stiles, or a frame carrying an inset panel. Choose from
the active project's appearance, materials, dimensions and manufacturing needs.
Use the client's explicit choice when supplied. This skill neither makes framed
doors the default nor limits the designs available to the model.

Read [the client conversation contract](../aikea/references/client-conversation.md)
for client-facing work. Use only the active project's measurements and choices.

## Choose and save the construction

Separate the visible profile from how it is made. Set the outline, openings,
border widths, layer thicknesses, materials and attachment method in project
specifications. Reuse existing fitting gaps and door placements when changing
construction. A prior example's dimensions are not defaults.

For a flat backing with a glued-on continuous frame, use the optional
[applied-frame helper](references/applied-frame.md). It produces two real parts
and one explicit adhesive relationship through the existing assembly contracts.
It supports rectangular fronts, unequal borders and square or rounded opening
corners. Door, drawer-front and fixed-panel ownership comes from the parent.

For another construction or outline, use the
[construction tools](../aikea-design-furniture/references/construction-tools.md)
and the [authored assembly contract](../aikea-design-furniture/references/authored-assemblies.md).
Author or adapt the necessary panel, profile and joint builders. A helper's
supported shape is a local capability boundary, not a reason to change the
client's design or reject another door. A plain slab does not need this helper.

## Keep physical pieces explicit

- Give each independently cut backing, frame, rail, stile or insert its own
  part, manufacturing frame and blank dimensions. Preserve their door-owned
  assembly so all pieces move together when the door opens.
- Resolve material and attachment together. Use
  [$aikea-choose-materials](../aikea-choose-materials/SKILL.md) when material advice
  is needed; do not force MDF, the example thicknesses, or a glue product.
- Record glue contact without inventing machining cuts. If a connection needs
  grooves, rebates or fasteners, return that real work to its participating parts.
- Apply the current [CNC limits](../aikea-build-units/references/panel-construction.md)
  to every blank, including the frame before its opening is removed. Plan corner
  radii, cutter access, hold-down and any hand finishing explicitly.

## Fit and review

When hinges are required, continue through
[$aikea-build-doors](../aikea-build-doors/SKILL.md) and exact hardware sourcing as
needed. The hinge owns its hardware pattern; the door supplies a mounting surface
and its placement. Lay out the pattern on that surface, then resolve its cuts
into whichever real parts lie behind it. Check depth, screw engagement, load and
collision separately against those solids. A hinge must not require a slab or
choose the door's construction. Moving views carry the complete front assembly.

Build the complete parent with the normal authored-assembly review command and
require its geometry and CNC checks to pass. For a construction-only revision,
compare the resulting occupied volume and placement with the previous front.
Show the closed result and, when useful, the same pieces separated for inspection
using [$aikea-review-unit](../aikea-review-unit/SKILL.md). A separated view is
presentation only. Geometry success does not settle adhesive strength, tall-door
stiffness, hinge support or fabrication readiness.
