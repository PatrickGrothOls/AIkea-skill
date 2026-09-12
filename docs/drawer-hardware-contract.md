# Complete drawer installation skill correction

## Scope

Make every drawer workflow include compatible runners, actual mounting holes and
spacers where door/hinge intrusion requires them. Apply this to custom compositions
and optional configurators, including doors added after drawers. This is a skill
workflow correction; the existing generic construction and fabrication gates stay
unchanged. Do not add furniture-specific inference to the shared builder.

Branch: `fix/drawer-hardware-contract`, based on `f3f99d2` from
`feat/assembly-exploded-view`. `origin/main` was fetched and verified as an ancestor
before creating this isolated worktree. The original checkout is preserved.

## Current state

The previous branch updated only the plan after the reference dresser exposed
missing runners. This branch updates the actual reusable skill and routes.
The reference dresser still has eight unresolved runner installations; its
historical geometry and evidence are not rewritten by this correction.

The actual skill correction, metadata/link validation, responsibility review,
focused regression checks and two independent forward tests are complete.
The requested fresh full build attempt has finished using the unchanged
`d4e2c70` skill package, reference image and already downloaded raw hardware CAD.
It had no prior dresser geometry, sizing or evaluation findings. **The full
eight-drawer build did not complete:** it generated a nine-panel carcass and
stopped drawer generation for incomplete runner installation support. It also
identified a manufacturer/profile discrepancy for the Cabineo brass inserts.
The carcass passes geometry and declared-face checks; inventory is draft and
fabrication is blocked. This is a partial build, not an end-to-end success.
Installed global aliases still point to the original checkout;
this branch has not been pushed, merged or installed over those aliases.

## Work packages

### WP1 — Complete drawer workflow

- [x] Put the installation contract in the drawer skill's own reference.
- [x] Route custom design, main intake and component use through that contract.
- [x] Require hinge-clearance spacers and revalidation after door/hinge changes.
- [x] Remove the box-only prototype escape; disclose existing generator fixing gaps.
- [x] Require physical hardware, mounting cuts and evidence in complete-tree review.
- [x] Review skill responsibility boundaries and contradictory instructions.

### WP2 — Verify the correction

- [x] Validate skill metadata and local links.
- [x] Run focused existing hardware, drilling and fabrication regression checks.
- [x] Run independent fresh-agent behavior tests from the reusable skill package.
- [x] Record actual results and limits; do not equate instruction tests with CAD proof.
- [x] Review the final diff and commit one coherent local checkpoint.

### WP3 — Fresh complete dresser run

- [x] Start an independent agent with a clean project and the exact updated skill.
- [x] Supply the raw image and unchanged local vendor downloads, without choosing
  hardware or importing the old dresser's dimensions for the agent.
- [x] Let the agent attempt construction, hardware sourcing/installation and review.
- [x] Independently inspect actual output: drawer hardware, mounting operations,
  one-face compatibility, inventory, movement and fabrication readiness.
- [x] Show the actual closed/exploded model and screenshot when available, or
  report the precise evidence-backed blocker without reusing the old model.
- [x] Preserve results and record whether the full build completed.

These checkmarks record completion of the evaluation, not completion of the
furniture. Eight drawer installations and their mounting/movement proof remain
unresolved. No runtime profile or generator was changed during this run.

## Review and validation

WP1 responsibility review used `review-code-boundaries` and the skill-creator
workflow. PASS: drawer installation policy has one owner in
`aikea-build-drawers/references/complete-drawer-installation.md`; the generic design
and review routes link to it. The door stage owns invalidating fit when a hinge
changes. No shared runtime file learns drawer classification or furniture purpose.
The permissive general prototype rule explicitly defers to the drawer contract,
and existing generators' incomplete fixing capabilities remain disclosed.

No production code changed. Affected instruction line counts (before → after):
main skill 209 → 210; drawer skill 180 → 195; drawer recipe reference 44 → 52;
new installation reference 0 → 91; design skill 82 → 89; component map 27 → 27;
manufacturing process 60 → 64; door skill 109 → 115; review skill 195 → 202.
The longer entrypoints retain routing/sequence ownership; detailed new policy
stays in the drawer-owned reference instead of expanding the common builder.

- `scripts/verify_skill_package.py`: 11 local skills and discovery links passed.
- Skill-creator `quick_validate.py`: all five changed skill entrypoints passed.
- Every relative Markdown link in the changed instructions and references passed
  (65 links), and `git diff --check` passed.
- Focused hardware ownership, host drilling, hardware-set verification, spacer
  reservations and fabrication evidence checks: **32 passed, 1 skipped**. The
  skip requires `AIKEA_BLUM_DOWNLOAD_DIR` for a real-source CAD integration test;
  fixture-based tests do not replace that evidence. CadQuery emitted nine existing
  export deprecation warnings.
- Rebuilt and evaluated a separate copy of the historical dresser with this
  branch's fabrication command. Exit **2**, status **blocked**, including all
  eight `runner_installation` obligations. The original project was untouched.

The forward-test package contains only reusable skill directories and the current
runtime environment. Agents receive the raw brief and, for the dresser, the user
image; no previous project, plan, findings or intended answers. Their tests are
behavior evidence, not a new verified hardware installation.

| Independent case | Observed result | Evidence boundary |
| --- | --- | --- |
| Fresh image-led 1500 × 500 × 950 mm dresser, eight drawers, model/cutting-file request | Read the drawer route, rejected the registered 500 mm option's depth, recorded eight intended runner pairs and missing exact 450 mm CAD/fixing data. Saved a measured proposal and exact sourcing handoff. No drawer parts, GLB or CNC files generated. | PASS for source-before-generation behavior. Proposed hardware is not a verified fit or approved purchase; no complete drawer installation was built. |
| Two 568 mm openings: left obstructed by 22 mm per side at usable door angle; right open | Included four runner sets and four 25 mm spacers on the left only. Recalculated nominal outside widths to 492.6 mm left / 542.6 mm right, kept load, mounting, material and one-face joinery unresolved, and asked for missing drawer-zone heights. | PASS for conditional spacer planning and preserved clear-width measurements. This was a layout request, not a CAD or collision proof. |

WP2 review: the actual artifacts support the behavior results above. The fresh
agents were not given the failure history or expected answers. They used the
copied skill instructions; the existing dresser gate and focused tests provide
separate runtime evidence. No claim of a universal deterministic drawer detector
or automatic completion of unsupported hardware is made.

Local evidence is retained under `local-evidence/drawer-installation-contract/`.
It is intentionally excluded from the skill and commit: raw forward-session
outputs, root validation summary, instruction hashes and the historical gate
report are development evidence, not reusable furniture construction.

### WP3 — Actual fresh build result

WP3 review used `aikea-review-unit`, including the shared construction-position,
one-face process, exploded-inspection and fabrication-readiness instructions.
The partial model is an inspection result only; no visual/fabrication approval
was requested or recorded for the incomplete dresser.

The isolated agent proposed a 1600 × 560 mm body, 1640 × 590 mm top and 900 mm
overall height. These are unapproved proposals derived from the reference image,
not measurements. Its real output contains nine carcass panels, zero drawer
installations and zero modeled purchased hardware components. The body follows
the integrated-leg/two-bay appearance, but cannot demonstrate the reference's
eight fronts, pulls, drawer motion or complete assembly appearance.

| Actual command | Exit | Result and limit |
| --- | --- | --- |
| Shared assembly build | 0 | Nine valid parts, no overlaps, uncertain intersections or envelope errors; construction explicitly incomplete. |
| Panel setup audit | 0 | Nine parts have compatible declared entry faces; missing runner cuts are outside that evidence. |
| Physical item count | 2 | Draft: nine panels, 57 paired Cabineo cut occurrences and 57 inferred brass inserts; exact Cabineo purchase SKU missing. Counts do not establish product compatibility. |
| Fabrication readiness | 2 | Blocked by unresolved construction, missing manufacturing outputs and absent current assembly approval. |
| Provisional sheet plan | 0 | Four sheets for the partial body only, not a whole-dresser material quantity. |

The actual source CAD hashes and native dimensions matched the supplied Hettich
manifests. That verifies source identity, not installation fit. The registered
KA 4532/spacer construction still lacks complete fastener/pilot and drawer-side
machining implementation. The MOVENTO route also lacks a qualified complete
locking/preparation arrangement under the one-face constraint. The drawer skill's
instruction, "Pause drawer generation until it is resolved," prevented either
unfinished recipe from producing boxes as if they were complete installations.
This dresser has no hinged doors; spacers are not universally required by it.

Independent manufacturer review confirmed that Lamello's
[drilling-system brochure, pages 32–33](https://lamello.com/fileadmin/Downloads/Broschueren/Bohr-System/PDF/Bohr-System_Broschuere_EN.pdf)
specifies an 8 mm diameter, 13.5 mm deep preparation for its M6 × 12.3 mm insert.
The saved shared receiver is 9.1 × 12.5 mm; the illustrated on-surface pocket and
rear-center dimensions also differ. Exact selected product/variant compatibility
must be resolved before changing the shared profile or calling the holes suitable.
The existing custom cutter and raw source files were preserved. The counter's
default brass SKU is not evidence of an independently selected compatible product.
The Hettich installation sheet additionally recommends a maximum 550 mm drawer
width; suitability for the proposed wider bays remains unqualified.

Parent review reconciled every GLB mesh with inventory and all nine chosen faces
with every declared operation. The final build/audit share construction hash
`a2c8f522f1aeb09f4f81185de12464b225127e6e0e87db807778505ff5fcd84a`.
The new GLB hash is
`385deb3eddb18254d4d8fa965c0325a3f1b56272a941f667494d6fa451850171`.
All 497 supplied skill files stayed unchanged, with no additional non-cache files.
This independent review inspected saved output and source evidence; it did not
independently regenerate the CAD or qualify the missing hardware installation.

The live viewer rendered the nine-piece body in its assembled and 65% exploded
poses; Restore assembly returned to 0%. No console errors appeared, only the
existing Three.js clock deprecation warning. Both screenshots are retained.
Viewer: `http://127.0.0.1:8847/` (local process; requires restart after shutdown).
Full local inputs, authored project, command reports, manufacturer evidence,
screenshots and parent review are retained under
`local-evidence/dresser-full-rerun/`. Vendor files remain ignored and local.

## Audit log

- 2026-09-12 — User explicitly required runners and mounting holes for every drawer,
  plus spacers wherever cabinet doors/hinges obstruct them. This confirms the
  policy correction and its physical reason: CNC files must contain installation
  machining, not merely drawer-box joinery.
- 2026-09-12 — Inspection found a custom box recipe could be delivered with
  unresolved runner obligations under the general prototype allowance. The drawer
  skill now owns a complete-installation contract; other stages route to it.
  Missing source/fixing data stops drawer generation and triggers sourcing rather
  than an incomplete drawer deliverable. Registered profile limitations stay explicit.
- 2026-09-12 — WP1 review and focused regression checks passed. The historical
  dresser still fails fabrication readiness for its missing installations; this
  correction does not retroactively add hardware to existing geometry. Started
  two independent fresh-agent sessions: image-led custom dresser construction and
  a layout containing both hinged and unobstructed drawer bays.
- 2026-09-12 — Both fresh behavior cases passed their bounded scope. The dresser
  session stopped for exact source/installation input before creating drawers;
  the hinged-bay session included the necessary spacers only on the obstructed
  side and retained the missing physical checks. The changed policy was tested
  without modifying source skills during either session.
- 2026-09-12 — Final review passed; all nine changed instruction/reference files
  match the exact fresh-test package hashes. Retained local evidence separately
  and saved the correction as one local skill checkpoint. No push, merge, global
  skill-alias change or update of the existing dresser geometry is included.
- 2026-09-12 — User requested a new run. Started `dresser_full_rerun` without
  inherited conversation context in `/private/tmp/aikea-dresser-new-run-uztpj9z9`.
  Inputs are the unchanged skill at `d4e2c70`, original dresser image, and vendor
  downloads for Hettich/Blum/Cabineo with hashes and original notices. The user
  supplied no measured dresser envelope; the agent must make explicit proposals
  rather than inherit the previous prototype's 1500 × 500 × 950 mm dimensions.
  This run targets an actual complete assembly and review, beyond the earlier
  bounded behavior tests. Unknown source data or capability remains a real gap.
- 2026-09-12 — Relayed the user's existing authorization for separate aesthetic
  router work/sanding when the fresh agent mistakenly marked that permission
  missing. This corrected the brief, without importing previous design geometry
  or coaching a hardware solution. The corresponding requirement changed the
  construction hash, so the agent regenerated its final build and reports.
- 2026-09-12 — Full attempt ended with a partial nine-panel carcass. The actual
  runner/fixing implementation and exact Cabineo/insert compatibility remain
  unresolved; no missing hardware was hidden behind a decorative proxy. Parent
  review verified the saved mesh inventory, all chosen faces, source/package
  integrity and closed/exploded visual delivery. WP3 evaluation is complete;
  complete-dresser and fabrication outcomes are failed/blocked, respectively.
  Preserved evidence locally and recorded this result without changing the
  runtime, installed skill aliases, old dresser or remote branches.
