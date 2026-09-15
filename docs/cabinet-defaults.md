# Cabinet construction defaults

## Scope and approved requirements
Replace the floor-standing rail/brace default with Korrekt adjustable feet, deck and front kickboard. Ordinary storage shelves use adjustable supports; fixed Cabineo shelves require a recorded deliberate choice and underside pockets. Structural floors/tops are independent. Preserve the trial room envelope and 95 mm base; exact hardware compatibility, loads and purchase evidence remain separate checks. Parent owns viewer changes.

## Work packages
- [x] WP1: Inspect reusable base, shelf, Korrekt mounting and generated construction boundaries.
- [x] WP2: Implement reusable default rules, physical support declarations and targeted regression tests.
- [x] WP3: Verify exact foot/deck geometry and update the private cabinet recipe with real supports and aligned floor access.
- [x] WP4: Run targeted tests, scope review and commit one coherent default slice.
- [x] WP5: Rebuild current CAD review artifacts once at bounded resource settings and report readiness limits.

## Current state
Reusable defaults and the private corrective recipe are implemented. Base generation emits only CNC-sized decks/kickboards and applies exact Korrekt pairs through the existing component. The available native foot pose rejects a deck underside below80 mm even though the physical product can adjust down to74 mm. Storage-shelf policy rejects unrecorded Cabineos and top-face fixed pockets. Adjustable shelf support features own four Duplo purchases and matching blind bores; floor access is a separate component.

The private trial preserves2475×450×2374 mm and95 mm base. Parent approved a clearly marked15 mm base deck/kickboard proposal under unspecified base stock;16 mm cabinet stock remains unchanged. Sixteen exact foot/plate pairs are planned, four per cabinet, with aligned floor-access holes. Thirteen adjustable shelves retain52 support purchases and five selectable32 mm rows at their actual front/rear support columns. Six drawers remain unbuilt, and hinge width/overlay issues remain explicit.

The native source files match both package hashes and contain valid single solids. At79 mm deck underside, exact foot-to-machined-deck intersection is950.7166 mm³; at80 mm it is0. Plate/foot intersection at80 mm remains2807.8024 mm³. This is a socket-fit qualification boundary, not proven mechanical compatibility. No scaling/articulation was invented.

Bounded targeted suite: **40 passed, 1 deselected in84.18 s**, exit0. Command: `direnv exec . env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python -m pytest tests/test_cabinet_construction_defaults.py tests/test_adjustable_shelf_taxonomy_builder.py tests/test_base_taxonomy_builder.py tests/test_configured_base_construction.py tests/test_base_part_geometry.py tests/test_part_placement_taxonomy.py tests/test_korrekt_mounting_geometry.py tests/test_korrekt_component_feature.py -q -k "not custom_parent"`. Syntax compilation and `git diff --check` also pass. A broader retained ConstructionTreeChecker test was interrupted after17 prior passes/133.65 s inside OCC; it remains pending and has not been weakened. Parent has started the checked Blender presentation. Corrected exports are complete; the earlier brace-base artifacts remain superseded.

## Audit log
1. User-approved correction, relayed by parent: default adjustable Korrekt base; no brace fallback. Default adjustable storage shelves; deliberate fixed shelf selection and hidden underside pockets. This directly authorizes the implementation choices in scope.
2. Preserve original trial as evidence. Correct reusable behavior and then regenerate current artifacts, without spending time on obsolete full collision/bake work.
3. Exact raw Korrekt files may be reused from Downloads; no old design placement data will be used. Height compatibility must be derived from the source and official product facts.
4. Parent approved15 mm base-deck proposal after exact source probe; preserve95 mm envelope and independently qualify stock, screws and source socket fit.
5. Parent authorized manufacturer-drawing-based Duplo46642 previews, with exact purchase identity and explicit dimensions. Unknown collar surface detail and workshop load proof remain unclaimed.
6. Retain broad construction test as pending; run bounded operation/geometry tests for this checkpoint. No failed or interrupted check is described as green.
7. Scope review found coherent planner/component/orchestration boundaries. Shared generic cutters remain unchanged; legacy base review helpers only gained kickboard compatibility. Existing brace-based evaluation fixtures remain untouched and require later expectation migration.

8. Targeted operation/geometry suite passed40 tests. One broad custom-parent construction check remains explicitly pending; untouched legacy evaluation expectations are not claimed passing.
9. Independent integration review found that a fixed-shelf choice without any actual
   joint could suppress its support pins. Require a declared shelf-source Cabineo
   joint before removing default supports; geometric adequacy still has its separate
   checks. This guard does not change the current all-adjustable cabinet recipe.

## Attachment metadata follow-up

- [x] Corrected CAD exported once using the integrated parent skills:134 interior and174 closed render meshes. Shared operation/solid validation passed. Inventory is draft:40 manufactured parts,127 hardware components,86 Cabineos and86 inserts.
- [x] Declare each Korrekt plate/foot's mounting_part_id from its planned BaseModuleSpec and deck ID. This is attachment metadata only; native placement and purchase IDs remain unchanged.
- [x] Bounded attachment tests:2 passed in10.29 s. No CAD solids or new qualification job were built.
- [x] Metadata-only GLB refresh preserves the entire binary chunk, mesh/accessor/buffer-view data, node names and transforms;32 hardware paths gain their deck owner.
- [x] Material outputs and final parent handoff: both corrected material GLBs passed unchanged-geometry/transform checks, contain seven strength-0.35 emitters, and preserve deck attachments and stock/finish IDs.

Audit continuation: exact module ownership now makes feet/plates follow their deck in inspection. This does not qualify socket fit, screws or loads. The completed model exports are distinct from still-incomplete fabrication readiness. Parent owns bake and visual review.

The current interior/closed material assets are `local-evidence/project/reviews/corrected-interior-materials.glb` and `corrected-closed-materials.glb`. Their `.material-check.json` files and the intermediate attached GLBs' `.metadata-check.json` files preserve the full hash chain from the untouched CAD exports. The metadata refresh changes only32 inspection paths. Material preparation adds UV/material data while preserving every original attribute/index accessor and the binary geometry prefix.

## Hinge attachment metadata follow-up

- [x] Trace explicit DoorHostSpec ownership: slab hinge to door_part_id, plate to support_part_id.
- [x] Add these mounting_part_id values in the shared Riex purchase factory without changing placement or purchase identity.
- [x] Bounded owner/pose tests: 5 passed in 81.90 s, exit 0; both hands and both support-face orientations passed without constructing CAD solids.
- [x] Saved new `local-evidence/project/reviews/hinge-attachment-mapping.json`: all 36 purchases reconcile to saved plans and current GLB IDs. Active bake input SHA-256 remains `659cb44a25c198dc6a50880f762b3b48a628e8802762577d89db6cef8e8a4b13`; no existing GLB was written.
- [x] Scope/diff review complete; attachment-only checkpoint prepared for parent integration. Production factory 36 lines, focused tests 62 lines, private mapping script 77 lines; each has one coherent scope.

Audit continuation: parent requested the bounded hinge ownership correction for panel explosion. The slab and carcass owners come directly from the installer declaration, never proximity. Layered-front hinge ownership remains unchanged because its door ID is an assembly datum and the current mounting_part_id contract requires an actual directly owned panel. Plate ownership is still explicit for that route. Door width, overlay, fit and motion qualification remain unresolved. Parent owns any later metadata-only derived baked/inspection assets and their geometry proof.

Validation command: `direnv exec . env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python -m pytest tests/test_riex_hinge_attachment.py -q`. Mapping command: `direnv exec . python local-evidence/project/scripts/map_hinge_attachments.py`. Mapping application and resulting geometry preservation are explicitly pending parent work on new derived files. The first private mapping run assumed positional purchase arguments; the saved repr uses keyword arguments. Corrected the literal AST reader and reran successfully before writing its new report.
