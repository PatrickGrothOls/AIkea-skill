# Hardware in the common furniture build

## Scope and current state

Branch `fix/construction-hardware-loading`. The ordinary furniture build must
resolve declared source-CAD hardware just as complete review does. Implementation
reuses the existing resolver inside the project runtime; focused verification and independent review pass.

## Work package and tasks

- [x] Reproduce a sourced multi-part hinge assembly failing in the common CLI.
- [x] Hydrate the complete tree before common geometry and construction checks.
- [x] Verify ordinary/fabrication exports include declared hardware and reject a
  missing provider without publishing a new successful report.
- [x] Re-run the real sourced hinge case through the CLI.
- [x] Complete the review skill and checkpoint the fix.

## Audit log

1. The same sourced hinge project already exports through complete review, but
   the common build failed on `hinge_01_hinge` lacking placed geometry. Its loader
   returned the declared purchase without invoking the existing CAD resolver.
2. Reuse the same resolver and recursive hydrator inside the existing project
   runtime. Hardware providers retain their exact-source requirements; no guessed
   shapes, swallowed failures or special-case door branch is introduced.

## Evidence

Ten focused tests pass, including ordinary/fabrication exports and existing
position-evidence checks. The synthetic provider verifies integration only.
Independent provider checks verify nested placement, project module access during
resolution, restored runtime imports and a missing provider invalidating the report
while preserving earlier GLB bytes.

The real source-CAD flat and transformed-parent CLI checks now finish and export
all nine physical items, including six exact hinge/plate purchases. All nested
bounds agree with the independently calculated parent transform. These particular
synthetic hosts contain real panel collisions; they remain INVALID, construction
incomplete and fabrication_ready=false. They prove the complete checking/export
path, not a valid cabinet. No contact allowance was invented.

Evidence: `/private/tmp/construction-hardware-review-ymd31159/closure.json` and
`/private/tmp/construction-provider-runtime-review-nck74dv_`.
The review skill and independent testing review found no remaining loading issue.

3. The moved collision fixture reports one additional plate/post overlap, while
   the common overlap volumes agree within 0.000002 mm³. Both designs fail. This
   unchanged geometry-check observation is retained for integration investigation;
   it is not described as approved mating contact or a successful design.
