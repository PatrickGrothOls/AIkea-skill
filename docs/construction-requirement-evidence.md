# Construction requirements and current evidence

## Scope and current state

Branch `feat/construction-requirement-evidence`, based on reviewed WP4a `ecda53e`.
This WP4b slice connects explicit requirements to the existing construction and
fabrication checks. Implementation and independent review are complete; WP4 contact/position evidence
and the later component migrations remain open.

## Work package and tasks

- [x] Declare requirements independently of executed operations, including
  unresolved work and justified loose-part or floor-contact dispositions.
- [x] Emit editable requirements from the standard recipe; use the same values
  for authored assemblies and check exact owned physical/operation paths.
- [x] Require material identity and selected purchase identity where applicable.
- [x] Bind visual decisions and extension evidence to current construction inputs.
- [x] Qualify custom joints through the existing scoped feature evidence contract.
- [x] Exercise missing work, stale inputs and qualified/unqualified extensions.
- [x] Run the `review` skill, fix findings and recheck this slice.
- [x] Prepare the coherent checkpoint after the complete diff review.

## Audit log

1. Patrick approved explicit requirement coverage and qualified extensions in the
   foundation plan. A requirement declaration records the brief; the checker
   cannot reconstruct a requirement that was never declared.
2. Reuse typed project values, physical tree paths, registered feature evidence,
   and the existing visual decision. No additional approval flow or ready flag.
3. A recorded connection verifies operation coverage, not strength. Requirements
   about loads, material suitability or movement need their own applicable
   evidence. Unknown requirements stay unresolved during previews.
4. Typed owner-relative requirements are independent of executed operations.
   Removed operations no longer disappear together with their obligations.
   Existing unassessed projects remain usable as previews and visibly incomplete.
5. Current-context hashes cover declared values, placements, selected products,
   `aikea.yaml`, assembly Python inputs and feature manifests. Existing STEP/GLB
   geometry checks remain authoritative for actual solids. Old approvals without
   this context binding cannot grant readiness after migration.
6. A two-panel paired-pocket test extension passes the shared executor and
   independently checks its world-space registration. Qualification separately
   requires its exact registered participants, current exports and passed feature
   evidence; incomplete scope, stale material or failed checks do not qualify it.
7. Primary review found that an already-open viewer could approve a replacement
   proposal with unchanged GLB bytes but different inputs. The viewer now pins the
   input context, and the existing locked decision rejects a changed proposal.
   Build producers also reject source edits made during generation.
8. Independent review found that hardware had no satisfiable installation path,
   and the generic preview had not wired in extension qualification. Both are
   fixed: features declare exact purchased paths and matching current evidence;
   preview and fabrication use the same resolver and requirement checks.
9. The existing manifest registration method now accepts those explicit purchased
   paths and qualified joint IDs. The paired-pocket/installed-pin tests use that
   actual producer, rather than hand-writing a separate registration convention.

## Verification

- Requirement/evidence, fabrication and generation regression: **42 passed**.
- Current-input decisions and concurrency regression: **12 passed**.
- Boundary/context/full-wardrobe/door-plan regression: **16 passed**, 212 seconds.
- Final configured/custom parity, extension/hardware and feature-composition
  regression: **18 passed**, including a removed configured joint whose obligation remains.
- These sets overlap; counts are not additive. The independent reviewer ran five
  targeted closure cases and reported no remaining findings.
- `review` skill critical/informational passes and testing specialist review are
  complete. All changed Python files are below 150 lines. Skill package/link
  validation and `git diff --check` pass. No remote CI, push or merge is claimed.
