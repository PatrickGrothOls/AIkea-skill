# Uncertain CAD intersections

## Scope and current state

Branch `fix/uncertain-cad-intersections` prevents a contradictory CAD Boolean
result from being reported as clear geometry. Implementation, focused checks
and independent source-CAD review are complete. Final integration regression
is tracked in the shared construction plan.

## Work package and tasks

- [x] Reproduce the missed source-plate collision in several rigid frames.
- [x] Independently classify common interior points and exclude native-location loss.
- [x] Retain the existing tolerance and cross-check common versus both subtraction volumes.
- [x] Report inconsistent pairs as unresolved/invalid before considering contact allowances.
- [x] Verify analytic contact/clearance/small-overlap controls and all three source pairs.
- [x] Complete the review skill, including retained allowance-bypass coverage.
- [ ] Complete final candidate regression in WP7.

## Audit log

1. Source CAD gives different intersection volumes after rigid transforms despite
   independently verified common interior points. Eight kernel settings did not
   repair all three source pairs across four frames; increasing fuzzy tolerance
   also erased a known small analytic overlap. Do not choose a favorable frame
   or relax the geometry tolerance to manufacture a passing result.
2. Compare intersection volume with material removed by A-minus-B and B-minus-A
   at the existing 0.0001 mm³ threshold. Disagreement is an explicit numerical
   uncertainty, not a fabricated collision volume or evidence for a contact
   allowance. This is a consistency check, not mathematical certification of CAD.
3. Position records now include uncertain_intersections and must reproduce this
   diagnostic too. Older records require regeneration through current checks.

4. Independent review found one retained-coverage gap: the false-empty-common
   regression did not include a valid contact allowance. The existing test now
   runs with and without that allowance and requires zero allowed overlaps.
   This preserves the demonstrated approval boundary without committing vendor CAD.

## Validation

Twenty-five focused tests pass. Independent source-CAD review confirms all six
real pair/frame cases remain invalid and uncertain despite generous valid
allowances. Fourteen analytic controls preserve clearance, touching and small
overlaps; a consistent ordinary overlap still receives its intended allowance.
Five additional scalar-boundary probes reject inconsistent/non-finite volumes.
The review skill is complete with its one informational test finding resolved;
there are no outstanding production or test findings. Whitespace checks pass.
