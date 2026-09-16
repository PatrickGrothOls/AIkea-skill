# Reusable lighting routing module

## Scope

Patrick requested a Python module used by the skill, with an explicit machining
face, front edge and optional connector pocket at a specified end. Keep the
sloped light's cable behind the vertical profile; the vertical light connects
underneath the base. Supplier qualification remains outstanding.

## Current state

Reusable module, feature adapter and documented example implemented. 49 targeted
cases passed across the initial 48-case regression run and the updated 6-case
integration run (five repeated, one new ownership regression). Independent
geometry/code review found no remaining material blockers; the
`review-code-boundaries` skill review returned PASS. Three STEP coupons generated
with compatible broad-face audits.
No cabinet geometry changed. Test dimensions are synthetic, not vendor defaults.

## Work packages

### WP1: Common stepped recess machining
- [x] Add one generic union-of-pockets operation so intentional internal overlap
  is counted once while collisions with unrelated machining still fail.
- [x] Verify retained geometry and broad-face setup auditing.

### WP2: Lighting route module
- [x] Define face-local directed front edge, inward offset, end margins and
  connector choice (`none`, `start`, `end`).
- [x] Derive the light run, profile seat, narrower rear cable relief and optional
  connector pocket from one route; require explicit dimensions and remaining stock.
- [x] Provide the shortened light plan and machining operation for composition.
- [x] Test both faces, reversed/sloped routes, material removal and invalid inputs.

### WP3: Usage and review
- [x] Document a complete Python usage example and explicit provisional dimensions.
- [x] Run independent geometry/code review and targeted regression checks.
- [x] Finalize the code-boundaries skill review.
- [x] Generate inspectable STEP coupons and record their limits.
- [ ] Integrate the qualified detail into the full cabinet after supplier fit and
  cross-panel cable passage are established (separate from this module slice).

## Audit log

- User approved a reusable face/front-edge/connector-end module. The operation
  will use a common stepped recess rather than sequential overlapping grooves:
  existing validation correctly rejects overlap with earlier unrelated cuts.
  Combining regions within one declared operation preserves that protection.
- Front-edge direction defines start/end and its left-hand inward offset in the
  selected face coordinates. No global up/down assumption is allowed. Cut radii,
  cable relief and pocket dimensions are explicit caller inputs, not supplier claims.
- Profile seats overrun light endpoints by one cutter radius to accommodate
  rounded cut ends without changing the actual light length. Installed-body
  intersection tests verify this for the declared rectangular profile envelope.
- Independent review found that a direct component call could target another
  part for machining; fixed with an explicit same-host check and regression.
- An oblique test fixture initially placed its relief outside the polygon. The
  existing boundary check rejected it correctly; increased the fixture margin
  and checked the independent expected coordinates rather than weakening checks.
- Generated `local-evidence/lighting-route-coupons/connector-{none,start,end}.step`
  and `report.json`. Intentional overlap is counted once; unrelated earlier cuts
  still fail. No actual Domus compatibility, cable bend, base exit or strength
  qualification is implied by these local tests.
- Independent boundaries review PASS: shared operation 0→59 lines, registry
  35→37, setup checker 57→57; lighting spec 0→78, resolver 0→73, feature adapter
  0→19, existing lighting feature 46→50. All stay below the 150-line trigger.
  Core machining owns only generic regions/union/face access; lighting owns
  profiles, wire relief, pocket ends and setbacks. No additional extraction needed.
