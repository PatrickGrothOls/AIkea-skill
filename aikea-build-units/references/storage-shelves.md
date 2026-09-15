# Storage shelves and structural panels

Ordinary storage shelves are adjustable. `ConfiguredUnitBuilder` passes them
through `StorageShelfPolicy` and `AdjustableShelfSupportFeature`, which supplies
four physical Hettich Duplo 46642 support purchases and their side-panel bores.
A panel plus a System 32 grid is not a supported shelf until the actual support
positions and purchases are included. Conversely, support bores or short adjustment
groups do not replace the cabinet's [full-height grid](panel-construction.md#machine-the-cabinet-hardware-grid).
Declare that grid separately before fitting shelves and reuse exactly matching
holes. Default to nearly the full usable cabinet depth, from the necessary front
clearance to the inside back. Seat the shelf on four pins in the cabinet-owned
front/rear columns at a common System 32 row. Derive pin positions from that saved
grid, not from a shortened shelf's ends. Additional columns require a deliberate
arrangement decision, not an automatic workaround for arbitrary shelf setbacks.

A shelf may visually cross or interrupt the side lighting line. Do not shorten it
merely to keep that line continuously visible. Check actual shelf bearing, door
and hinge travel, drawer installation, and any protruding LED profile/diffuser.
Visual overlap is acceptable; physical interpenetration is not. Retain necessary
fit clearances and explain a specific physical conflict rather than silently
restoring a large front setback.

The [official Hettich drawing, page 825](https://catalog.hettich.com/General/TA_2025/en_DE/catalogs/TA_2025_en_DE/pdf/save/bk_827.pdf)
was checked on 2026-09-15. The selected nickel-plated article has Ø5 mm pins,
8 mm insertion and a 0.5 mm stop. The recipe uses 0.5 mm shelf clearance per
side and four supports. Standard columns are 37 mm from the cabinet side panel's
front/rear edges; a shelf setback must not shift those columns. Existing
`AdjustableShelfSupportFeature` inputs are shelf-relative: reconcile their output
with the cabinet grid before claiming the supports follow this policy.
The shelf underside is 2.5 mm above the pin centre. Side holes retain the shared
Ø5 × 13 mm blind grid, giving 8 mm pin insertion and 5 mm depth allowance.
Sixteen-millimetre sides retain 3 mm material behind these bores.

The supplied cylindrical hardware preview is dimension-based, not manufacturer
STEP. It deliberately omits un-dimensioned collar surface detail. The exact
purchase identity, source drawing and dimensions remain explicit. No invented
manufacturer-CAD claim or workshop load proof follows from that preview.
Verify shelf load/deflection, insertion, material, removal and retention for the
actual use. Reuse only exactly matching existing holes; do not merge nearby holes.

Use role `floor_panel` for structural cabinet floors, rather than treating them
as removable storage shelves. Structural floors/tops retain their own joints.
For a deliberate fixed storage shelf, record `FixedShelfChoice(shelf_id, reason)`
and give it its paired Cabineo joints. `StorageShelfPolicy` rejects unrecorded
Cabineos and requires their shelf-source pockets on `<Z`, the hidden underside of
the horizontal shelf. Never make Cabineo the default simply because the operation
is available. Assembly sequence and one-face machining still need their checks.
