# Base configurator through shared construction

## Scope and current state

WP5a on `feat/base-configurator-construction`, based on reviewed WP4c `2775a4b`.
Implementation and review are complete. Preserve the current segmented sheet-base recipe,
its paired Cabineo machining and its unresolved deck/support/seam decisions.
Adjustable-foot replacement is a separate component migration in WP5.

## Work package and tasks

- [x] Route base assembly and individual-part entry points through the same
  `PanelAssemblyBuilder` used by configured cabinets and custom panels.
- [x] Append explicit local machining inputs without changing positional callers;
  emit independent construction requirements from the base recipe.
- [x] Compare configured and directly authored base solids, placements, cuts and
  inventory against the existing construction, including unresolved connections.
- [x] Test local adaptation and exact missing-work diagnostics; run relevant base
  geometry and review regressions.
- [x] Update the component's host/input/effect/evidence guidance.
- [x] Run the review skill, fix/recheck findings and commit this slice.

## Validation

- 11 generator, taxonomy and base-part tests passed.
- Eight configured/direct parity and paired-Cabineo tests passed, plus 52 subtests.
- Three tree-generation and base-review-export tests passed.
- Two saved-taxonomy upgrade tests passed; all nine skills and links verified.
- Independent testing review reconstructed the actual previous base files:
  recorded output upgrades, an edited deck builder blocks every write, and an
  unrecorded older base remains untouched. No findings remained in either review.
- The base's unresolved supports/seams and missing materials remain visible;
  these tests do not approve a furniture design or establish load capacity.

## Audit log

1. Patrick authorized useful configurators as optional recipes over shared tools.
   The existing base dimensions and joint layout remain the reference for this
   migration; no new engineering claim or support policy is introduced.
2. Independent scope review checked the inherited module renderer, spec renderer
   and specification contracts. Their responsibilities are coherent; a few base
   fields do not justify splitting the public dataclasses or serializers. Remove
   the unused old physical builder template when its last producer is migrated;
   retain demonstrated metadata-upgrade compatibility.
3. The shared route preserves 19 panels, all existing paired cuts and inventory
   in the reference base. Removing a declared connector leaves its independent
   requirement missing; translating/rotating the base inside an authored parent
   needs no new construction engine. These are local software checks only.
