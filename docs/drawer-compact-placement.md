# Compact drawer placement

## Scope

Fix the drawer stack first, preserving required operating clearance, purchased
runner geometry, real fixing holes and the shared shelf grid. Base side returns
remain on their separate branch.

## Current state

Implemented a compact collection planner and executable repair command. The
first drawer keeps its exact floor clearance; upper runners reuse suitable grid
rows and box heights fill the intervening space. Conflicts fail rather than move
individual drawers. Existing saved snapped layouts keep their prior behavior.
Legacy wardrobe review now checks actual compact geometry before export, even
when travel evidence is missing. This does not waive fabrication qualification.

The original Claude project has been downloaded and regenerated with exact
checksum-verified 9057405 CAD. Its old gaps were 77, 20, 24 and 3.5 mm. The revised
plan has 3 mm gaps and heights 167, 253 and 182.5 mm under the existing shelf.
Forty focused tests passed, including built solids and real cut probes (with a
hardware test double in the integration fixture). Original-project export passed
the compact geometry check and the open viewer visibly shows the corrected stack.
Skill/package and whitespace validation passed. Full drawer joinery and travel
qualification remain outstanding; this is a placement fix, not fabrication approval.

## Work packages

### WP1: Reproduce and correct placement

- [x] Inspect current placement, grid, machining and review paths.
- [x] Add a compact stack planning route with explicit operating gaps.
- [x] Preserve planned positions when placing runners and their fixing holes.
- [x] Preserve saved legacy placement on reload.
- [x] Verify actual generated drawer solids and fixing positions.

### WP2: Enforce and deliver

- [x] Check vertical gaps independently of unavailable travel evidence.
- [x] Prevent legacy full-wardrobe review from reporting a bad stack as valid.
- [x] Update the skill's executable workflow.
- [x] Run focused regressions and package checks; review the diff.
- [x] Commit the coherent placement fix.
- [x] Deliver a corrected visual review, with remaining fabrication limits clear.

## Audit log

- 2026-09-21: User requested fixing drawers before base work. This authorizes
  correcting placement and enforcing the existing compact-stack policy.
- 2026-09-21: Shared shelf rows start at 100 mm; a runner centered 23 mm above
  its drawer bottom cannot put a drawer 3 mm above a typical cabinet floor if
  forced onto those rows. Shelf support rows remain unchanged. Runner drilling
  must use the resolved drawer placement, as the installation contract already
  distinguishes runner axes from shelf-pin rows. Preserve collision checks.
- 2026-09-21: Requested the AGENTS-mandated responsibility review of existing
  implementation files over 150 lines. No unrelated refactor is planned.
- 2026-09-21: Exact fractional upper heights initially produced a partial
  intersection with existing shelf bores. Retained the machining check and used
  compatible upper rows, deriving box heights between them instead of accepting
  clipped holes. This preserves the user's compact-stack requirement.
- 2026-09-21: Independent review found a greedy row-allocation edge case and a
  legacy-load test gap. Reserved rows for remaining drawers and added both
  regressions. The single-drawer planner is 152 lines and remains cohesive
  orchestration; the reviewer advised against extracting a redundant wrapper.
- 2026-09-21: Kept the source project, vendor CAD and rendered evidence outside
  the branch under ignored local-evidence/drawer-compact-placement. No changes to
  source stock, base design, hinges or licensing were made in this placement fix.
- 2026-09-21: Exported the corrected original wardrobe with doors removed and
  visually verified the stack in the browser. All four intended vertical gaps
  are 3 mm. The preview does not carry a full fabrication approval.
