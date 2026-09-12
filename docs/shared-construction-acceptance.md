# Shared construction acceptance

## Scope and current state

Branch `test/shared-construction-acceptance` closes WP7 of the
[shared foundation plan](shared-construction-foundation.md). It verifies the
complete local design path and preserves the distinction between functioning
construction tools and unresolved furniture/fabrication decisions.

Candidate `c33b78126e9ccff0959c894d438630fb39928eba` is under complete regression:
802 collected cases, partitioned by whole test file into two 401-case processes.
The run has exposed drawer source-frame failures and is not yet green. Current
runtime closure of the standard and saved projects is also in progress.

## Work package and tasks

- [x] Run independent model-led standard and custom designs from fresh briefs.
- [x] Fix and independently review the observed startup and native-placement defects.
- [x] Retain uncertainty when exact CAD Boolean operations contradict each other.
- [x] Preserve private input, CAD, command, screenshot and comparison evidence.
- [x] Compare all saved manufactured pieces and exact hardware with their source.
- [x] Remove duplicate production panel algorithms after independent parity review.
- [ ] Complete the full regression and resolve all relevant failures.
- [ ] Complete final current-runtime project replays and inventory/sheet reconciliation.
- [ ] Record the completed acceptance matrix and residual construction gaps.
- [ ] Apply the review skill to final WP7 evidence and resolve its findings.

## Evidence location and provenance

Private files are retained under the ignored directory
`local-evidence/shared-construction-20260912/`. `archive-manifest.json` records
858 archived files and their hashes. Vendor CAD and user projects are not added
to Git. Commands use the active direnv environment; current-runtime replays
explicitly remove `PYTHONPATH` and retain process output and exit codes.

The independent fresh-model trials initially used a source snapshot of `b386016`.
Those original findings and artifacts remain unmodified under
`standard-forward-original/` and `custom-forward-original/`. They are behavioral
evaluations, not claims that final candidate fixes existed in that snapshot.
Separate current-runtime replays close each identified implementation defect.

## Observed design flows

| Case | Observed output | Explicit limits |
| --- | --- | --- |
| Fresh custom stepped entryway | Seven panels, one shared divider, eight Cabineo seams, 16 connector positions and 16 inserts; common builder, no new furniture-purpose engine. Final candidate build passes geometry and operation checks; sheet scenario fits one sheet. | Seven declared unresolved construction requirements; exact connector/supplier/load evidence missing; fabrication gate blocked. |
| Fresh standard cabinet and base with selected Riex door | Fourteen panels and six exact hinge/plate solids; 28 Cabineos and 28 inserts. Closed/open visual evidence exists. Model used shared tools and moved a generated adjustable shelf down 64 mm to clear a detected hinge collision, preserving user measurements. | Hardware interface evidence remains unresolved. Final candidate replay is in progress; original snapshot needed now-fixed startup workarounds. |
| Actual saved seated wardrobe with proposed leg base | 3940 × 2597 × 465 mm; 104 manufactured pieces, including one wood hanging rod; 128 Cabineos and 128 inserts; 14 exact Korrekt feet and 14 plates. | Actual thicknesses remain 18/15/9/6.5 mm. No regenerated 16 mm or split-back design is implied. Materials, some connections and manufacturing evidence remain incomplete. |

Saved-wardrobe comparison: all 104 manufactured local solids have zero symmetric
difference against independent historical output. All 104 accumulated placement
matrices match exactly, including 67 rotated panels. All 28 purchased source
solids match by native CAD comparison, immutable source hashes and exact identity.
All 31 original source files remain unchanged.

The raw hardware STEP re-export/re-import comparison failed despite equal bounds
and volumes. It is retained as unsuccessful evidence. Native exact-source CAD
comparison and placement/hash checks establish the separately stated hardware
parity; the failed round-trip test is not relabeled as passing.

The saved sheet scenario places 102 of 103 panels on 20 sheets at 1220 × 2440 mm
with 10 mm margins and 8 mm gaps, allowing rotation. One oversized niche back and
missing material identities remain unresolved. This is an incomplete nesting
scenario, not a complete purchase quantity or a grain-qualified material quote.

## Validation boundaries

The original fresh standard and custom viewers returned HTTP 200 for the page
and GLB with no browser page errors; actual screenshots were inspected. Standard
closed/open, custom overall, and saved overall/bottom views are retained. The
viewer currently applies a generic wood appearance to prototype MDF/white parts;
written material and finish choices remain authoritative.

Independent native-placement review confirms the real standard open-door report
matches decoded GLB positions within 0.00001914 mm and preserves all 20 mesh vertex
arrays. Independent uncertainty review covers six actual source-pair/frame cases,
14 analytic controls, ordinary bounded allowance behavior and five scalar boundary
cases. These numerical checks do not certify strength or physical mating fit.

The separate furniture gates remain blocked by applicable unresolved source,
attachment, load, stability, machining, manufacturing or approval obligations.
No new load rating, screw specification, price or customer approval is invented.

## Audit log

1. Patrick authorized implementation with the review skill after every work
   package. WP7 evaluates the existing construction scope and does not broaden it
   into publication, hosted storage, supplier communication or manufacturing.
2. The fresh-model evaluations were allowed to surface actual instruction and
   implementation failures; each raw run remains available alongside subsequent
   reviewed corrections and final runtime replays.
3. The full candidate regression exposed a drawer proof-frame inconsistency.
   Completion stays pending until the fix and its evidence receive independent
   review. Exact source frames must match actual installed geometry.
