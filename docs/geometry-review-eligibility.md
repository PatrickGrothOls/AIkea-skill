# Geometry eligibility for fabrication review

## Scope and current state

Branch `fix/geometry-review-eligibility` makes standard review proposals obey the
same shared geometry result as the common construction command. The full WP7
standard replay exposed an approval proposal despite twelve uncertain geometry
interfaces. The final fabrication gate already blocked that design. This slice
fixes the earlier proposal and live-session boundary. Implementation and review
are complete: 43 affected tests pass and independent review has no findings.

## Work package and tasks

- [x] Reproduce legacy-valid/shared-invalid proposal creation in the real standard flow.
- [x] Carry this run's shared geometry status and report through the renderer result.
- [x] Withhold proposals for invalid, missing, stale or skipped shared evidence.
- [x] Reject stale existing-session decisions without rewriting historical records.
- [x] Keep the inspection GLB available and expose invalid status through the CLI.
- [x] Test valid-to-invalid transitions with unchanged GLB bytes and construction hash.
- [x] Verify ordinary valid, open and presentation routes.
- [x] Run independent review using the review skill and record the result.

## Audit log

1. The fresh standard trial passes seven legacy position checks but has twelve
   uncertain shared interfaces. Approval must use the shared result, not only
   the canonical filename and door pose; this implements the agreed common checks.
2. Preserve proposed and approved records byte-for-byte when new evidence blocks
   them. A small saved-record reader checks schema, valid status and a matching
   nonempty construction hash inside the existing review read/locked decision
   path. A stale open viewer receives the existing conflict response. Historical
   user decisions remain on disk; no new decision history or readiness engine.
3. Requiring the entire fabrication gate here would be circular because visual
   approval is one of its inputs. Missing manufacturing requirements continue to
   block the final gate independently, even when geometry permits visual review.

4. Final regression: 43 passed in 107.79 seconds across eleven files, including
   real generated standard closed/open CLI runs and an injected shared-invalid
   result after successful legacy positioning. The first run's three new fixture
   failures lacked the intake's required third height measurement; the corrected
   fixture and complete affected rerun pass. Initial logs remain preserved.
5. Independent review reproduced 18 live eligibility failures on the exact old
   source and passes all 21 patched HTTP/session probes plus 12 proposal probes.
   Proposed and approved history remains unchanged when evidence becomes invalid.
   The actual saved standard GLB/report also refuses a proposal; CLI result
   handling reports invalid/exit 2 while retaining inspection. That last check
   reuses saved CAD output; it is not a new full manufacturer-CAD regeneration.
   Review source snapshots, hashes, commands and results are in ignored
   local-evidence/shared-construction-20260912/independent-review-eligibility.
