# Drawer host proof: scope review

Reviewed 2026-09-12 on `feat/drawer-host-proof`, baseline `e72d168`.
Scope: the inherited installed-runner checker (156 lines), installed-fixing
checker (164 lines), and their proof/evidence collaborators. This is a
responsibility review, not validation of the forthcoming implementation.
No production code was edited and no tests were run.

**Recommendation: retain the two existing checker boundaries. No separate
engine or file extraction is required merely because they exceed 150 lines.**

| Concern | Current location | Assessment |
| --- | --- | --- |
| Bind the wooden drawer to the installed fixed/moving runner pair | `hettich_ka_4532_installed_runner_checker.py:30-137` | One coherent physical relationship: drawer front/bottom, runner axis height, lateral allowance and relative articulation must agree before its datum result is usable. |
| Resolve support identities and datums | same file, lines 36-56, 99-101 and 139-141 | Replace standard-name and bounding-box-front assumptions with the current `DrawerHost`. A small private host-datum agreement helper is sensible if the new checks need grouping; a second product checker is not. |
| Verify rail-to-spacer-to-support fixing paths | `hettich_ka_4532_spacer_installed_fixing_checker.py:27-125` | Already consumes verified runner datums and owns a different, exact-product relationship. Keep it separate from runner articulation. |
| Compare fixing points and directions | same file, lines 127-160 | These predicates encode that fixing relationship and its tolerances. They belong beside the fixing check, not in a generic geometry utility. `SourceNormalizedFrame` already owns shared coordinate transformation. |

Minimal structure for this slice:

- Load the current declaration through the existing `DrawerHostLoader` at the
  proof-generation boundary; pass it through the proof checker, fixing-evidence
  checker and installed checkers. Do not rebuild a host from saved proof data.
- Keep reservation participant checks in `HettichKa4532SpacerProofChecker`;
  compare them with the host's actual support IDs rather than cabinet names.
- Keep rendered-part membership and agreement with current support datums in
  the installed-runner check. A declared bay front may be inset from panel
  fronts, so it must not be replaced by their bounding-box minimum.
- Retain internal drawer-part identities, exact-source comparisons, motion,
  collision checks and the unresolved machining blocker in their current
  collaborators. Renaming host supports is not a reason to bypass any of them.

The proof generator owns file/runtime orchestration, the proof checker combines
independent evidence, and the fixing-evidence checker compares the saved schema
with freshly checked installation. These responsibilities should remain
separate. Extract a host-to-rendered-support agreement collaborator only if a
second independent consumer needs that same check; this slice does not yet
establish that need.
