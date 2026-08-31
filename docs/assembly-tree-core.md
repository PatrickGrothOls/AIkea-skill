# Assembly tree core

## Scope

Make the generated `BuiltAssembly` taxonomy the complete physical authority for
one recursively composed assembly. Add explicit part placement and one generic
tree traversal without changing current cabinet geometry or feature behavior.
Keep cabinet-feature migration and wardrobe-level composition in later stacked
branches so this branch remains independently testable and reviewable.

## Workpackages and tasks

### WP1 - Existing contract audit

- [x] Confirm that `BuiltAssembly` already owns nested child assemblies.
- [x] Confirm that purchased hardware already has local-to-parent placement.
- [x] Identify the missing explicit local-to-parent placement on built parts.
- [x] Record the exact legacy placement authorities that migration must preserve.

### WP2 - Complete physical node contract

- [x] Add an explicit local-to-parent placement slot to every built part.
- [ ] Make every generated assembly builder populate its part placements.
- [ ] Require every geometric hardware instance to have an explicit placement.
- [ ] Keep declared specifications and built values structurally aligned.

### WP3 - Generic recursive traversal

- [x] Add one depth-independent assembly-tree walker.
- [x] Accumulate local-to-parent frames into root coordinates.
- [x] Yield stable paths for parts, child assemblies, and purchased hardware.
- [x] Keep rendering, collision, BOM, and machining consumers outside the walker.

### WP4 - Verification and compatibility

- [x] Add arbitrary-depth nesting tests.
- [x] Add transform-composition and stable-order tests.
- [ ] Prove generated cabinet and base placements match their current locators.
- [x] Run focused composition and taxonomy tests.
- [ ] Run focused review tests after generated builders populate placements.

### Later stacked branches

- [ ] Make drawer, door, hinge, runner, and lighting builders return into the tree.
- [ ] Make the wardrobe builder position complete cabinet trees in run order.
- [ ] Replace feature-specific review stitching with generic traversal consumers.
- [ ] Run a fresh whole-skill fabrication and viewer test.

## Current state

The reusable tree contract and walker are implemented and covered by arbitrary
nesting, transform-composition, stable-order, missing-placement, and hardware
placement tests. Generated part builders still need to populate the new placement
slot from the current cabinet, base, and drawer placement authorities before
review consumers can switch to the generic traversal.

## Audit log

1. 2026-08-31 - Patrick confirmed that the complete cabinet builder is the
   assembly spine and that the wardrobe builder must recursively compose and
   position complete cabinet assemblies.
2. 2026-08-31 - Preserved the existing `BuiltAssembly` contract instead of adding
   a parallel `AssemblyNode`: it already expresses nested assemblies and hardware.
   The narrow missing contract is explicit part placement plus generic traversal.
3. 2026-08-31 - Split the migration into independently green branches because
   moving placement authority affects generated builders, review geometry,
   collision checking, and every downstream manufacturing consumer.
4. 2026-08-31 - Added frame composition and a generic tree walker without any
   rendering or furniture-specific knowledge. It exposes assembly, part, and
   hardware visits while preserving stable paths and root-relative placements.
