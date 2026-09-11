# Shared surface grooves

## Scope and current state

Branch `feat/shared-surface-grooves`, based on `0a741ba`. Implementation and review complete.
Provide the existing straight lighting groove as a role-independent local machining
operation. Lighting will supply its product dimensions and face placement in the
following component slice. The operation itself has no furniture or light knowledge.

## Work package and tasks

- [x] Declare positive length, width and depth in a saved panel surface frame.
- [x] Share actual entry-face validation with surface drilling.
- [x] Use common dispatch, complete-material checks, cut ownership and output checks.
- [x] Verify orientation, dimensions, old groove parity and clipped/overlapping failures.
- [x] Review with the review skill and resolve findings.

## Evidence boundary

The contract describes a straight rectangular volume starting at the center of
one end, +X along the run and +Z into the material. The full volume must fit
available material; the opening must lie on an actual entry face. Blind ends,
cutter radii, routing access and product-specific installation remain fabrication
questions. This adds no automatic reuse of an existing groove or prior holes.

## Audit log

1. Use an explicit local operation rather than treating lighting as a panel joint.
   This preserves the lighting skill's ownership rule and allows other designs to
   request the same simple groove without duplicating its construction code.
2. Reuse the established panel executor and strict local-cut checks; do not add a
   second light-specific Boolean subtraction path.

## Validation and review

55 focused tests pass across grooves, shared drilling, exact hole reuse and
Korrekt mounting. All nine skill packages validate. The independent review skill
specialist found no issues: a groove entering the 45-degree edge of a triangular
panel matches a separately extruded prism exactly, including after parent rotation
and translation. Buried/over-depth raw output, changed surface frames and attempts
to reuse grooves as holes fail through the common checks.

The inherited public `specification.py` reached 151 lines. Its independent scope
review found coherent immutable construction records and compatibility re-exports,
with execution kept in separate modules. No immediate split is warranted. A future
separation of recipe-specific records is appropriate if independent behavior grows;
type unions now agree across every common/configured assembly contract.
