# Installed source frames

## Scope and current state

Branch `fix/installed-source-frames` corrects a proof consumer exposed by the
complete WP7 regression after native CAD placement was fixed. Implementation is
complete. All 118 affected runner/drawer tests pass; independent review found no remaining findings.

## Work package and tasks

- [x] Reproduce the failures with the synthetic fixture and exact manufacturer CAD.
- [x] Verify source-point coordinates against actual installed GLB geometry.
- [x] Apply only the parent placement to already-native source points.
- [x] Correct fixture placements while retaining intended physical datums.
- [x] Add hand-derived baked/stored source and parent-transform coverage.
- [x] Run the affected drawer proofs and negative mutations.
- [x] Complete independent review using the review skill.

## Evidence and scope review

The exact runner source has nonidentity native locations on all four members.
Native hole coordinates already include those locations. Canceling them again
moved the first left depth axis from its correct 37 mm to 46.5 mm. Independent
isolated correction restores installed axes at height 23 mm; a 1 mm moving-rail
misalignment still rejects. Decoded GLB vertex bounds match the real installed
runner geometry within 0.000177341 mm.

The 170-line inherited test support received the required independent concern
review. Its source shapes, two hands and review states form one coherent exact
source fixture. This change adjusts two declarative placements and adds no new
responsibility. No immediate extraction is required; expanding mutation helpers
should move to the existing InstalledGeometryTestSupport. The scope report is
preserved with the private independent review evidence.

## Audit log

1. The full candidate regression found a real proof-frame mismatch in addition
   to obsolete fixture placements. Neither loosening proof tolerances nor only
   changing the fixture fixes the actual manufacturer-source failure.
2. Native source coordinates include the stored CAD transform; apply the parent
   frame once. Preserve the public SourceNormalizedFrame constructor and strict
   proof checks. Cutter transforms and the mounting planner
   remain unchanged because their coordinate contracts are separate.
3. The moving fixture's external placement becomes Y=drawer offset+11.5 and Z=23,
   yielding its intended physical Y=drawer offset and center Z=23 after the
   source's (-11.5,-1) displacement. Both hands retain the same interpretation.

4. The saved-project replay exposed the paired producer: the hardware renderer
   folded native source Location into the saved parent frame, after which physical
   rendering applied it again. Store the unchanged mounting plan directly and
   remove that redundant conversion plus its unused source-shape arguments.
   The saved custom-drawer proof retains this regression; old generated hardware
   specifications and their evidence need deliberate regeneration from the plan.

5. Final affected regression: 118 passed in 404.83 seconds across 23 test files.
   Independent review regenerated a saved drawer with exact manufacturer CAD;
   all 13 closed/open GLB bounds agree with reports within 0.001134 mm. Moving
   items translate exactly 500 mm while static items remain fixed. All eight
   1 mm hand/inset mutations reject; purchase identity and quantity stay fixed.
   Manufacturing authority remains false where screw/pilot evidence is missing.
   Evidence is preserved under ignored local-evidence/shared-construction-20260912.
