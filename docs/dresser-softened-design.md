# Softer eight-drawer dresser

## Scope

Patrick asked to make the existing functional dresser beautiful, permitting a
separate router finishing step while preserving single-face CNC structural work.
Use the same 1800 × 600 × 930 mm prototype and paired Cabineo construction.
Do not change global defaults or represent this styling trial as fabrication ready.

## Current state

- Baseline `83d22a2`; refreshed `origin/main` is an ancestor.
- Isolated branch `test/dresser-softened-design`; original trial is preserved.
- Design direction: softer corners, a rounded thick top, wider finger grips,
  gentle leg arches and a finished frame visible between or behind open drawers.
- Changes are design proposals under Patrick's trial authorization. The final
  complete geometry is valid; no overlaps, invalid solids or uncertain intersections.
- Runner holes/motion, lighting, loads, stock suitability and CAM remain unresolved.

## Work packages

### WP1 — Form and process

- [x] Read the current construction and review contracts and preserve the source.
- [x] Separate structural CNC operations from authorized secondary edge finishing.
- [x] Define actual radii and affected edges; measure retained joint material below.
- [x] Review the proposed form against the original construction.

### WP2 — Build and verify

- [x] Add a small explicit edge-finishing tool using the shared cut contract.
- [x] Build rounded top, fronts, grips, frame and side/leg transitions.
- [x] Check actual solids, Cabineo preservation and structural entry faces.
- [x] Review the completed work with the code-boundary review skill.

### WP3 — Show the difference

- [x] Capture matching before/after views plus useful details and open view.
- [x] Prepare the proposed form and practical finishing sequence for review.
- [x] Save evidence and a coherent local commit.

## Design and machining record

- Top: 24 mm corner radius in plan and 8 mm rounding on its upper perimeter.
- Drawer fronts: 6 mm corner rounding and 3 mm rounding at the exposed face.
- Grips: 220 × 20 mm through-openings with R9 corners, followed by the exposed
  face's R3 edge treatment. These are actual openings, not added handles.
- Side/leg openings: R70 upper transitions; R6 rounding on the long front/back
  outside edges. The curved openings themselves retain their CNC-cut edge.
- Front frame: R2 visible-edge rounding, including the eight drawer openings.
- The CNC stage retains 54 compatible parts and no conflicting declared faces.
  Its hash is `e4d04f38989146691c04fae00c82676ba50aa2e03f2cb751621231c19f120924`.
- That stage is saved separately at `local-evidence/dresser-cnc/`. The proposed
  finished tree is at `local-evidence/dresser/`. Finishing is explicit in its
  operation history; a full-tree face audit cannot claim the finishing is CNC qualified.

## Evidence and review

- `local-evidence/dresser/reviews/dresser_01.geometry-check.json`: 54 valid parts;
  zero out-of-envelope items, overlaps or uncertain intersections. All declared
  cuts are present. Secondary finishing remains an unqualified extension.
- Final construction hash:
  `8bf711fd0ba5d533d4a47a33292069f0bd87bff4b11d4c5ad849854ba9fc00ed`.
- `finishing-evidence.json` uses that same hash: 12 finished parts; minimum
  measured distance from removed finishing material to Cabineo cutter geometry
  is 4.272 mm at the front frame. This does not establish required joint strength.
- `physical-inventory.json`: 54 manufactured parts, 232 verified Cabineos and
  232 matching brass inserts. Runner hardware is still not installed in the tree.
- Nine focused rounding/face-audit tests passed, including analytic roundover
  volume, existing bore preservation, shared feature application and qualification.
  The final three rounding tests also passed after adding the explicit check
  that secondary finishing cannot receive a compatible full-tree CNC face result.
- Four CAD viewers returned HTTP 200 for both page and model, with no browser
  errors. All four comparison tabs passed at 736, 360 and 320 pixels in light
  and dark appearances. Actual model screenshots and the mobile detail view
  were visually inspected.
- Code-boundary review: PASS. New 50-line `panel_edge_finish.py` owns only an
  explicit finishing operation and its removed geometry. The 38-line private
  finishing recipe owns this dresser's edge/radius choices. Shared builders,
  face auditor, fabrication gate and viewer have not gained design-specific rules.
- The rejected first attempt is retained under `reviews/first-rounding-attempt/`.
  Its fit result is superseded, not suppressed or made green through tolerances.

## Audit log

1. 2026-09-12 — Patrick explicitly permitted secondary router finishing. This
   does not relax the structural single-face rule or approve a second CNC setup.
2. 2026-09-12 — Keep the original prototype intact. Profile finishing must be
   explicit in the part history, not a viewer-only geometry alteration.
3. 2026-09-12 — Use understated curved edges and repeated grip proportions as
   the first design direction. Dimensions and finish remain proposals for review.
4. 2026-09-12 — Full perimeter fillets around the shaped sides produced inconsistent
   CAD Boolean volumes at tangent contacts. Limit side roundovers to the long
   straight outer edges while keeping the R70 arch profile. The rebuilt complete
   tree passes the unchanged geometry checker with no uncertain intersections.
5. 2026-09-12 — Keep this checkpoint additive: the finishing tool, its tests and
   documentation ship together. Project recipes, intermediate geometry and local
   review scripts stay under ignored `local-evidence/`; no push or merge.

## Local review files

- `local-evidence/dresser/assemblies/dresser_01/finishing_recipe.py`: editable
  appearance choices, removable through `DresserBuilder(finishing=False)`.
- `local-evidence/dresser/reviews/`: checked closed GLB, open view, isolated
  front/leg parts, inventory and retained connector clearance measurements.
- `local-evidence/dresser/reviews/screenshots/`: before/after/detail/open images
  and the browser/layout verification records.
- `local-evidence/softened_review.py`: repeat review exports and measurements.
- `local-evidence/serve_softened_design.py`: standard loopback viewers.
- `local-evidence/capture_softened_design.cjs`: matching screenshot cameras.

Production sequence proposal: cut profiles and joinery from the declared CNC
face; perform exposed-edge rounding as a separately planned router operation;
sand and finish a sample before choosing the final material/coating. Exact
tooling and access still need review, including any substitution of CNC profile
bits for the separate router operation.

## Tool references

- [CMT roundover router bits](https://www.cmtorangetools.com/eu-en/industrial-router-bits/roundover-router-bits)
  establish the ordinary router tool family for eased edges.
- [Amana CNC rounding/chamfer profile systems](https://www.amanatool.com/products/cnc-router-bits/profiling-cnc-router-bits/double-rounding-chamfering-insert-cnc-router-bit-systems.html)
  establish that CNC profile tooling exists. Exact tooling, machine clearance,
  hold-down, feeds and profile compatibility have not been selected or approved.
