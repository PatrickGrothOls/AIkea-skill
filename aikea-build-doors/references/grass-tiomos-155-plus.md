# GRASS Tiomos 155 Plus construction option

Source the exact F028122660 hinge and F058139748 plate using
[the public STEP route](../../aikea-source-hardware-cad/references/grass-tiomos-155-plus.md).
Read official catalogue pages [518](https://mediacenter.grass.eu/Katalog/EN/518/),
[519](https://mediacenter.grass.eu/Katalog/EN/519/),
[580](https://mediacenter.grass.eu/Katalog/EN/580/) and
[594](https://mediacenter.grass.eu/Katalog/EN/594/) for the selected application.

## Shared implementation

Use `GrassTiomos155Loader.load(project / 'hardware/grass')`, then the existing
`DoorHost` for the actual door and side. `GrassTiomos155Planner.plan(host, count,
mass_estimate_kg, reservations)` resolves placements; `GrassTiomos155Machining.build`
returns paired panel drilling; `GrassTiomos155Hardware.build` returns purchased
component specifications. Apply those through shared panel construction and
include the unchanged loaded bodies in the same assembled tree. Resolve screws
as separate items/holes; do not silently inherit NC70 Euro-screw or open-pose data.
The count and mass are explicit inputs supported by actual material and chart
evidence, not automatic GRASS load approval.

The supported native configuration is left-hand, full overlay, K3 hinge with
3 mm plate, 6 mm cup-edge distance and 15 mm overlay. Its native cup and 37 mm
plate line agree only with a **1.5 mm rear-door gap**. This is not the catalogue's
lateral reveal. Preserve the requested external depth by resolving the carcass
front and all dependent grids, shelf pins, runners and cuts from the same datum.
Do not reuse this gap for a different product without its own source evidence.

The cup is Ø35 ×11.5 mm; cup fixing pair is 45 ×9.5 mm. The plate has a four-point
wood-screw pattern, not two Ø5 System32 bores. Shared code puts its pilot pair
between grid rows and checks the complete closed hinge envelope below a sloping
roof. Any necessary roof-clearance placement change invalidates affected drawer
checks. The current Ø2.5 ×12 mm pilot choice still needs actual screw/stock
qualification; the plate drawing calls for Ø3.5 ×15 mm wood screws.

## Checks and limits

Check exact placed hardware against all wood, including the cup flange, sloping
roof and drawer fronts. Distinct hole centres and valid solids are insufficient.
Keep intentional source clip engagement distinct from unintended wood overlap;
never whitelist every overlap merely because both objects are hardware.

The load chart uses 600 mm reference leaves; apply the shared
[door decision process](door-and-hinge-construction.md#reference-widths-limits-and-the-clients-decision).
The supplied STEP is one fused **closed** hinge, not an articulated mechanism.
Page 518 establishes lateral flushness at 90° for K3/3 mm; it does not supply the
full fore/aft endpoint or moving-arm envelope. Nearby 12/8 mm dimensions belong
to the different K9.5 mitred installation and cannot be borrowed.

An explicitly labelled illustrative open-door view may help inspect the layout.
State which placement is assumed. Keep the door-owned cup/flange attached to its
cup opening and the fixed mounting plate on the carcass; missing arm articulation
must not silently remove all the door hardware. Do not rotate the complete fused
closed hinge as one rigid body with the door.

For the checksum-bound F028122660 source documented above, a source-derived visual
cup partition can retain native y <= -35.35 mm at the observed outer flange face;
its seating plane is y=-38.5 mm and native cup axis is x=5.5,z=0. The resulting
bounds are x[-13,27],y[-49.5,-35.35],z[-31,31] mm. Verify these source datums before
using them; they are not generic hinge dimensions. Preserve the original STEP,
record its hash, retain the partition's exact source surfaces, and declare the
artificial closure at the splitting plane. This is a visual partition, not a
supplier-certified separate component or machining authority.

Transform this cup region with the same door frame and check its opening axis
and seating plane before/after the illustrative pose. Preserve fixed plates and
all other parts; omit only unsourced moving linkage and state that limitation.
Retain the pose/partition provenance. This view provides no full-travel or
fabrication proof.
