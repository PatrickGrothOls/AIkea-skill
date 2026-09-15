# Compact static CAD review geometry

## Scope
Corrected Vilja has 174 parts but 18,181 glTF draw primitives, including 431 surfaces
per hinge. Preserve exact geometry and materials while combining surfaces within
each physical part/material. This directly addresses the requested lightweight
inspection without reducing manufacturing detail.

## Work packages
- [x] Read actual primitive counts and identify the render bottleneck.
- [x] Implement static embedded-buffer repacking by part/material/attribute signature.
- [x] Compare every indexed attribute bitwise and preserve transforms/identity.
- [x] Verify material boundaries, image bytes, idempotence and unsupported animations.
- [x] Pack the real inspection model and verify it visibly with seven lights.
- [x] Review boundaries and update the skill procedure.
- [x] Commit the validated checkpoint locally.

## Current state
Three targeted tests pass. The real model drops from 18,181 to 174 primitives with
every indexed attribute bitwise equal and materials/nodes/transforms unchanged.
Independent audit retains 174 identities, 16 legs and plates, seven attached emitters
and the exact outside envelope. The existing immutable Blender input and running
bake remain untouched. Packed inspection output is a new file.
No geometry simplification, normal recomputation or renderer-only finishing.

## Audit log
1. 2026-09-15: Measured 18,181 primitives for 174 parts after browser timeouts.
   Consolidating compatible primitives changes GPU submission, not CAD triangles.
2. StaticGlbBuffers owns embedded buffer IO; ReviewMeshPacker owns grouping and
   indexed-attribute proof; the CLI only adapts arguments. Files stay below 150 lines.
3. Boundary review using review-code-boundaries: PASS. New production owners are
   StaticGlbBuffers (embedded IO), ReviewMeshPacker (compatible grouping and proof)
   and PackReviewMeshesCommand (argument boundary). No construction, lighting or
   furniture-specific policy enters shared infrastructure. No existing code file grows.
4. Material boundary, embedded image preservation, repeat output and unsupported
   animation tests pass. Real indexed-attribute comparison and envelope/ownership
   audit pass. Hardware ownership correction is applied separately to a new local
   evidence asset, preserving all binary chunks and every other JSON value.
5. Live inspection exposed two representation assumptions. LightingEmitterFace
   now finds the local +Z emitting face using preserved source normals, so a
   consolidated solid still yields one area light. ExplodedGroupLayout uses the
   single carrier panel's thickness axis even when fittings enlarge its group.
   This prevents full-height hinged doors moving vertically. No source poses change.
6. Expanded boundary review PASS: LightingEmitterFace owns emitter-face selection
   (17 lines), LightingSource retains source identity and placement (86 to 86),
   ExplodedGroupLayout retains inspection offsets (44 to 46). The packer remains
   ignorant of furniture and lighting rules. Other new production files: 72, 74,
   17 lines respectively. All remain below the 150-line review trigger.
7. 64 viewer tests pass and the production bundle builds. Same-tab DOM confirms
   174 pieces, seven live sources, one canvas and no photo renderer. Visual checks
   show separated panels, leg base and the right-side strip with shelf supports.
   This verifies inspection behavior, not completed Blender quality or peak memory.
