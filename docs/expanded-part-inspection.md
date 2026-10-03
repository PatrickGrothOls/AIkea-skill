# Expanded exploded inspection

## Scope

The user wants more separation than the current 100% limit and a way to inspect
every physical part individually. Preserve the existing mounting hierarchy:
runner supports carry their runners, drawer panels carry their declared fittings,
and only a selected deeper inspection separates those fittings. Reuse the current
99-piece GLB; no furniture geometry, holes or source CAD are changed.

Branch `feat/expanded-part-inspection` is stacked on `8ca59fb`. Refreshed
`origin/main`, verified it is an ancestor and created an isolated worktree.

## Current state

Implemented and verified locally. Separation extends to 300%; above 100%,
aligned drawer groups spread apart while retaining their mounted fittings.
Every physical part is available through the dropdown or by picking it and
choosing Inspect selected part. The final packaged viewer was checked on the
unchanged 99-piece dresser, including panel isolation, rotation and full reset.

## Work packages

### WP1 — More space and individual focus

- [x] Extend separation to 300%, keeping the existing 0–100% behavior intact.
- [x] Above 100%, spread group centres to separate aligned drawer stacks.
- [x] Make every visible physical part an inspection target.
- [x] Add an Inspect selected part action using explicit inspection identity.
- [x] Keep attached hardware, multi-surface parts, framing and reset correct.
- [x] Verify behavior and review the focused code changes.

### WP2 — Present the unchanged dresser

- [x] Update the review skill and rebuild its bundled viewer.
- [x] Test higher separation and actual part isolation against the existing GLB.
- [x] Check the browser flow, rotation/zoom and restore with actual screenshots.
- [x] Finish the branch record and commit the reviewed change locally.

## Verification and evidence

- All 45 viewer tests passed. Added meaningful coverage for aligned stacks,
  physical leaf selection, 300% reset, multi-surface ownership and path identity.
- The independent review reproduced a newly exposed trailing-underscore path
  collision. Encoding every underscore within a segment fixed it; regression
  cases cover leading, trailing and repeated underscores plus literal percent
  text. The reviewer independently rechecked the fix and hidden/multi-primitive
  focus; no findings remain. Report: `local-evidence/expanded-inspection-review.md`.
- Skill-package validation passed for 11 skills. Vite rebuilt the shipped assets
  after the final changes. All changed authored code files remain below 150 lines.
- The real GLB passes 99 individual focus checks and exact matrix reset. All 32
  explicit hardware attachments remain intact at 100%, 200% and 300%. Adjacent
  drawer-front centre spacing increases from 154.5 to 309 to 463.5 mm, respectively.
  All 99 focus checks were rerun after the path-encoding correction.
- The existing GLB is byte-identical before and after inspection; SHA-256:
  `33ed761edebae32923c67b4d8c0e0839952035c8e0687a5c587893105ba19276`.
  Measurement record: `local-evidence/expanded-inspection-proof.json`.
- Browser validation: 200% full view; pick the actual right-end panel; Inspect
  selected part shows one piece; rotate it; Restore assembly shows all 99 at 0%;
  raise separation to 300%. The final bundle also renders the singular piece
  label correctly. Default browser sizing was used; no viewport override.
- Actual screenshots: `local-evidence/dresser-expanded-200.png` and
  `local-evidence/individual-panel.png`. The live viewer remains available for
  the user. These are inspection results, not new manufacturing qualification.

## Audit log

- 2026-09-13 — User requested greater explosion and inspection of individual
  parts. Verified the current viewer was already at 100%; a larger limit alone
  would not separate drawers whose current group offsets are identical.
- 2026-09-13 — Keep the previous range unchanged, add centre-based spreading
  only beyond it, and route individual focus through the existing structured
  hierarchy. These implement the requested inspection behavior without changing
  furniture construction or the previously agreed attachment rule.
- 2026-09-13 — The independent review found a path-delimiter ambiguity newly
  reachable through leaf selection. Escaped segment underscores consistently,
  added regressions and rechecked actual-model focus before completing WP1.
- 2026-09-13 — Completed live picking, individual panel inspection, rotation,
  higher separation and full restoration. Updated the skill, captured images,
  reviewed the final diff and saved this small follow-up locally.
