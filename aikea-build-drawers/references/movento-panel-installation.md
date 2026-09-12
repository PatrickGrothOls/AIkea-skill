# Four-sided MOVENTO panel installation candidate

`MoventoDrawerInstallation.apply` adds one six-panel drawer, both T51.7601 clips,
both 760H5000S runners and five actual fixing holes in each named host panel. Use
it to develop a complete installation on an authored parent. It is currently an
engineering candidate: exact installed-source geometry, material/fastener fit and
movement qualification remain unresolved. Do not present it as CNC ready.

The installed source set is the existing checksum-gated 500 mm MOVENTO manifest.
Source files must be available in the project's `hardware/blum/movento` library;
the common hardware hydrator verifies and imports them. There is no scaled or
mirrored substitute. Both downloaded locking devices have their own drilling
coordinates. This route does not install the paired Hettich spacer product.

## Inputs and composition

Run inside a generated project's shared contract runtime. Supply the built parent,
a unique drawer ID, `MoventoPanelDimensions`, a `MoventoPilotChoice`, the drawer's
closed local-to-parent placement and its actual left/right supporting part IDs:

```python
parent = MoventoDrawerInstallation().apply(
    parent, drawer_id, dimensions, pilots, drawer_to_parent,
    left_support_part_id, right_support_part_id,
)
```

The drawer frame's X spans the opening, Y follows its depth and Z points up.
Its X=0 and X=clear-width planes must coincide with the chosen mounting faces.
The installer transforms every fixing into the host's real local frame; a fixing
off its selected face raises an error. Existing parent panels, machining,
requirements, children and purchases are retained. A duplicate child ID raises an
error so an authored installation cannot be silently overwritten.

The helper `MoventoPanelDrawer` supplies intermediate panel construction only.
Use the installer above for an actual drawer, then hydrate and review the entire
tree. Repeating only the helper would omit the parent runners and host holes.
Spacers/supports needed by a front frame or door must already be physical, joined
parts in that parent. Resolve their dimensions from the actual aperture and travel;
do not assume the carcass width is also the unobstructed drawer opening.

## Construction and source evidence

The [Blum TD-132/1 installation document](https://d2.blum.com/services/BEC003/me13029704_td_dok_bau_%24sen_%24aof_%24v1.pdf)
provides the nominal drawer and hook preparation (page 5), all five 500 mm
option-B system-screw positions (page 13), and vertical locking-device fixing for
a four-sided drawer (page 19). The shared profile now carries all five fixing
depths: 19, 37, 69, 261 and 293 mm from the drawer-front datum.

The panel recipe uses 16 mm sides/bottom, a 490 mm side length, 13 mm bottom
recess, a separate 64 mm deep × 29 mm thick front mounting rail and a back whose
lower edge is 0.5 mm above the side bottom. These are an explicit construction
candidate, not universal stock or furniture defaults. The rail's underside hosts
the clip pilots and source-derived reliefs. Its two Cabineo positions avoid those
cuts; all panel joins retain the common paired cutter. The visible front is also
the structural front, removing a separate unfastened decorative facade.

`MoventoPilotChoice` records selected host and clip pilot dimensions and their
basis. It is not manufacturer/material approval. The trial uses host Ø5 × 14 mm
and clip Ø2.5 × 10 mm, with 661.1450.HG / 606N as fixing candidates. Actual stock,
screw engagement and supplied quantities must be qualified before fabrication.

## Current limits from the eight-drawer trial

- All six drawer panels and all runner supports have compatible chosen CNC faces.
  The independent drilling requirement fails if locking preparation is removed.
- The raw right-hand runner and nominal Ø6 × 10 mm rear bore leave a small source
  intersection. Do not enlarge or move the bore to conceal that discrepancy.
- The vendor runner representations produce inconsistent CAD Boolean volumes and
  overlap their engaged clips. Exact-source fit remains invalid; no broad contact
  allowance or adjusted tolerance has been added to clear it.
- The flattened source runners are not separated moving-stage CAD. An exploded
  inspection is useful, but does not prove installed extension or swept clearance.
- Production remains gated by the exact hardware/fastener installation, chosen
  stock and Cabineo compatibility, load/stability, tooling, machining exports and
  current user approval. These gaps do not remove the intended drawers from scope.

Use `build_furniture_design.py`, `check_panel_setups.py`, physical inventory and the
fabrication gate on the same complete tree. Do not certify from the panel helper
or its focused tests alone.
