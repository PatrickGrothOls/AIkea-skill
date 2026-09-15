# Cabinet construction defaults

## Scope and approved requirements
Replace the floor-standing rail/brace default with Korrekt adjustable feet, deck and front kickboard. Ordinary storage shelves use adjustable supports; fixed Cabineo shelves require a recorded deliberate choice and underside pockets. Structural floors/tops are independent. Preserve the trial room envelope and 95 mm base; exact hardware compatibility, loads and purchase evidence remain separate checks. Parent owns viewer changes.

## Work packages
- [x] WP1: Inspect reusable base, shelf, Korrekt mounting and generated construction boundaries.
- [x] WP2: Implement reusable default rules, physical support declarations and targeted regression tests.
- [x] WP3: Verify exact foot/deck geometry and update the private cabinet recipe with real supports and aligned floor access.
- [x] WP4: Run targeted tests, scope review and commit one coherent default slice.
- [ ] WP5: Rebuild current CAD review artifacts once at bounded resource settings and report readiness limits.

## Current state
Reusable defaults and the private corrective recipe are implemented. Base generation emits only CNC-sized decks/kickboards and applies exact Korrekt pairs through the existing component. The available native foot pose rejects a deck underside below80 mm even though the physical product can adjust down to74 mm. Storage-shelf policy rejects unrecorded Cabineos and top-face fixed pockets. Adjustable shelf support features own four Duplo purchases and matching blind bores; floor access is a separate component.

The private trial preserves2475×450×2374 mm and95 mm base. Parent approved a clearly marked15 mm base deck/kickboard proposal under unspecified base stock;16 mm cabinet stock remains unchanged. Sixteen exact foot/plate pairs are planned, four per cabinet, with aligned floor-access holes. Thirteen adjustable shelves retain52 support purchases and five selectable32 mm rows at their actual front/rear support columns. Six drawers remain unbuilt, and hinge width/overlay issues remain explicit.

The native source files match both package hashes and contain valid single solids. At79 mm deck underside, exact foot-to-machined-deck intersection is950.7166 mm³; at80 mm it is0. Plate/foot intersection at80 mm remains2807.8024 mm³. This is a socket-fit qualification boundary, not proven mechanical compatibility. No scaling/articulation was invented.

Bounded targeted suite: **40 passed, 1 deselected in84.18 s**, exit0. Command: `direnv exec . env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python -m pytest tests/test_cabinet_construction_defaults.py tests/test_adjustable_shelf_taxonomy_builder.py tests/test_base_taxonomy_builder.py tests/test_configured_base_construction.py tests/test_base_part_geometry.py tests/test_part_placement_taxonomy.py tests/test_korrekt_mounting_geometry.py tests/test_korrekt_component_feature.py -q -k "not custom_parent"`. Syntax compilation and `git diff --check` also pass. A broader retained ConstructionTreeChecker test was interrupted after17 prior passes/133.65 s inside OCC; it remains pending and has not been weakened. No Blender run is queued. Current artifacts are still superseded until the corrected export completes.

## Audit log
1. User-approved correction, relayed by parent: default adjustable Korrekt base; no brace fallback. Default adjustable storage shelves; deliberate fixed shelf selection and hidden underside pockets. This directly authorizes the implementation choices in scope.
2. Preserve original trial as evidence. Correct reusable behavior and then regenerate current artifacts, without spending time on obsolete full collision/bake work.
3. Exact raw Korrekt files may be reused from Downloads; no old design placement data will be used. Height compatibility must be derived from the source and official product facts.
4. Parent approved15 mm base-deck proposal after exact source probe; preserve95 mm envelope and independently qualify stock, screws and source socket fit.
5. Parent authorized manufacturer-drawing-based Duplo46642 previews, with exact purchase identity and explicit dimensions. Unknown collar surface detail and workshop load proof remain unclaimed.
6. Retain broad construction test as pending; run bounded operation/geometry tests for this checkpoint. No failed or interrupted check is described as green.
7. Scope review found coherent planner/component/orchestration boundaries. Shared generic cutters remain unchanged; legacy base review helpers only gained kickboard compatibility. Existing brace-based evaluation fixtures remain untouched and require later expectation migration.

8. Targeted operation/geometry suite passed40 tests. One broad custom-parent construction check remains explicitly pending; untouched legacy evaluation expectations are not claimed passing.
