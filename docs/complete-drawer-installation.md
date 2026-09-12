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

Investigation active. The skill now requires complete installations, while the
default KA 4532 route is inseparable from an unfinished spacer installation and
MOVENTO lacks mounting preparation. The existing KA 5332 route has explicit
drilling but remains client-selection-only and recommends narrower drawers.
Source CAD is already available. Exact source installation data, actual one-face
drawer joinery and generator capability must be reconciled before choosing the
smallest repair. The first generic repair allows authored connector positions
without weakening minimum count or spacing. Its focused regression failed on
the baseline and now passes with the existing paired-geometry tests (16 passed).
One complete MOVENTO drawer is still being developed; no repaired full dresser
has been generated yet.

## Work packages

### WP1 — Reproduce and choose the repair

- [x] Verify checkout, upstream ancestry, baseline run and unchanged source inputs.
- [ ] Trace product selection, box construction, mounting cuts and declared gaps.
- [ ] Confirm one compatible runner/fastener installation from primary sources.
- [ ] Reproduce the missing installation in a focused regression case.
- [ ] Review responsibility boundaries and any existing file over 150 lines.

### WP2 — Complete the reusable installation

- [ ] Implement the missing sourced installation through existing shared operations.
- [ ] Preserve explicit product choices and make spacers depend on actual clearance.
- [ ] Join the drawer panels without opposing-face machining conflicts.
- [ ] Include physical hardware ownership, matching mounting cuts and requirements.
- [ ] Run meaningful regressions and review using the applicable skills.
- [ ] Commit each coherent repaired slice; split distinct concerns if needed.

### WP3 — Finish and verify the dresser

- [ ] Build one complete drawer installation on the real host panels.
- [ ] Repeat the verified installation into all eight drawer positions.
- [ ] Run complete geometry, entry-face, installed motion and physical inventory checks.
- [ ] Reconcile Cabineo product compatibility and remaining fabrication limits.
- [ ] Show current assembled, open and exploded views with mobile screenshots.
- [ ] Review the actual result and update the skill instructions and branch state.

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
