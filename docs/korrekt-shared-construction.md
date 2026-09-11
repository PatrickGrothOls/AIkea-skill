# Korrekt mounting through shared construction

## Scope and current state

WP5d machining slice on `feat/korrekt-shared-construction`, based on `8aa3ac9`.
Reuse the sourced Korrekt tooling from `fc78dfa` and execute its participant cuts
through the common panel feature path. Implementation and review are complete. This slice
does not choose a new leg layout or add physical fit/load authority.

## Work package and tasks

- [x] Reuse the measured 61854 pattern, footprint, clearance checks and source hash.
- [x] Generate the same overshooting through-holes with shared SurfaceHolePattern.
- [x] Apply recorded participant cuts through the shared feature/validation path.
- [x] Check geometry parity, rotations, thicknesses, split decks, prior cuts and
  child/hardware preservation, plus ordinary machining-feature regressions.
- [x] Review with the review skill and fix/recheck findings.
- [ ] Follow with complete leg-feature ownership and current scoped evidence;
  preserve unknown physical installation questions separately.

## Audit log

1. Reuse `fc78dfa` Korrekt tooling selectively; do not import the finishing stack's
   divergent construction contracts. The source dimensions and chosen pilot/access
   diameters stay unchanged.
2. Shared PanelMachiningFeature now accepts explicit joint operations with an
   injected builder, in addition to local drilling. It uses the same participant
   accounting, cut applicator and independent output validation. Unsupported
   default joint requests still fail, and custom joints still require scoped
   qualification at fabrication readiness.
3. Korrekt's total material-removal check remains component-owned: it verifies a
   whole mounting pattern across joined deck pieces before common execution.
   It does not relax local drilling's complete-hole rule or permit silent reuse.

## Validation and review

The 15 Korrekt geometry/boundary tests pass. Before the two extra boundary
tests, the combined Korrekt, drawer-host and shared-surface regression passed
30 tests. All nine skill packages and their links validate. Independent testing
review compared 30 thickness/rotation cases against the original raw cylinders
with zero symmetric difference, plus three rotated half-lap cases. Wrong cut
ownership and a pre-existing shallow mounting pilot are rejected. Prior unrelated
cuts, children and purchases survive.

The review found a missing part accessor in the new test fixture. The fixture
was completed and all 15 tests rerun successfully; production contracts were
unchanged. No unresolved code review findings remain. Physical fit, screw
engagement, access and structural/load approval have not been demonstrated.
