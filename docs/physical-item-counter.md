# Physical item counter

> Historical implementation record imported from the earlier feature branch. Current integration and fresh evidence: [wardrobe-inventory-integration.md](wardrobe-inventory-integration.md).
## Scope

Implement the first repeatable closed-assembly inventory, following Patrick's
confirmed counting rules. Keep physical component coverage separate from
installed purchase sets. This slice does not approve a design or calculate a
selling price.

## Current state

The draft counter is implemented on `feat/physical-item-counter`, stacked on the
approved parts-breakdown documentation. No customer design is selected. Skill storage
persistence remains unresolved and deferred while Patrick is away from his Mac.

## Work packages

- [x] WP1 — Declare installed purchase identities in generated hardware.
  - [x] Link both KA 5332 sides to one exact runner set.
  - [x] Link KA 4532 fixed/moving members across owners; count spacers separately.
  - [x] Retain hinges and plates as explicit pieces, with included mounting screws.
- [x] WP2 — Export the physical inventory from the closed assembly tree.
  - [x] Preserve every panel and hardware path, including repeated local IDs.
  - [x] Validate Cabineo cuts and emit one brass insert per connector.
  - [x] Reconcile declared purchase members; expose missing information.
  - [x] Write a draft report without replacing fabrication BOM records.
- [x] WP3 — Verify and document the command.
  - [x] Exercise generated mixed-rail furniture and corrupted counting evidence.
  - [x] Check hinges, handles, supplied-fastener policy, and unresolved inputs.
  - [x] Review the diff and commit the coherent counter slice.

## Audit log

1. Patrick confirmed hinges and handles belong in the BOM, and mounting fasteners
   are supplied with purchased parts. Brass inserts remain separate, exactly one
   Häfele 267.91.314 per Cabineo. This prevents missing hardware and double charges.
2. Patrick's “Yes” authorizes implementing the documented counting slice. Use
   explicit purchase membership because CAD nodes are not purchasing units.
   Missing declarations remain visible rather than guessed from mesh counts.
3. The report remains a draft inventory: material propagation, missing features,
   construction choices, supplier pack rules and design approval are separate
   requirements before a complete customer quote.

4. Counting the generated fixture exposed the existing drawer-part contract,
   which has local dimensions but no named panel-dimension map or outline. The
   exporter now supports both real contracts without inventing material IDs.
5. Shared hardware declarations live in the build runtime. Feature generators
   import them directly so they also work with older project-local contracts;
   no migration or overwrite of existing client assembly files is needed.
6. Scope review: counter orchestration, paired-cut validation, purchase grouping,
   and CLI file handling have separate responsibilities. All changed code files
   are below 150 lines. The bounded review of the existing hinge-plan module
   measured 138 lines and recommended retaining its coherent current structure.

## Verification and limits

Passed 50 focused tests across counting, hardware generation, assembly contracts,
taxonomy upgrades and fabrication gates. Skill validation passed. A direct CLI
run wrote the expected totals and returned exit 2 with 95 unresolved records, as
designed for this incomplete fixture.

The generated mixed-rail fixture uses supplier-CAD test doubles; it proves item
ownership/counting, not vendor geometry fidelity. It intentionally retains a
legacy project-local hardware contract while generating current features.
Expected result: 61 panels, 127 verified Cabineos, 127 inserts, one 9057405 pair,
one 9114276 pair, and two 13952 spacer pieces. Riex hinge/plate generation and
generic declared handles are covered separately. Missing/duplicate/wrong-index/
wrong-part Cabineo cuts and invalid purchase memberships cannot silently count.

All current generated panels still lack material IDs. Shelf-support products,
17 base relationships, and four unused door-hinge relationships remain unresolved
in the mixed-rail fixture. The counter does not prove intended-feature coverage,
resolve absent handles, bind an approval fingerprint, or reconcile modeled
Cabineos with their cut-derived occurrences. These remain explicit follow-up
requirements before a complete priced order. CNC geometry is unchanged.

Usage and report semantics are in
[the skill reference](../aikea-review-unit/references/physical-item-counting.md).
