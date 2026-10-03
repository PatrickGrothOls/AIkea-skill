# Presentation bake validation

## Scope

Diagnose the fresh Claude desktop run's black cabinet and close the bake
acceptance gap without changing the user's birch choice or CAD geometry.
Track the separately reported hanging rail, index overflow and open-hinge
identity failures without declaring the incomplete cabinet delivered.

## Current state

Read the completed Claude task and its downloaded project archive. The saved
material remains birch plywood. Claude reports a completely black atlas despite
PASS evidence; current code checks UV coverage and geometry but not illumination.
Hanging rails have no source/profile/installation recipe in the package.
The black-bake cause is reproduced: CadQuery omits metallicFactor, Blender imports
1.0, and a diffuse-only bake has zero signal. Identified CAD panels now receive
an explicit nonmetal default while preserving declared materials and hardware.
The bake and viewer require a fifth report, lighting-signal.json.
38 targeted tests pass. A real Blender 5.2.1 test lit the fixed CAD panel with
unchanged geometry and rejected the reproduced fully metallic empty bake.

## Work packages

- [x] Read the actual run, saved brief and package paths.
- [x] Reproduce the black bake on a small CAD-exported panel.
- [x] Correct the cause and require illumination evidence before viewer delivery.
- [x] Test failed/black reports and a real Blender bake; review and commit.
- [ ] Separate follow-up: geometry indices exceeding uint16 range.
- [ ] Separate follow-up: identity on alternate door-state hardware.
- [ ] Separate follow-up: source a hanging rail and its real mounting recipe.

## Audit log

- 2026-09-21: User reports the fresh Claude result is black and lacks hanging
  rails. Inspection confirms the stored selection is still birch. Treat this as
  a presentation defect, not permission to change finish or conceal missing work.
  Preserve the uncoached run as evidence and fix reusable package behavior.
- 2026-09-21: Native Blender import independently confirms metallic=1 for the
  unchanged CAD export. The corrected export gives metallic=0 for identified
  panels only; shared hardware keeps its original materials and binary geometry.
  Existing explicitly declared metalness is preserved. Signal validation samples
  actual triangle centroids, permits unlit hidden faces and rejects globally empty
  or nonfinite results. It is not a lighting-quality or photometric certificate.
- 2026-09-21: Real tiny-fixture acceptance: nonmetal maximum luminance 0.9731,
  10/12 lit triangle samples, zero geometry error; metallic maximum 0.0, 0/12
  lit samples, rejected before presentation summary. Evidence retained locally in
  local-evidence/claude-bake-failure/acceptance-01. This does not validate the full
  delivered cabinet, which still needs rebuilding after other reported defects.
- 2026-09-21: Hanging rail sourcing is viable: Hettich oval 30 x 15 mm rail
  9000894 and SL 322 support 70664 have official product/CAD pages. The support
  specifies three screw holes, 32 mm spacing and rail length = clear width - 7 mm.
  Exact CAD, all fixing datums, screw engagement and load still need integration;
  a generic tube or a product link alone does not complete a hanging compartment.
  Sources: [SL 322 support](https://shop.hettich.com/gb_EN/Further-products/Interior-Fittings/Wardrobe-interior-organisation/Oval-wardrobe-rails-and-wardrobe-rail-supports/Wardrobe-rail-supports/SL-322-wardrobe-rail-support/p/70664)
  and [oval rail](https://shop.hettich.com/de_EN/Further-products/Interior-Fittings/Wardrobe-interior-organisation/Oval-wardrobe-rails-and-wardrobe-rail-supports/Cabinet-rails/Wardrobe-rails%2C-oval%2C-30-x-15-mm%2C-5000-mm%2C-matt-nickel-plated/p/9000894).
- 2026-09-21: Final data-flow and compatibility review completed. Existing explicit
  metalness remains byte-for-byte unchanged in the JSON document. Placeholder
  material changes preserve geometry buffers and do not change shared hardware.
  Viewer tests reject old/missing/failed lighting evidence. All 11 skill links
  validate. No runtime files or manufacturer CAD are committed. This branch is
  not merged or published and has not been injected into the uncoached Claude run.
