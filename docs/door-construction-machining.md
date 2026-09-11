# Shared door and hinge machining

## Scope and current state

WP5c operation slice on `feat/door-construction-machining`, based on `87bada6`.
Implementation, focused tests and review pass in `shared-components`. The previous
slice's full suite found two stale fixtures; their separate repair is recorded in
`shared-construction-validation`. No production relaxation is needed.

The existing slab-door recipe now emits shared surface-hole operations for the
cup and mounting plate. Generated features retain cuts, requirements and exact
purchases. The existing preview helper reuses the same cup pattern. Explicit
custom door-host inputs and supported front variants
remain the next slice; this is not yet a universal door configurator.

## Work package and tasks

- [x] Reuse the NC70 cup pattern from `c08f1b0`; retain both hands and dimensions.
- [x] Save explicit cup/plate operations and exact reuse of existing grid holes.
- [x] Apply generated features through the common panel machining boundary.
- [x] Retain exact hinge/plate purchases and their explicit evidence scope.
- [x] Verify geometric parity, missing host holes, ownership, regeneration and
  edited-file protection on the official build path.
- [x] Run the review skill and fix/recheck findings.

## Audit log

1. Reuse the existing source-derived cup pattern; no new hole geometry engine.
2. The standard mounting recipe uses the existing 5 by 13 mm System 32 interface,
   which exceeds the selected plate's 12 mm required hole depth. Reuse is declared
   only for matching whole holes; absent holes are explicit new cuts.
3. The retained 2.5 by 10 mm cup pilot choice is made an unresolved screw/material
   requirement. Migrating its geometry does not promote it to verified authority.
4. Generated construction includes exact purchased hardware in feature evidence
   scope. The shared complete builder is written under ordinary file protections.

5. Primary review found that replanning from an already composed door can treat
   its old cuts as reusable host geometry. The review command now excludes that
   exact feature before rebuilding. The generic loader keeps the same base and
   every unrelated feature; it rejects exclusion from an incompatible authored
   builder instead of discarding custom work.

## Validation

- Eleven focused machining, alignment, generation and complete-review tests passed.
- After strengthening the regeneration assertion to reload the rebuilt result,
  all four machining cases passed again, including both door hands.
- Independent review compared both hands with the former raw-cylinder geometry:
  symmetric difference was zero. Shallower existing holes were rejected for reuse.
- Independent exclusion probes retained an unrelated feature's cuts and purchase,
  and refused an incompatible authored builder without running or overwriting it.
- The primary review's regeneration issue is fixed and independently rechecked.
  No open findings remain. The [scope report](reviews/door-machining-scope.md)
  retains the generator's existing orchestration responsibility.
- All nine skill packages and links validated; `git diff --check` passed.

These are local software checks; custom door-host placement and full opening
proof remain separate work. Existing pilot choices retain their unresolved status.
