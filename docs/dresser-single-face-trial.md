# Eight-drawer dresser: single-face CNC trial

## Scope

Exercise the shared construction protocol on a demanding freestanding dresser.
Patrick requested a thick top, attractive legs, eight wide drawers, and a visible
frame that looks finished open and closed. His machining constraint is binding:
three-axis CNC, one broad machining face per physical part, no flipping, and
paired Cabineo construction. Geometry alone must not claim this constraint passed.

## Current state

- Baseline: `9cbfbec`; refreshed `origin/main` is an ancestor. Earlier work is preserved.
- New isolated branch: `test/dresser-single-face-trial`.
- Existing tools provide shaped blanks, through-pockets, paired Cabineo negatives,
  drawer sizing/hosts, exact runner hydration, tree review and construction checks.
- Added a separate, non-authorizing face-demand audit; it does not replace the
  fabrication gate or CAM. Its result is bound to the current construction hash.
- Current prototype: 54 wooden parts, 232 matched Cabineos and matching inserts;
  closed geometry valid and all declared entry faces compatible.
- Cabinet/runner pilots, repeated hardware installation, lighting, loads, material
  sourcing, 40 mm tool reach, workholding and CAM remain unresolved. No cutting approval.
- Local project and evidence: `local-evidence/dresser/`. Vendor CAD is not committed.

## Work packages

### WP1: Save the trial brief and architecture

- [x] Record the one-face constraint and distinguish assumptions from measurements.
- [x] Inspect shared operations and drawer-host contracts.
- [x] Identify conflicts: two-sided centre divider, leg/deck opposing bores,
  and inner drawer joinery versus outer runner pilots.
- [x] Save editable prototype dimensions, parts and independent requirements.
- [x] Review the architecture against every requested feature and machining face.

### WP2: Build and check the actual parts

- [x] Build two drawer bays with paired divider sheets and shaped outer sides/legs.
- [x] Add a thick top and one front frame with eight rounded through-openings.
- [x] Resolve eight drawer boxes from the shared recipe; add paired Cabineo joins.
- [x] Assess exact runner availability, installation, and any missing machining data.
- [x] Check declared operation entry faces, paired cuts, ownership and connectivity.
- [x] Run existing complete-tree geometry and requirements checks; retain all failures.
- [x] Review the completed slice and fix defects within the trial scope.

### WP3: Show the result and record its limits

- [x] Export and inspect closed, open and structure views of the same saved design.
- [x] Prepare actual model screenshots/viewer and the discovered capability limits.
- [x] Commit the coherent evidence/documentation checkpoint; no push or merge.

## Evidence and review

- `reviews/dresser_01.geometry-check.json`: 54 parts, zero invalid solids,
  envelope violations, overlaps or uncertain intersections. Applied-operation and
  built-in qualification checks pass; 20 explicit engineering/installation
  requirements remain unresolved.
- `reviews/panel-setup-audit.json`: all 54 parts compatible for declared built-in
  entry faces. Construction hash matches the geometry report:
  `ea8c84b1eba9008a2e18ee30203b909dada9442c84ae33d709c977277f4ca329`.
- `reviews/physical-inventory.json`: 232 verified connector occurrences, 232
  matching inserts, no installed runner solids. Hardware cannot be counted as installed.
- `reviews/connection-graph.json`: no isolated wooden panels; one connected
  14-part case and eight connected 5-part boxes. The nine groups still need the
  runner attachments to connect physically. Every blank fits 1220 × 2440 stock
  by dimensions; this is not sheet nesting or stock-product availability.
- `reviews/hardware-download-availability.json`: both existing vendor downloads
  match approved STEP hashes (9114276 and 13952). Availability does not resolve
  the longer screw, cabinet pilot, drawer fixing or repeated-installation proof.
- `reviews/open.glb` and `reviews/structure.glb`: shared review poses of unchanged
  parts; the open image is not a verified hardware-motion simulation.
- Tests: 19 focused setup/blank/operation cases passed, followed by a final
  6-case setup-check rerun. This branch did not repeat the full baseline suite.
- Browser: three actual GLBs loaded with HTTP 200 and no page errors. All four
  presentation tabs passed at 736, 360 and 320 pixels in light/dark appearances.
- `review-code-boundaries` verdict: PASS. The new checker (70 lines) owns only
  generic entry-face demands; the CLI (52 lines) owns traversal, freshness and
  reporting. Furniture dimensions and topology remain in the private recipe.
  No existing core executor changed or acquired dresser-specific rules.

## Prototype assumptions (not confirmed client measurements or production defaults)

Use a 1800 × 600 × 930 mm envelope, two columns of four inset drawers, a 40 mm
top, 16 mm case internals/drawer sides/bottoms, and 18 mm fronts/drawer backs.
The shared sizing recipe uses the same front/back thickness; the wider visible
front is an explicit recipe adaptation. Outer sides continue into shaped
legs; their thicker stock is a prototype structural proposal. A paired centre
divider avoids opposite-face runner drilling on one sheet. These are editable
test choices under Patrick's authorization to attempt a difficult design.
Material suitability, loads, tipping restraint, finishing and machine tooling
remain unqualified until their actual evidence exists.

## Audit log

1. 2026-09-12 — Patrick authorized a harder design trial. Use existing primitives
   and configurators rather than a furniture-specific cutting engine.
2. 2026-09-12 — Patrick added the explicit single-face three-axis constraint.
   Existing tests do not establish it; do not reinterpret through-holes as requiring
   a second setup, or treat entry-face checks as a complete CAM/tool-reach proof.
3. 2026-09-12 — Proposed paired centre sheets and integrated shaped legs to remove
   known opposite-face conflicts. These remain prototype choices for visual review,
   not changes to the global furniture policy.
4. 2026-09-12 — The shared drawer recipe requires 536 mm outside box depth at
   the proposed panel thicknesses. The prototype is 600 mm deep to retain usable
   frame and back clearance. Front frame receives Cabineos from separate horizontal
   webs; putting its source pockets in narrow stiles would break into the openings.
5. 2026-09-12 — Initial real build passed: 54 parts, no invalid solids, envelope
   violations, intersections or uncertain intersections; all applied operations
   passed independent verification. Declared entry-face audit found no opposing
   demands. A positional-argument mistake in requirement declarations was corrected
   to explicit keywords. Final rerun also adds through-cut finger grips.
6. 2026-09-12 — Replaced sharp concave leg outlines with convex outer profiles
   and shared through-pockets with R25 internal corners. Finger grips use R6
   pockets; exact half-width radius is outside the current pocket tool's contract.
   Final geometry and entry-face checks pass on those actual revised solids.
7. 2026-09-12 — Boundary review keeps this audit separate from manufacturing
   approval. Through openings may share either setup face; opposing blind
   demands and edge/unknown operations fail. Unknown hardware holes remain
   requirements, never implicit passes.

## Reproduce locally

Run from this worktree, using its direnv environment:

```sh
direnv exec . python aikea-review-unit/scripts/build_furniture_design.py local-evidence/dresser --assembly dresser_01
direnv exec . python aikea-review-unit/scripts/check_panel_setups.py local-evidence/dresser --assembly dresser_01
direnv exec . python local-evidence/dresser-tools/review_views.py "$PWD" "$PWD/local-evidence/dresser"
direnv exec . python aikea-review-unit/scripts/serve_unit_review.py local-evidence/dresser/reviews/dresser_01.glb
```

The local probe scripts and screenshots are preserved under `local-evidence/`.
The source recipes are not a built-in dresser product or a fabrication-ready example.
