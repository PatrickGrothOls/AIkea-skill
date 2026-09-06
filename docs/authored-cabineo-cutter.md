# Authored Cabineo machining cutter

## Scope

Replace the two imported STEP inputs with procedural machining volumes while
preserving the existing panel cuts, including the user's enlarged brass-insert
receiver. Do not replace purchased hardware CAD or change the furniture design.

## Workpackages and tasks

### WP1 - Dimensional proof

- [x] Inspect the existing source pocket and receiver in the placed joint frame.
- [x] Build a procedural prototype from cylinders and the source-panel plane.
- [x] Prove zero added or removed volume in both mating panels against the old cutter.

### WP2 - Runtime replacement

- [x] Replace STEP loading and reference-file alignment with authored geometry.
- [x] Preserve the 9.1 mm diameter, 12.5 mm deep receiver at its existing datum.
- [x] Remove the two STEP files and their special Git tracking rules.
- [x] Document numerical dimensions and the replacement's scope.

### WP3 - Verification

- [x] Lock actual pocket and receiver geometry in focused regression tests.
- [x] Verify paired cuts and generated source/receiver parts.
- [x] Run the complete declared-environment suite and review the diff.
- [x] Commit the cutter replacement as a coherent checkpoint.

## Current state

The prototype removes exactly the same material from representative source and
receiver panels as the legacy cutter: boolean differences are zero in both
directions. Pocket volume is 4568.311275598426 mm³; receiver volume is
812.9852738867837 mm³. The runtime now builds these volumes directly; the two
STEP files and reference-file alignment code are removed. The focused geometry
suite passes 16 tests and 62 subtests. The complete declared-environment suite
passes 467 tests and 72 subtests, with 5 expected skips.

## Audit log

1. 2026-09-06 - The user requested an authored alternative to the STEP inputs and
   clarified that the female cut was deliberately enlarged for brass inserts.
2. 2026-09-06 - Inspection resolved the actual receiver to diameter 9.1 mm, depth
   12.5 mm, and an axis 5 mm from the source face. The replacement preserves
   these existing dimensions without inferring a different insert product.
3. 2026-09-06 - The source pocket is reproduced by three radius-7.5 mm bores,
   clipped at the source edge, with 10.5 mm cutting depth. Their rear centre is
   25.5 mm from the edge; spacing follows their intersections at x = ±5 mm.
   Geometry above the source face removes no panel material and is omitted.
4. 2026-09-06 - Independent scope review retained the existing 150-line paired
   joint integration suite: paired placement, applied solids, and blind receiver
   checks form one coherent contract. Dimensional regression belongs separately.
5. 2026-09-06 - The complete suite passed after the replacement. Skill metadata
   and discovery links also validate; the reviewed code stays within the existing
   cutter, profile, and placement responsibilities.
