# Capture the Vilja lessons before a fresh branch run

## Scope and authorization

Patrick requested capturing the reusable lessons, then corrected the release
instruction: rebase this branch onto current main and test a fresh agent here;
do not merge or publish. Keep the existing project and viewer for comparison.
Capture procedures and configurable calculations, not Vilja dimensions as defaults.

## Current state

- [x] Fetched origin and rebased `codex/vilja-fresh-restart` on `origin/main`.
  Main is `52facbf`; rebase was already up to date. No merge or push.
- [x] Audited shared instructions/code against project fixes. Key gaps: GRASS
  public retrieval recipe, warm lighting command defaults, legacy assumed door
  mass, shelf-relative pin columns, installed-Blender reuse and project-only
  collision fixes. Installed skills still point to root main; fresh agent must
  load this branch's skill directory explicitly.
- [x] Capture and validate the reusable gaps below.
- [x] Independent review passed after both findings were fixed; six coherent code/documentation checkpoints committed.
- [x] Start a fresh agent using only this branch's skills and a clean design brief.
- [ ] Inspect that agent's outputs; do not infer success from dispatch.

## Work packages

### WP1: hardware recovery and qualification

- [x] Add exact GRASS hinge/plate public STEP retrieval, identity checks and
  discoverable integration guide; retain CAD outside Git.
- [x] Capture public catalogue/archive alternatives before a login handoff,
  truthful source-format conversion and resumption through installation.
- [x] Replace the legacy implicit plywood rectangle mass with explicit material,
  outline and finish inputs; unknown finished mass remains unknown.
- [x] Preserve user-owned width/layout decisions and open-motion limitations.

### WP2: reliable construction and lighting defaults

- [x] Default new lighting commands to neutral white while preserving existing choices.
- [x] Keep shelf pins on cabinet-owned grid columns despite front/rear shelf gaps.
- [x] Provide positive shelf fit clearances and test the resulting grid alignment.
- [x] Record runner/front, support-screw/rail, shelf-pin datum and base seam checks
  as reusable construction requirements rather than copying final project offsets.
- [x] Remove stale brace-base review guidance; keep Korrekt and one-face policies.

### WP3: presentation delivery and fresh evaluation

- [x] Expose compatible installed headless Blender reuse through shared entrypoint,
  with runtime probe, one-job memory limits and fallback provisioning.
- [x] Keep illustrative open poses distinct from verified kinematics.
- [x] Run focused regression tests and skill validation; review changes.
- [x] Launch fresh agent on this branch, without old assembly code/evidence or
  conversation fixes. Give room envelope, material and functional preferences only.

## Audit log

- 2026-09-16: User reversed the merge instruction. Branch rebase and fresh branch
  evaluation are authorized; main/installed-skill promotion is deferred.
- The review found meaningful shared policies already present: complete drawers
  and compact supports, symmetric structural fronts, 3 mm starting stack gaps,
  Korrekt feet and independently segmented decks, full System32 Ø5×13 mm holes,
  one-face fallback rules, geometry-preserving bake and bounded inspect lights.
  These do not establish cold-start reliability or fabricated-part qualification.
- 6 mm HDF remains a selected material subject to runner/load compatibility,
  rather than a universal safe bottom thickness for every drawer system.

- Capture validation: 48 focused tests passed, and all seven affected skill entrypoints
  passed quick validation. Independent review accepted responsibility placement but
  found two defects: explicit mass must not clear load qualification, and automatic
  discovery must not select an incompatible Blender. Both were corrected with
  targeted regressions; final review and commit follow before fresh launch.

- Final targeted verification after review fixes: 21 tests passed. The previous
  48-test run and seven skill validations remain recorded above; counts overlap.
  Reviewer confirmed both fixes and coherent ownership, all changed production
  files below 150 lines. No full build success is inferred from these unit tests.
- Committed checkpoints: `48f34b1` source recovery, `5e786bf` explicit mass/load
  status, `dfbbcd6` cabinet-owned shelf grid, `5f98aea` neutral lighting,
  `fcdaf36` compatible engine reuse, `54f67b2` construction review guidance.
- Launched fresh no-history agent `/root/vilja_branch_cold_start` with the room
  envelope and functional/material preferences. It must load branch-local skills,
  write `local-evidence/skill-cold-start-20260916`, and maintain its own plan.
  Previous project code/evidence is excluded; shared skill changes during the
  evaluation must be reported rather than silently folded into its result.
  Viewer replacement and finished-build inspection remain pending.


### Cold-start finding: design inspection and fabrication were conflated

- [x] Fresh agent independently reproduced the missing 400 mm drawer installation
  and the 79 mm versus 80 mm foot source-pose limitation. These remain recorded
  cold-start failures, not retrospectively passed evaluations.
- [x] Add a bounded provisional drawer review route under the user's ongoing
  request to inspect a complete design: exact hardware and actual proposed
  construction, explicit unknown pilot/motion requirements, no fabricated PASS
  and no changes to complete-review/fabrication gates. This matches the existing
  provisional hinge-review boundary and keeps sourcing active.
- [x] Independent review and skill validation passed; continue the agent as an assisted
  continuation. Its later outputs must not be reported as an unassisted pass.

- Named the existing construction GLB exporter for provisional inspection; no
  validator or completed-review gate was bypassed or changed.
