# Door and hinge construction

## Ownership

The cabinet owns the fitted door assembly. The door panel owns its blank and
cup-side preparation. The hinged cabinet side owns the shared hardware grid.
The selected hardware profile owns exact purchased-component identity,
manufacturer dimensions, the grid interface it requires, supported door
relationships, source CAD, and movement evidence.

Each hinge has one saved vertical center and one adjacent grid-row pair. The
center locates the cup, cup fixings, mounting plate, closed hardware, and open
hardware; the pair names the existing cabinet holes used by the plate.
Local panel machining stays in each panel's manufacturing frame; only assembly
placement maps it into the cabinet and complete furniture run.

## Door layout before hardware

Resolve the complete front as part of arranging the cabinet run. A registered
hinge is a starting option, not authority to change the client's chosen layout.
For a genuinely wide or heavy leaf, first assess whether adding a door leaf to
the opening solves the load/width concern while preserving useful access and
the intended appearance. Propose that division; do not silently add doors,
narrow cabinets, or add side fillers. There is no universal 600 or 700 mm cutoff.
If division does not solve the concern or conflicts with the chosen design,
source compatible hinges or propose a different door construction/material.

### Reference widths, limits and the client's decision

Read the exact manufacturer's wording. Record explicit maximum dimensions and
loads separately from the reference width used for a hinge-count/load chart.
Absence of wider-door data does not establish a hard maximum or prove suitability.

Before presenting a width concern, calculate the actual leaf width, height,
thickness and mass, including frames, finish and attached hardware. State the
material/density source or assumption and the intended hinge quantity, spacing,
plate and fixing substrate. Compare these with the manufacturer's conditions;
weight and leverage both matter. Do not extrapolate a safe capacity or add an
extra hinge as a cure unless the manufacturer supports that application.

For a modest overrun of a reference width, explain the actual difference in mm
and percent and offer the relevant choices with their physical consequences:

- Keep the requested dimensions as a provisional design, with the unresolved
  qualification and a concrete verification step (supplier confirmation or the
  manufacturer's specified trial fitting). The user may explicitly accept this
  uncertainty; that does not constitute manufacturer or load approval.
- Divide the opening into more leaves, showing the change in appearance/access.
- Narrow the leaves with fitting strips only if the user chooses that compromise;
  explain any resulting on-site fitting work and changed usable dimensions.
- Select another suitable hinge system or lighter door construction where that
  better preserves the design.

For example, a 616.75 mm leaf is 16.75 mm (about 2.8%) wider than a 600 mm chart
reference. Report this as an evidence gap, not automatically as an unsafe door
or a harmless difference. If 600 mm is instead an explicit maximum, treat it as
a product limit; a user acknowledgement cannot turn it into a compliant choice.

Keep the existing layout while awaiting the choice. Save the user's decision,
the exact unresolved issue and its verification step alongside the door review.
An unresolved chart qualification alone need not block a clearly labelled
visual proposal or independent work. Keep fabrication approval unresolved;
known collisions, invalid fixings and hard product limits remain separate checks.
Acceptance of width uncertainty does not waive drawer/hinge movement checks.

Every single door begins with the ordinary left-side hinge. Room boundaries,
slopes, and position in the run do not change that proposal. Only an explicit
client choice changes one door to the right side, and that choice remains part of
the global furniture specification.

The first cabinet remains the complete physical review model. The project-wide
review record lists the proposed hand for every saved cabinet, including any
client-requested exception. Approval confirms the whole proposal; a requested
change returns to the global project choice before review continues.

## First registered profile

The first proof uses these exact purchased items:

- Riex NC70 F000001, clip-on full-overlay soft-close hinge;
- Riex NC50/NC70 F000049, H0 mounting plate with Euro screws.

The public skill records URLs, SHA-256 checksums, solid counts, and unchanged
native bounds. The downloaded STEP bytes remain in the active project's ignored
`hardware/riex/nc70/` library.

For the resolved K6/H0 relationship, the manufacturer drawings establish a
35 mm cup, 12 mm cup depth, 23.5 mm cup center from the door edge, and a 45 mm
fixing pair on a line 9.5 mm farther into the door than the cup center. This puts
the fixing line 33 mm from the door edge. The same drawings establish a 17 mm
overlay, 37 mm mounting line from the cabinet front, and
32 mm mounting-plate fixing separation. The F000049 drawing requires two 5 mm,
12 mm deep cabinet holes, so the plate consumes an adjacent pair from the
cabinet-owned System 32 grid instead of adding hinge-specific pilot holes.

The source closed and open STEP files share one native frame. The open cup body
is a rigid 112.601389 degree movement around the source hinge axis while the
arm's cabinet-owned members remain fixed. The review maps those native states
into the cabinet instead of approximating the movement.

The F000049 source bounds resolve a 52 mm vertical plate envelope and a
19.576999-63.576999 mm front-depth interval after placement. Save both plate
fixing nodes and this physical envelope in the cabinet hardware map. A different
node is not sufficient clearance: the plate must also avoid the complete
installed envelope of drawer runners, shelf contacts, and other fittings.

## Required evidence

Before a door can be repeated, its saved result must expose:

- the exact door relationship and gaps;
- the selected hinge and matching plate identity;
- the resolved quantity and every shared placement;
- paired machining in the door and cabinet side;
- material containment and retained panel thickness;
- the closed fit and the manufacturer's open state;
- the client's reviewed opening decision for the complete run;
- collisions with cabinet parts or other owned features;
- all profile compatibility findings.

The current 741 mm-wide proof door exceeds this profile's published 600 mm width.
Its visual mechanism proof does not qualify that installation. Apply the
decision process above: establish whether the source specifies a limit or chart
reference, assess a divided front and alternative hardware, and obtain the
client's layout choice before regenerating it. Do not force a narrower layout
merely because this was the first registered hinge.
