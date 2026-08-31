# Wardrobe tree composition

## Scope

Generate one wardrobe-root assembly that owns the structural base and every
complete cabinet in saved left-to-right order. Review and export must traverse
that one tree without reconstructing cabinet positions.

## Workpackages and tasks

### WP1 - Existing placement audit

- [x] Trace saved unit order, widths, and project-local cabinet origins.
- [x] Trace structural-base ownership and placement.
- [x] Trace every full-wardrobe review geometry consumer.

### WP2 - Wardrobe root

- [x] Generate a wardrobe specification with explicit child placements.
- [x] Generate a wardrobe builder that loads every complete child builder.
- [x] Preserve declared and built child order exactly.

### WP3 - Generic review consumer

- [x] Render parts and purchased hardware from `AssemblyTreeWalker` visits.
- [x] Hydrate exact registered hardware geometry at the review boundary.
- [x] Remove transient cabinet-position reconstruction from default full review.

### WP4 - Verification

- [x] Test arbitrary cabinet counts.
- [x] Test accumulated cabinet, drawer, part, and hardware frames.
- [x] Run the dependency-free suite and skill validation.
- [x] Run CadQuery fit and full-wardrobe export tests.

## Next stacked branch

- [ ] Pin and document the Python and Node source-development environments.
- [ ] Migrate specialized open-drawer pose additions off the compatibility adapter.
- [ ] Generate one fresh cabinet with combined features and review it through the root.
- [ ] Require all fabrication evidence before emitting a fabrication-ready result.

## Current state

`wardrobe_01` now owns the structural base and all complete cabinets in saved
order. Default full-wardrobe export hydrates exact registered hardware and
renders one recursive tree. The dependency-free suite passes 216 tests; 13
targeted CadQuery construction and full-export tests also pass in the configured
geometry runtime. The specialized open-drawer review path remains isolated in a
compatibility adapter for migration during the fresh combined-feature run.

## Audit log

1. 2026-08-31 - Started as a stacked branch after complete cabinet builders
   became the sole feature-composed cabinet entry points.
2. 2026-08-31 - Made the structural base the first wardrobe child, followed by
   cabinets in saved left-to-right order, preserving existing export naming.
3. 2026-08-31 - Extracted wardrobe taxonomy types after the required 150-line
   responsibility review; cabinet, base, part, and joint taxonomies remain one
   stable build-unit contract.
4. 2026-08-31 - Kept vendor-specific CAD loading behind a provider registry so
   the recursive walker remains independent of hardware families.
5. 2026-08-31 - Isolated legacy posed drawer additions rather than mixing their
   presentation transforms into the new default tree consumer.
