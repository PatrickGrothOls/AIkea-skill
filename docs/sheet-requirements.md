# Sheet requirements from the physical inventory

> Historical implementation record imported from the earlier feature branch. Current integration and fresh evidence: [wardrobe-inventory-integration.md](wardrobe-inventory-integration.md).
## Scope and current state

Patrick requested the number of 1220 × 2440 mm sheets needed after the parts
counter. This branch, `feat/sheet-requirements`, follows `feat/physical-item-counter`.
Use the same 61-panel synthetic assembly to demonstrate the next step; an accepted
customer design remains unselected. Implementation and the fixture demonstration are complete. Customer material
and grain decisions remain unresolved before purchasing.

## Work packages

- [x] WP1 — Inspect the existing Vilja nesting implementation.
  - [x] Identify reusable rectangular packing and its project-specific imports.
  - [x] Record margins, spacing, rotation and material assumptions.
- [x] WP2 — Produce generic, inspectable sheet requirements.
  - [x] Consume the counter's manufactured-part instances; preserve full paths.
  - [x] Separate material/thickness groups and retain unresolved material identity.
  - [x] Nest bounding rectangles with configurable rotation and clearances.
  - [x] Validate complete coverage, bounds and spacing; expose oversized parts.
  - [x] Export a JSON report and browser-viewable sheet diagrams.
- [x] WP3 — Verify and demonstrate the result.
  - [x] Test repeated IDs, incompatible stock, rotation, gaps and oversize parts.
  - [x] Run the same 61-panel inventory through 1220 × 2440 mm sheets.
  - [x] Update skill guidance and the overall plan; review and commit.

## Audit log

1. Patrick explicitly selected 1220 × 2440 mm stock. The current input is the
   previously demonstrated fixture, not an inferred customer design.
2. The Vilja planner uses 10 mm margins and 8 mm part gaps. Reuse these as stated
   provisional planning assumptions, with 90-degree rotation allowed for this
   demonstration. They are not newly approved machining or grain requirements.
3. The existing 222-line layout module received the required bounded scope review.
   Separate numeric records, placement search, and validation for generic reuse.
   Do not import its customer-specific panel builders or alter the Vilja project.
4. Packing is a deterministic heuristic over bounding rectangles. Report a
   feasible sheet estimate, not a proven minimum. Preserve sloped outlines for
   traceability without claiming shape-aware nesting. Missing material and grain
   rules remain explicit before purchasing or pricing.

5. Testing exposed wasted shelf capacity when only the shortest-height orientation
   was preferred. Compare both narrow-first and short-first preferences, keeping
   the feasible result with fewer sheets. The fixture improved from 19 to 18
   sheets; this still does not prove optimality.

## Verified fixture result

| Thickness | Parts | 1220 × 2440 sheets |
| --- | ---: | ---: |
| 18 mm | 51 | 16 |
| 15 mm | 8 | 1 |
| 9 mm | 2 | 1 |
| Total | 61 | 18 |

All parts were placed exactly once, with bounds and gap checks passing. The
calculation uses 10 mm margins, 8 mm gaps, and 90-degree rotation. Missing material
IDs are provisionally pooled by thickness; this is not a customer purchase order.

Passed 24 tests covering the generated inventory integration, packing choices,
stock grouping, complete coverage, malformed inputs, corrupted placements,
oversized parts, source hashes and HTML escaping. The direct CLI produced the
same result using a fresh generated fixture and supplier-CAD test doubles.

The input inventory, JSON and standalone HTML are retained in this thread's
`sheet-requirements` artifact folder under Codex visualizations. The JSON records
its exact input SHA-256. No customer project or original Vilja script was changed.
All added/changed Python files remain below 150 lines; the existing Vilja layout
module received the required independent scope review.

Browser verification: the standalone HTML rendered in an isolated headless
Chrome session with 18 sheet cards, 61 panel labels and no horizontal overflow
at 1200 px. The screenshot was inspected and retained with the report.
