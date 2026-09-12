# Whole-front hinge component

## Scope and current state

Branch `feat/assembly-door-component`. Integrate an explicit multi-part front
child with the existing NC70 hinge planner, sourced hardware frames and shared
layer drilling. Construction and generic moving review are verified and reviewed.

## Work package and tasks

- [x] Supply a dimension-only front datum from the actual child without adding stock.
- [x] Reuse hinge layout and purchased hardware declarations for slab and child hosts.
- [x] Route real cup/pilot segments to child layers and plate holes to the parent.
- [x] Move or hide the complete child through generic tree review.
- [x] Verify both hands, current plan binding, quantities, parent transforms and removal.
- [x] Verify fresh saved-project generation and source-CAD review.
- [x] Complete the review skill and close findings.

## Audit log

1. Keep the original physical child and its layers. A temporary dimension-only
   mounting datum lets the existing upright hinge planner operate without making
   its slab calculation a new physical panel or combining inventory identities.
2. This host supports a directly owned flat panel assembly with its datum at the
   lower/back corner. The shared layer recipe enforces parallel broad faces and
   continuous material at each bore. It does not infer adhesive or load ratings.
3. Use existing generic child motion for the whole front. Exact open hardware CAD
   remains a presentation overlay; sampled poses are not full motion-clearance
   certification. The separately owned mounting support remains stationary.

4. Independent review reproduced a 10 mm frame border accepting a saved hinge
   feature before the full build rejected its cup/opening clash. Added real-part
   preflight within the project runtime before writes/registration, and included
   the installation plan in that conflict-checked write set. A rejected generation
   must preserve the prior active plan and feature. The source test verifies no
   generated files/registration on failure and a still-buildable original parent.

## Validation and review

- Seven focused tests passed after the preflight repair, including the existing
  slab feature generator. The prior explicit-host regression also passed.
- Independent checks covered both hands, opposite support faces, current plan
  binding, duplicate purchase rejection, edited-file conflicts and regeneration.
  Invalid regeneration preserves the previous plan and every generated file.
- Six fresh complete-review CLI exports used checksum-verified vendor STEP files:
  both hands in closed/open/removed states. Closed/open each contain three real
  panels and six hardware bodies; removed retains only the stationary support.
- Parent-transformed review moves every front layer together. Purchase frames
  agree with the established slab path. No extra inventory panel is introduced.
- The review skill's preflight finding was fixed and independently closed; no
  remaining component findings. Ten skills validate and the diff check is clean.

Local evidence: `/private/tmp/assembly-door-closure-review-0sfgveb0` (source CAD
exports and failure-preservation checks) and
`/private/tmp/assembly-door-frames-review-el9jnrb6` (frame comparison).
The reports retain `manufacturing_authority=false`; adhesive, installation,
load and full motion-clearance evidence remain separate.

5. The ordinary `build_furniture_design.py` command was separately reproduced
   failing to hydrate declared hardware despite available source CAD. That common
   command integration is the next small slice; it does not invalidate the fresh
   complete-review exports above.
