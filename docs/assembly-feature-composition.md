# Assembly feature composition

## Scope

Make each cabinet feature return through the recursive `BuiltAssembly` contract.
This branch covers drawer-part placement, installed doors and hinges, runner and
lighting hardware ownership, and one deterministic feature-builder entry point.
Wardrobe-level positioning and viewer traversal remain separate stacked work.

## Workpackages and tasks

### WP1 - Feature contract audit

- [x] Trace drawer parts, child placement, runners, and locking devices.
- [x] Trace door machining, hinge geometry, and cabinet placement.
- [x] Trace lighting host-part replacement and luminaire geometry.
- [x] Identify the one generated cabinet builder that must compose all features.

### WP2 - Complete child and hardware trees

- [x] Give every drawer part a drawer-local placement.
- [x] Retain exact hardware asset identities and saved placements.
- [x] Return door machining and hinge instances through `BuiltAssembly`.
- [x] Preserve lighting host machining and luminaire placement in the same tree.

### WP3 - Deterministic cabinet entry point

- [x] Generate one complete-cabinet builder with explicit feature order.
- [x] Prevent features from silently loading the unmodified base builder.
- [x] Keep all declared specs and built values structurally aligned.

### WP4 - Verification

- [x] Test drawer-part traversal at arbitrary nesting depth.
- [x] Test declared door, drawer, runner, hinge, and lighting ownership.
- [x] Run all dependency-free feature tests.

## Next stacked branch

- [ ] Compose complete cabinets and the structural base under one wardrobe root.
- [ ] Hydrate every exact purchased-hardware solid in the generic review consumer.
- [ ] Run CadQuery fit, machining, and complete-wardrobe export tests.

## Current state

Complete cabinet builders now apply registered drawers, doors, and lighting in
explicit manifest order. Drawer-part frames and purchased-hardware identities
and placements live in the recursive assembly tree. The dependency-free suite
passes with 211 tests, and all five affected skills validate. Exact CAD
hydration and CadQuery fit tests move with the generic wardrobe review consumer
into the next stacked branch.

## Audit log

1. 2026-08-31 - Started this as a stacked branch on the completed generic tree
   and spec-owned placement contract so feature migration cannot alter the core
   traversal semantics.
2. 2026-08-31 - Chose a cabinet-local ordered feature manifest so new features
   compose without teaching the complete builder about feature types.
3. 2026-08-31 - Saved drawer-part and purchased-hardware frames in generated
   specs so review code consumes the tree instead of reconstructing placement.
4. 2026-08-31 - Kept exact CAD hydration in the review boundary because asset
   loading is an external operation shared by cabinets and wardrobe traversal.
5. 2026-08-31 - Verified 210 dependency-free tests plus the loopback review API
   test; 53 dependency-gated tests were skipped and two CadQuery-only modules
   remain uncollected until CadQuery is installed.
