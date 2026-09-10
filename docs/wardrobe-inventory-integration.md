# Wardrobe inventory integration

## Scope
Integrate the existing physical item counter and sheet estimator onto refreshed main, then reconcile the seated-middle wardrobe with the proposed Korrekt leg base. Preserve the existing design. Establish actual thicknesses and an explicit 16 mm stock scenario; do not disguise a stock scenario as regenerated construction.

## Current state
Implemented on origin/main 52f3dbc in feat/wardrobe-inventory-integration. Imported the physical counter and sheet planner from db0336d/4988d2c without the unrelated installer stack. Added explicit root selection and labeled stock scenarios/non-sheet selections. Fresh regression evidence: 512 distinct tests pass, 5 expected skips, 72 passing subtests. Nine skill/link checks pass. The full run had 507 passes and five socket-permission failures; rerunning the two viewer files with localhost access passed all six tests and cleared every failure.

Actual furniture_legs_01 was built using its frozen authoring runtime plus four existing Korrekt helpers. Main alone cannot yet build it: its composition runtime lacks strict joint machining and the Korrekt extension. No implementation fallback silently bypasses that dependency. Original source remains unchanged; the evaluated copy adds only explicit purchase metadata for the 28 modeled Hettich items. Generated physical records are equal before and after.

The inventory has 103 sheet parts and one custom round wooden rod, 128 verified Cabineo occurrences and 128 matching inserts, 14 Hettich 70151 feet and 14 61854 plates. A separate direct graph/cut-pair reconciliation agrees. Ten doors and two drawers exist but exact hinges, runners and handles are not installed. Lighting, rod supports, kickboard clips and remaining attachment coverage are also open. This is an incomplete order.

The original 1268 × 1550 niche back does not fit 1220 × 2440 stock. Actual mixed-thickness stock places 20 sheets and leaves that back unplaced. All-16 mm stock places 16 sheets and leaves it unplaced. A separately labeled stock scenario splits that back into two 634 × 1550 rectangles, yielding 104 sheet panels plus the rod, all placed on 18 sheets. This retains original face dimensions and does not regenerate construction or validate the seam. The original CAD still has 80 panels at 18 mm, 13 backs at 6.5 mm, eight drawer pieces at 15 mm and two bottoms at 9 mm.

Local evidence is under local-evidence/ (ignored); a durable report copy is saved under the original checkout's dist/wardrobe-inventory-2026-09-09. No supplier CAD or full customer project will be committed.

## Work packages
- [x] WP1: Integrate existing counter with its focused regressions.
  - [x] Import only counter runtime, generation contracts, references and tests.
  - [x] Run counting and hardware regressions.
- [x] WP2: Integrate existing rectangular sheet planner.
  - [x] Import planner, validation, report and tests.
  - [x] Run planner and combined focused tests.
- [x] WP3: Reconcile the actual wardrobe.
  - [x] Record source identity and retain individual panel/hardware paths.
  - [x] Reconcile panels, Cabineos/inserts, drawers, hinges, handles, legs and lighting.
  - [x] Report unsupported/absent declarations without guessing quantities.
  - [x] Validate 1220 x 2440 sheet layouts and explicit 16 mm scenario.
- [x] WP4: Review and save the real-design evidence.
  - [x] Test failure cases encountered in integration.
  - [x] Save readable results and report limitations.
  - [x] Review diffs and commit coherent checkpoints.

## Merge closure
- [x] Recheck refreshed origin/main and final diff; no blocking findings.
- [ ] Pass hosted CI, merge into main and verify remote state.
- [ ] Preserve local design evidence and remove the completed branch/worktree.

## Audit log
1. 2026-09-09: Patrick approved integrating the counting and sheet-estimation tools and verifying the seated-middle wardrobe first. This permits the focused work above; installer, unrelated feature stacks, supplier prices and fabrication fixes are deferred.

2. The scoped integration preserves the existing inventory protocol and generated hardware contracts. All changed/imported code files were reviewed against the 150-line threshold; none exceed it. No unrelated refactor was needed.
3. Actual-project execution exposed the missing composition/Korrekt runtime dependency. Evaluation uses the saved project runtime explicitly; it does not pretend the other stacks have landed on main. An independent direct graph walk validates panel paths, paired cuts and physical hardware counts.
4. One existing custom rod would have been treated as sheet material by the original counter/planner combination. Explicit non-sheet selection retains that item in the inventory and reports it separately. Tests reject unknown/duplicate selections and prevent filtering from concealing corrupted source records.
5. Patrick's previously agreed all-16 mm comparison and split back from the finishing request are recorded as stock scenarios. Panel face sizes, cabinet geometry and original files remain unchanged. Positive finite thickness, source hashes, missing hardware and oversized panels are preserved and tested.
6. The first broad pytest command also collected the copied project's archived tests. This caused duplicate module/import collection errors; the repository suite was then explicitly limited to tests/. No production-code change was made for this environment issue.

7. Final verification: 512 distinct tests passed, 5 expected skips and 72 subtests passed. The only full-suite failures were sandbox localhost bind denials; six tests across their two files passed with socket access. Package verification passed all nine skills. Source-to-layout reconciliation accounts for every one of the 104 proposed sheet rectangles exactly once; 18 SVG sheets and scenario limitations are present in the HTML. No new model-driven usability eval or physical fabrication test was claimed.

8. 2026-09-10: Patrick authorized final review, merge and cleanup. Refreshed origin/main remains 52f3dbc, so the tested production diff is unchanged. Final review rechecked purchase ownership, paired Cabineo counts, failed-run invalidation, sheet accounting, explicit stock scenarios, source preservation and generated-contract compatibility. No blocking finding. Nine skill/link checks passed again. The scope is the counter/planner; outstanding furniture design work is tracked separately and does not hold this tooling merge open.
