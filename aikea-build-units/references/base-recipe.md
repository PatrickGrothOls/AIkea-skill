# Adjustable cabinet-base recipe

Floor-standing cabinets use Hettich Korrekt adjustable feet, a deck and a front
kickboard. `BaseTaxonomyBuilder` now emits deck/kickboard modules; the configured
builder applies `KorrektBaseFeature` through the existing `KorrektComponentFeature`.
It never substitutes sheet braces for a missing foot installation. Older saved
rail/brace projects remain historical inputs and require explicit migration.

## Height and stock

Overall base height includes the deck. `KorrektBaseLayout` checks the remaining
support height against article 70151's official 74–110 mm adjustment range.
The supplied checksum-bound foot CAD is one 80 mm-high solid. The current builder
rejects a deck underside below that source pose; it does not scale the foot or
pretend that the available solid has an adjustable joint. For example, 95 mm
base minus 16 mm deck leaves 79 mm: physically inside the article range, but the
unchanged CAD plug intrudes into the deck. A separately declared 15 mm deck
proposal leaves 80 mm without altering cabinet/room height. Obtain suitable stock
or a verified adjusted source pose before accepting a different arrangement.

A source-derived floor placement does not prove the socket fit. Keep measured
plate/foot intersections, insertion depth, installation, load distribution,
anti-tip fixing and selected fasteners visible as outstanding qualifications.

## Ownership and machining

The base owns each deck, kickboard, exact 61854 plate and exact 70151 foot once.
Every article has its own one-piece purchase identity. Four plate screws are
additional purchases/selection work; they are not included with the plate.
Source files stay local-only via `$aikea-source-hardware-cad`; never ship them in
the skill. Review resolves the exact source solids and retains their native shape.

Use the existing [Korrekt mounting operation](korrekt-mounting.md): four Ø3 mm
through pilots and one Ø8 mm adjustment passage. Check the **whole rotated plate**
against the assembled deck boundary, with a declared margin (default proposal
15 mm), not only its screw holes. Keep the foot's whole contact disk behind the
kickboard. Station spacing is a proposal, not a calculated load rating.

A cabinet floor above the deck is a separate owner. Apply
`KorrektFloorAccessFeature` with the same axes transformed into that cabinet's
frame; it cuts aligned Ø8 mm passages through the floor. The real tool route must
remain open after drawers, shelf loads and floor finishing are installed.

`BaseModulePlanner` retains CNC-sized deck/kickboard segments. Module seams,
kickboard clips, cabinet-to-base fastening and load/anchoring evidence remain
explicit unresolved requirements until their actual construction is selected.
Common builders/checks consume the current feature result; do not edit derived
part solids after export or hide unknown joints merely to obtain a passing check.

## Deck segmentation

Choose deck sections from the client's intended segmentation, sheet size/orientation, usable CNC area, handling and seam support. Deck count is independent of cabinet count; never default to one deck per cabinet. Use `BaseModulePlanner` with the actual constraints and prefer useful cabinet-gap seams. Check the full foot/plate footprint and its required edge margin on each side of every seam, retain aligned cabinet-floor access, and provide deliberate assembly clearance. A section wider than a sheet's short side can still fit along its long side; verify the two-dimensional nesting before adding another seam. Keep the adjustable-foot/deck construction and intended footprint; segmentation does not authorize a brace plinth.
