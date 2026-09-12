# Shared construction acceptance

## Scope and current state

WP7 execution is complete on the reviewed local stack through `010d19b`.
Standard configurators and authored layouts use one construction foundation,
one physical tree and common checks. Final independent acceptance review is
complete on `test/shared-construction-final-acceptance`, with no remaining findings.

The initial full integration candidate was `c33b781`. Separate reviewed fixes
addressed native runner frames (`5d6969b`) and geometry approval eligibility
(`010d19b`). All nine full-suite failures pass in the affected rerun. No remaining
application-code finding is known; the five downloaded-Blum tests remain skipped.

## Work package and tasks

- [x] Run independent model-led standard and custom designs from fresh briefs.
- [x] Fix and independently review observed startup, native-placement and approval defects.
- [x] Preserve uncertainty when exact CAD Boolean operations contradict each other.
- [x] Preserve private inputs, vendor CAD, commands, screenshots and comparison evidence.
- [x] Compare saved manufactured parts and exact hardware with their original source.
- [x] Retire duplicate panel algorithms after independent compatibility review.
- [x] Complete full regression and resolve every reported failure with affected reruns.
- [x] Complete current-runtime replays and inventory/sheet reconciliation.
- [x] Record actual matrix outcomes and remaining furniture obligations.
- [x] Close final independent WP7 evidence review using the review skill.

## Regression record

| Run | Result | Exact scope |
| --- | --- | --- |
| Full candidate `c33b781` | 788 passed, 9 failed, 5 skipped; 72 additional subtests passed | All 802 manifest nodes ran exactly once across two disjoint whole-file shards. |
| Native-frame correction | 118 passed | 113 existing drawer/runner cases and five new frame regressions; every original failure has a same-node pass. |
| Geometry approval correction | 43 passed | 29 existing review/server/input cases and 14 new cases, including actual standard closed/open CLI builds. |

Independent collection verifies 821 unique current cases, exactly covered by the
baseline plus scoped reruns. Results above retain their actual candidate and run
boundaries; they are not presented as one fresh all-green final-checkout run.
All five skips require the absent `AIKEA_BLUM_DOWNLOAD_DIR` vendor download.
No skipped check is counted as a pass. The three failed new approval test fixtures
in the first attempt omitted the required third height sample; the corrected
eleven-file rerun passes, with the initial log retained.

Independent exact-manufacturer drawer regeneration agrees with closed/open GLB
bounds within 0.001134 mm for all 13 items. Moving items translate exactly 500 mm,
static items remain fixed, and eight 1 mm hand/inset mutations reject. The
approval patch passes 21 independent live session/startup/control probes and
12 proposal probes. Invalid or stale evidence returns HTTP 409 while inspection
remains available and prior proposed/approved record bytes remain unchanged.

## Observed design flows

| Case | Observed output | Remaining design or validation limits |
| --- | --- | --- |
| Fresh custom stepped entryway | Seven panels, one shared divider, eight Cabineo seams, 16 connectors and 16 inserts. Common builder passes geometry and operation checks; provisional one-sheet nesting. | Seven declared requirements remain unresolved, including exact purchase/support/load evidence. Fabrication gate blocks. |
| Fresh standard cabinet/base with exact Riex door | Fourteen panels, six hinge/plate solids, 28 Cabineos and 28 inserts. Six official CLI stages run without ambient PYTHONPATH; closed/open GLBs stay byte-identical and inputs stay unchanged. | Twelve Boolean-uncertain interfaces and 24 inventory gaps remain. Legacy positioning passes seven checks; shared geometry stays invalid. |
| Actual saved seated wardrobe with leg base | 3940 × 2597 × 465 mm; 104 manufactured pieces including one wood rod; 128 Cabineos plus 128 inserts; 14 Korrekt feet plus 14 plates. | Fourteen foot/plate overlaps, missing material/connection/manufacturing evidence and an oversized niche back remain explicit. Fabrication gate blocks. |

The original fresh-model runs used frozen `b386016` source and are retained with
their startup findings. Final standard/custom/saved CLI replays used `c33b781`
runtime (ending checkout `6923acb` changes documentation only). The drawer fix
has its separate exact-source saved-project replay. The final approval fix has
actual small standard closed/open CLI tests and a saved real-standard boundary
replay; that last check reuses its CAD output without rebuilding the full model.

The fresh standard model deliberately moved its generated adjustable shelf down
64 mm to clear an observed hinge clash while preserving user measurements. Its
final replay changes no recipes, dimensions, materials, hardware or shelf row.
Twenty physical items remain valid solids; twelve interfaces are uncertain,
which does not establish clearance. No contact allowance or source evidence was
invented. The old unapproved proposal is preserved as historical output; current
proposal/result handling refuses it on the saved invalid report.

Saved-wardrobe parity: all 104 manufactured local solids have zero symmetric
difference against independent historical output; all 104 root placement matrices
match exactly, including 67 rotated panels. All 28 hardware items match their
native exact source solids, identity and placement. All 31 original source files
remain unchanged. The failed hardware STEP re-export/re-import comparison stays
recorded as unsuccessful; native-source comparison supplies the stated parity.

Actual stock remains 18/15/9/6.5 mm. The sheet scenario nests 102 of 103 panels
on 20 sheets at 1220 × 2440 mm, 10 mm margins and 8 mm gaps, allowing rotation.
The oversized niche back and missing material IDs keep it incomplete. This does
not regenerate a 16 mm or split-back design or establish a grain-qualified order.

## Evidence and visual inspection

Canonical private archive: `local-evidence/shared-construction-20260912/` in this
worktree. `final-evidence-index.json` hashes the complete retained artifact set;
the older 858-file `archive-manifest.json` remains its historical subset. CAD,
user projects and private review artifacts are ignored and are not added to Git.

| Evidence group | Contents |
| --- | --- |
| `standard-forward-original`, `custom-forward-original` | Raw fresh-model trials, original failures and source snapshots. |
| `standard-final`, `custom-final`, `saved-final` | Final CLI commands, source hashes, exit codes, GLBs, inventories, sheet/gate reports and screenshots. |
| `saved-wardrobe`, `independent-cad`, `independent-root-placements` | Original source provenance and independent manufactured/hardware/placement parity. |
| `component-proofs` | Retained exact door-host, whole-front, Korrekt and lighting added/removed proof. |
| `independent-runner-frames`, `saved-manufacturer-drawer` | Native source diagnosis, saved real-CAD drawer regeneration and negative controls. |
| `regression`, `runner-regression`, `geometry-review-final`, `independent-regression-coverage` | Baseline, affected runs and exact node/hash reconciliation. |
| `independent-review-eligibility` | Old/new source snapshots, actual HTTP probes and preserved saved-standard boundary output. |

Inspected screenshots: `custom-final/visual-full.png`,
`saved-final/visual-overall.png`, `saved-final/visual-bottom-full.png`,
`standard-final/screenshots/common-closed.png` and
`standard-final/screenshots/complete-open.png`. Their browser records report
HTTP/model 200 and no page errors. Corresponding GLBs remain in the same project
groups. Component proof retains closer connection and moving-state artifacts.

The viewer applies a generic wood appearance to prototype MDF/white parts; it is
not finish authority. The corrected standard open-door bounds differ from actual
GLB vertices by at most 0.00001914 mm; three plate overlays retain pre-existing
conservative bounds up to 0.494635 mm outside mesh bounds. Pose/source comparisons
do not establish full swept clearance, strength or physical mating. The two exact
standard closed CAD checks took approximately 13 minutes under concurrent suite
load; these are observed contended timings, not an isolated benchmark.

## Audit log

1. Patrick authorized implementation and review after each work package. This
   scope remains construction tooling; manufacturing, publication and hosted
   storage decisions remain separate.
2. Preserve raw fresh-model failures beside reviewed corrections and replays.
   No historical result is promoted to a fresh final-runtime result.
3. Complete regression found nine native runner proof/producer failures. Their
   corrected frames, exact manufacturer-source replay and affected suite are
   independently reviewed; tolerances and purchase counts were not relaxed.
4. Standard replay exposed an approval proposal despite invalid shared geometry.
   The separately reviewed correction carries current status, blocks stale live
   decisions and preserves historical records without a second readiness engine.
5. Independent coverage audit verifies all current node IDs and all failure-to-pass
   mappings. Final acceptance-document review is the remaining WP7 closure task.

6. Final independent review verified the complete archive, all current Python
   hashes, baseline/affected coverage, preserved original inputs and the ten-case
   matrix. Five documented screenshots and their HTTP/model records were
   inspected. Review and supporting evidence are retained under
   `final-acceptance-review/`. All eleven local skills and links pass package
   verification. Default pytest discovery retains exactly the same 821 cases and
   excludes archived test copies. Final closure changes documentation and test
   discovery configuration; construction and test Python code are unchanged.
