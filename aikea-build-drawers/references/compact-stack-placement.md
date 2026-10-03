# Compact stack placement

Start the first structural front 3 mm above the actual cabinet floor top, leave
3 mm between adjacent fronts and finish 3 mm below the cap-shelf underside.
These are initial operating gaps, not movement or hardware qualification.
Check real fit before delivery. Larger gaps require an explicit user exception.

Place the cap shelf on its required shelf-pin rows first. Measure its underside
relative to the cabinet floor top, accounting for pin support height and panel
frames. Do not use a shelf hole center as the shelf underside. The shelf grid
remains unchanged; runner axes do not have to occupy its rows.

For the KA 5332 route, after saving all requested drawer children, run:

```sh
python <drawer-skill>/scripts/compact_hettich_ka_5332_drawers.py <project>/aikea.yaml --assembly <cabinet-id> --cap-underside-mm <measured-height-above-floor-top> --hardware-directory <exact-hardware-directory>
```

This rebuilds the saved collection together. It uses the agent-proposed heights
as approximate proportions of the available space, preserving drawer identities,
depth and stock. Upper runners reuse suitable shared rows to avoid partially
overlapping existing shelf holes; box heights fill the intervals with 3 mm gaps.
The first drawer retains its floor-adjacent position. It generates runner holes,
and rejects physical reservation conflicts rather than shifting a drawer. It
does not create or move the cap shelf. Do not use proportional resizing for
client-fixed heights; use explicit `DrawerLayout` values with
`snap_to_system_32=False`, resolve the cap and check the resulting gaps.

For first-time KA 5332 Python composition, call
`HettichKa5332CompactStackPlanner.plan(host, layouts, cap_underside_mm=...)`
and pass the returned layouts directly to
`HettichKa5332CabinetDrawersGenerator.generate`. Layout heights are proportions,
not minimum-capacity requirements. If a resulting drawer is too short for its
runner, bottom or intended contents, revise the proportions or cap position.

Save `assemblies/drawer-layout-policy.json` with real floor, cap, front and side
paths as specified in the [complete installation contract](complete-drawer-installation.md#enforced-review-and-completion-evidence).
The full wardrobe review now requires compact-layout evidence and measures
actual geometry even while travel qualification is pending. This limited check
does not pass the full installation/fabrication gate or prove drawer joinery.
Neither a successful calculator nor a rendering replaces those remaining checks.
