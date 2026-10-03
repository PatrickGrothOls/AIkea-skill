# Complete drawer installation repair

## Scope

Fix the reusable drawer construction path that prevented the fresh eight-drawer
reference dresser from producing drawers, then rebuild and inspect that dresser.
Every drawer must include exact runners and actual mounting cuts; conditional
hinge spacers and one broad CNC face per part remain required. A blocked partial
carcass is the baseline failure, not the intended result.

Branch: `fix/complete-drawer-installation`, stacked on
`fix/drawer-hardware-contract` at `b6732e0`. Fetched `origin/main` and verified it
is an ancestor before creating this isolated worktree. Original worktrees and
the failed run are preserved. No push, merge or fabrication release is included.

## Current state

The missing-drawer defect is repaired in the authored construction path and the
reference dresser has been rebuilt. It contains eight six-panel drawers, sixteen
exact-source MOVENTO runners and sixteen locking devices. The complete tree has
61 wooden panels, with a compatible chosen broad machining face for every panel.
All 80 runner host holes, 32 clip pilots, 16 rear-hook bores and 16 small runner
reliefs are present. The independent rebuild matches the exported construction
fingerprint. This is an engineering candidate, not a fabrication-ready dresser.

The cause was a gap between the skill's complete-installation obligation and its
available builders. The default KA 4532 route depends on unfinished article 13952
spacer fixing; KA 5332 is a poor candidate for these wide drawers; the legacy
MOVENTO route supplied an unmachined box without complete installation. The fresh
agent therefore withheld every drawer. The new shared installer adds each drawer,
both runners, both clips and actual host cuts together. A batched call does the
same for all eight. It does not silently replace the legacy generators.

Exact installed source geometry remains invalid: the raw runner CAD has Boolean
volume inconsistencies, runner/clip engagement overlaps and a small right rear-hook
discrepancy. These were not hidden by shifting holes, increasing tolerances or
adding broad contact allowances. Pulls, installed motion, stock/fastener
qualification, Cabineo compatibility, loads and final machining approval remain
open. The original independent eight-complete-drawers requirement is retained.

## Work packages

### WP1 — Reproduce and choose the repair

- [x] Verify checkout, upstream ancestry, baseline run and unchanged source inputs.
- [x] Trace product selection, box construction, mounting cuts and declared gaps.
- [x] Verify nominal runner/clip mounting coordinates from primary documents and source CAD.
- [ ] Qualify exact installed CAD engagement and chosen fasteners/materials.
- [x] Capture the zero-drawer baseline; add regressions for missing locking preparation and actual host cuts.
- [x] Review responsibility boundaries and existing files over 150 lines.

### WP2 — Complete the reusable installation

- [x] Implement the sourced mounting candidate through existing shared operations.
- [x] Preserve explicit product choices and require real supports where the aperture needs them.
- [x] Join all six drawer panels without opposing-face machining conflicts.
- [x] Include physical hardware ownership, matching mounting cuts and independent requirements.
- [x] Run focused regressions and independent review using the review skill.
- [x] Commit the generic connector-placement repair separately (`cd6fc7b`).
- [x] Commit the coherent drawer installation, tests and skill guidance checkpoint.

### WP3 — Finish and verify the dresser

- [x] Build one drawer and both actual host mounting patterns.
- [x] Apply the same shared installation to all eight positions.
- [x] Run full-tree geometry, chosen-face and physical inventory checks; retain failures.
- [x] Show the assembled dresser and installed/exploded drawer inspection with screenshots.
- [x] Update skill guidance and review the actual implementation independently.
- [ ] Resolve source-CAD fit contradictions and prove installed drawer travel.
- [ ] Add the requested pulls and their installation preparation.
- [ ] Qualify stock, fasteners, Cabineo product compatibility, load/stability and tooling.
- [ ] Produce and approve current machining exports after those checks pass.
- [ ] Complete the repository-wide regression run before landing; this run was interrupted.
- [ ] Re-run a context-free agent against the qualified complete route before claiming cold-start success.

## Verified result and evidence

The prior zero-drawer project is preserved. The repaired project, downloaded
manufacturer documents/CAD, review reports and screenshots are kept locally under
`local-evidence/`, outside the feature's committed source files.

| Check | Result |
| --- | --- |
| Actual saved tree | 9 assemblies, 61 wood panels, 32 purchased hardware components |
| Drawer inventory | 8 drawers, 16 runners, 16 clips |
| Physical joint count | 213 paired Cabineos and 213 brass inserts; product qualification is separate |
| Installation cuts | 80 host holes, 32 clip pilots, 16 rear bores, 16 reliefs |
| Chosen broad CNC faces | All 61 compatible |
| Complete source geometry | Invalid: 88 uncertain intersections; fabrication ready remains false |
| Focused installation/layout/profile tests | 21 passed, 1 source-download-dependent skip |
| Additional tilted-host regression | 1 passed; real valid host frames also checked independently |
| Downloaded-CAD legacy integration test | 1 failure on both unchanged baseline and this branch: unintended wood overlap |
| Skill package discovery and links | All 11 verified |
| Broader suite | Interrupted after 202 passed and 58 subtests passed in 25:58, inside legacy door/plinth CAD geometry |
| Independent code review | No remaining findings in the final candidate slice |

The focused tests ran on the final production code, including the perpendicular
axis guard. The additional tilted-host test was added and run afterward. The
broader suite began before the final batch/guard edits and is not final-snapshot
whole-suite proof. Its log is preserved; it must not be reported as a green suite.
The exact downloaded CAD was separately hydrated and checked in the real dresser.
The initially skipped environment-driven source-CAD test was subsequently enabled
with those downloads. It failed at `hardware has no unintended wood overlap` on
both unchanged baseline `b6732e0` (43.00 s) and this branch (44.10 s). This is an
existing legacy generator defect, not a passing integration test or a waived
assertion. That baseline checkout remains clean. The candidate's own source-fit
failures are independently retained in the complete dresser report.

Final construction SHA-256:
`67afe7c5929b01ab8de7e80a9f3826e81b73fbe080a5fe6446a3b86438397cd4`.
Canonical GLB SHA-256:
`5642b4ebccb53079c5e69a73c8337dcf3359bf0404dbc76dd8016024db6f7954`.

Key local evidence:

- `local-evidence/repaired-dresser/project/reviews/independent-audit.json`
- `local-evidence/repaired-dresser/project/reviews/panel-setup-audit.json`
- `local-evidence/repaired-dresser/project/reviews/physical-inventory.json`
- `local-evidence/repaired-dresser/project/reviews/dresser_01.geometry-check.json`
- `local-evidence/drawer-installation-review.md`
- `local-evidence/drawer-proof/final-focused-tests.log`
- `local-evidence/drawer-proof/tilted-host-test.log`
- `local-evidence/drawer-proof/downloaded-cad-test.log`
- `local-evidence/drawer-proof/baseline-downloaded-cad-test.log`
- `local-evidence/full-tests.log`
- `local-evidence/repaired-dresser/assembled.png`
- `local-evidence/repaired-dresser/drawer-installed.png`
- `local-evidence/repaired-dresser/drawer-exploded.png`

Inspection GLBs only add the viewer's existing source-CAD label to preserve metal
color; the close-up selects six panels and their four hardware components. Their
binary geometry and transforms are unchanged. They are not motion states and do
not move physical runner ownership out of the parent. Provenance is recorded in
`reviews/inspection-provenance.json`. No review approval or fabrication release
was recorded. Current local viewers: full dresser on port 8849; drawer close-up
on port 8850. Each server holds an immutable snapshot of its bound GLB.

## Evidence boundary

The previous run has nine panels and zero complete drawers. Passing geometry
only confirms those existing panels. New success requires actual drawer bodies,
runner members and installation holes in the saved full tree. Manufacturer CAD
identity does not prove installation, stock fit, screw engagement or motion.
Any unfinished fabrication work stays explicit without removing the drawers from
the intended scope or weakening their required installation.

## Audit log

- 2026-09-12 — User explicitly asked to fix the missing drawers and determine why
  generation stopped. This authorizes implementation and another complete build,
  rather than another report of the same partial model.
- 2026-09-12 — Isolated the repair above the tested instruction correction.
  Initial trace shows selection and capability do not provide a complete route.
  Flagged the existing 156-line KA 4532 spacer planner for the required independent
  responsibility review; hardware/source investigation continues separately.
- 2026-09-13 — The downloaded left and right MOVENTO clips have distinct vertical
  mounting coordinates. A compact front mounting rail needs connector placement
  independent of the automatic quarter points to avoid the real fixing pattern.
  Added optional explicit Cabineo positions while retaining two connectors,
  300 mm spacing, 200 mm end distances and paired cutter bounds. This is a
  construction detail within the authorized repair, not a furniture dimension
  change. The required independent review found the immutable field belongs in
  `specification.py`; layout validation and geometry stay in their existing owners.
  Baseline: 2 focused failures; repaired layout and existing geometry: 16 passed.
- 2026-09-13 — Implemented an explicit four-sided MOVENTO construction using a
  horizontal clip mounting rail. Manufacturer TD-132/1 permits vertical clip
  fixing in this construction. All paired Cabineo cuts and mounting preparation
  share each panel's chosen face. Nominal rear bores were retained despite the
  right-hand source discrepancy; material and screw choices remain candidates.
- 2026-09-13 — Added the shared installer rather than leaving callers to remember
  parent runners, child clips or host drilling. Five option-B fixing axes per
  runner are sourced from TD-132/1 page 13 and independently confirmed in both
  downloads. Four physical support panels resolve the reference front-frame
  apertures. Proposed external furniture dimensions and the original body design
  were retained; no new user-approved measurements or materials are claimed.
- 2026-09-13 — Independent review caught removal of the original broad drawer
  requirement and stale two-hole prose. Both were corrected. A one-shot iterator
  bug in batching was fixed before the final rebuild and tested with real cuts.
  A final perpendicular-axis check rejects tilted hosts even when the fixing row
  still lies on their chosen face. The reviewer checked both actual handed hosts.
- 2026-09-13 — Rebuilt and independently reconciled the full nine-assembly tree.
  All eight drawers and required mounting cuts exist; all 61 chosen faces pass.
  Source geometry remains invalid and completion requirements remain open.
  Verified assembled and exploded visual inspections without manufacturing approval.
- 2026-09-13 — Stopped this turn's older broad test run after 25:58 in unrelated
  door/plinth CAD work. Preserved its 202 passing tests and 58 passing subtests as
  partial evidence only. Final production-code focused checks and the separate
  tilted-host test passed. No push or merge is authorized by this checkpoint.
- 2026-09-13 — Enabled the optional exact-download integration test. Its legacy
  cabinet generator fails the unintended wood-overlap assertion on both this
  branch and untouched `b6732e0` with identical source files. Preserved both logs
  and the failing assertion. Verified all eleven skill entrypoints and links.
