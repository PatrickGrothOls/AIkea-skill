# Assembly tree core

## Scope

Make the generated assembly taxonomy the complete physical authority for one
recursively composed assembly. Add explicit part placement and one generic
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

- [x] Add an explicit local-to-parent placement to every generated part spec.
- [x] Make generated cabinet and base builders retain those part placements.
- [x] Require every geometric hardware instance to have an explicit placement.
- [x] Keep declared specifications and built values structurally aligned.

### WP3 - Generic recursive traversal

- [x] Add one depth-independent assembly-tree walker.
- [x] Accumulate local-to-parent frames into root coordinates.
- [x] Yield stable paths for parts, child assemblies, and purchased hardware.
- [x] Keep rendering, collision, BOM, and machining consumers outside the walker.

### WP4 - Verification and compatibility

- [x] Add arbitrary-depth nesting tests.
- [x] Add transform-composition and stable-order tests.
- [x] Prove generated cabinet and base frames match their legacy formulas.
- [x] Run focused composition and taxonomy tests.
- [ ] Run focused review tests after generated builders populate placements.

### Later stacked branches

- [ ] Make drawer, door, hinge, runner, and lighting builders return into the tree.
- [ ] Make the wardrobe builder position complete cabinet trees in run order.
- [ ] Replace feature-specific review stitching with generic traversal consumers.
- [ ] Run a fresh whole-skill fabrication and viewer test.

## Current state

The reusable tree contract and walker are implemented. Cabinet and structural-base
part frames are now resolved into their generated specifications; builders are
rejected if their built parts differ from those declarations. The former cabinet
and base locators now only convert saved frames into CadQuery locations. Drawer
parts and feature builders remain the next stacked branch.

The dependency-free suite passes 204 tests with 53 expected skips when the one
viewer-server API test is allowed to use a local socket. Fifteen focused CadQuery
geometry tests are among the skips because CadQuery is not installed here.

## Audit log

1. 2026-08-31 - the maintainer confirmed that the complete cabinet builder is the
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
5. 2026-08-31 - Put part placement on `PartSpec`, not `BuiltPart`. Placement is a
   declared property of the assembly taxonomy, while `BuiltPart` only materializes
   the declared part as a solid. This prevents each consumer from rebuilding the
   cabinet's spatial rules independently.
6. 2026-08-31 - Replaced cabinet and base placement calculations in review locators
   with one conversion of the saved spec frame. Pure tests preserve the exact
   origins and axes used by the previous formulas.
7. 2026-08-31 - The required 150-line review separated materialized `Built*`
   values and their alignment invariants into `assembly_composition.py`; declarative
   part, cabinet, and base schemas remain in `specification.py`. Existing imports
   from `assemblies.specification` remain compatible through re-exports.
