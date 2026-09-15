# Exact KA 4532 400 mm runner profile

## Scope
Qualify the unchanged Hettich 9114274 source and official 400 mm installation row, then add an exact-size member/profile verification slice. Preserve the existing Vilja project, its six requested drawers, captured 6 mm HDF bottom requirement and one broad CNC face per panel. No drawer geometry until real fixing, clearance and setup inputs are resolved. Parent owns sourcing documentation and presentation.

## Work packages
- [x] WP1: Verify the exact STEP/PDF sources and classify all four native members.
- [x] WP2: Derive installation datums and fixing axes from the official 400 mm row and exact source openings.
- [x] WP3: Add a narrowly scoped exact-size profile and source verification with targeted meaningful tests.
- [x] WP4: Review the slice, run bounded checks, commit locally and hand off a concrete route to one complete drawer.

## Current state
Fresh exact-source opening verification passes all 12 axes: fixed members at 37/165/229 mm from the cabinet front, moving members at 37/165/291 mm from the drawer front. The independently read 400 mm PDF row and native cylindrical boundaries agree at a +11.5 mm depth transform; native front -9.5 becomes the drawn 2 mm setback. First two moving fixings are the centres of vertical 4.4 x 4 slots; the last is round. All four native members are valid, uniquely classified and unchanged. A new exact-size manifest/profile/loader/opening checker is implemented; targeted tests passed: **9 passed in 8.24 s**, including the real source integration check and rejection of an incorrect 500 mm fixing axis.

The manufacturer specifies 12.7 mm (+0.8 mm) side spacing, 46 mm height, 404 mm minimum body depth, 35 kg load class and recommended drawer width no more than 550 mm. Native fixed-to-moving outside planes are 12.5 mm apart, so source/nominal contact allowance is still an installed-fit issue. Nominal product dimensions do not authorize scaling the source. The 500 mm runner and 486 mm spacer are excluded from the 416 mm cabinet.

No drawer parts or existing GLBs have been changed. Next construction evaluates separate lower runner-support strips: their outer-face pilots and Cabineos are separate from the upper walls' inner-face captured-floor grooves and joints. Front/back panels receive all wall/strip joints and floor grooves from their inner face. This must pass actual paired cuts, connectivity, hardware clearance and independent setup checks before repetition.

## Audit log
1. Parent relayed Patrick's explicit instruction to resume and resolve the drawer installation. Exact 400 mm source is newly supplied; previous download assumptions are superseded by the successful official browser retrieval.
2. This branch preserves the complete existing project and limits first implementation to exact article identity, member classification, datums, openings and verification. Installation/wood fabrication follows only after the real inputs and compatible single-face construction are established.

## Continued installation scope
- [ ] WP5: Resolve one complete drawer's screws/pilots, hinge clearance and real spacer/support attachment, using the exact 400 mm source.
- [ ] WP6: Prove all seven candidate wooden panels retain one CNC face and the 6 mm HDF is captured by four grooves; reject any unresolved physical conflict.
- [ ] WP7: Apply the full usable-height System 32 grid, resolve all lighting/joinery/hardware collisions, and reconcile actual rows.
- [ ] WP8: Repeat only a verified complete drawer to the retained 2/2/1/1 allocation; export and check actual current artifacts within the unchanged outside envelope.

3. Patrick explicitly resumed the full six-drawer objective. The source/profile slice remains a separate coherent checkpoint; then proceed to actual installations. Parent's System 32 policy at 9a926be is authoritative: full usable-height rows by default, with explicit overrides only. Existing short shelf groups do not fulfil it.
4. A conventional one-piece side requires inner grooves and outer runner pilots, which conflicts with one-face CNC. Evaluate real lower support strips rather than deleting operations or changing blind holes to through holes. The raised floor reduces usable capacity and must be accounted for. Stock, coating and existing nominal shelf/door allowances remain unqualified; do not invent replacement gaps.

Source/profile validation command: `direnv exec . env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 AIKEA_TEST_KA4532_400_SOURCE=local-evidence/project/hardware/hettich/ka-4532-silent-system/9114274/source python -m pytest tests/test_hettich_ka_4532_400_profile.py -q`. Actual source/opening report: `local-evidence/project/reviews/ka4532-400/source-opening-verification.json`; all twelve corridor intersection volumes are 0 mm³. Source hash remains unchanged. These are source/profile results, not installed drawer or fabrication proof.

5. Source/profile checkpoint is coherent and reviewed. The reusable verifier command passed against the real unchanged source; scope review found each new code file below 150 lines with one role. The consuming drawer skill now links its 400 mm reference and command. The existing 500 mm route and parent-owned sourcing docs are unchanged. Installation work remains active in WP5–WP8 after this checkpoint.
