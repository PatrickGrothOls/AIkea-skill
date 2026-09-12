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
