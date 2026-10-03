# Verify exported furniture despite nearly coincident vertices

## Scope
Keep the 0.002 mm export tolerance and prove a bijection of oriented triangles.
The old nearest-vertex map conflates distinct source vertices at float32 precision,
then incorrectly rejects unchanged hinge surfaces. Do not rebake or alter geometry.

## Work packages
- [x] Diagnose the real rejected hinge independently from GLB bytes.
- [x] Replace ambiguous nearest-vertex mapping with oriented triangle correspondence.
- [x] Test changed geometry, winding, duplicate counts and ambiguous correspondence.
- [x] Run every real exported part through the corrected check.
- [x] Review scope, update the procedure and commit the verified correction.

## Current state
Nine focused tests pass, plus three unchanged packing tests. Failed hinge has 73,632 source and output triangles;
all match bijectively with winding preserved and maximum error 0.000543457 mm.
Its 36,807 exact source vertices collapse to 36,790 at float32 precision. Evidence:
local-evidence/hinge-export-diagnostic.json and hinge-failure-geometry.npz.
Bake03 finished but original final verification failed, so no presentation PASS
has been issued and no baked visual delivery made. The original files are retained.
The full revised comparison passed all 174 parts. Maximum vertex difference is
0.000794331 mm, below 0.002 mm, with a complete oriented triangle bijection.
export-geometry-rechecked.json and presentation-rechecked.json record recovery
without rewriting the original failed log. The delivery finalizer verifies every
hash in the packing and metadata chain and matches the two assets' identities.
The installed engine's Python successfully imports and executes the new verifier
without extra dependencies. The small full-engine acceptance fixture was adjusted
for explicit exported-scene loading and ValueError; its render rerun is deferred
while another task's Blender animation is active. No new render is needed for the
actual Vilja output, whose prepared, coverage, shaded and final export checks pass.

## Audit log
1. 2026-09-15: Final verification rejected cabinet_01/hinge_04_hinge. Independent
   direct-GLB comparison proved all triangles match within the unchanged tolerance.
2. GlbWorldGeometry owns scene transforms and indexed geometry; triangle comparison
   owns candidate search and one-to-one matching; ExportGeometryVerification owns
   whole-artifact identity and report composition. No Blender invocation is needed
   for geometry comparison, so this does not compete with the other active render.
3. Boundary review using review-code-boundaries: PASS. Existing export verifier
   shrinks from 61 to 26 lines and delegates to coherent scene reading (53 lines) and
   geometric correspondence (65 lines). These owners contain no furniture-specific
   policy. No existing file crosses 150 lines. Dependency remains NumPy, already
   supplied by the pinned Blender engine; no SciPy or new renderer is required.
4. Changed vertex position, reversed winding, missing triangles and duplicated
   replacement faces all fail. Cyclic vertex order, sub-tolerance export rounding
   and ambiguous candidate assignment pass only with a complete bijection. Matrix
   tests cover glTF quaternion order, scale order, column-major storage and parents.
5. Actual model revalidation and hash-bound delivery derivation PASS. Original bake
   failure remains recorded; revised verification did not change source/export bytes.
6. Corrected baked and inspection assets delivered in the existing port63332 tab.
   Live DOM verified baked-to-inspection-to-baked transition,174pieces,7inspection
   lights,1canvas and no photo renderer. Original manufacturing gaps remain open.

## Before merging
- [ ] Rerun tests/blender_bake_acceptance.py with the provisioned engine when the
  other render is finished. This branch remains local; no push or merge performed.
