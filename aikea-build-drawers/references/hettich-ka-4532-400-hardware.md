# Exact KA 4532 Silent System 400 mm source

Article **9114274** has a checksum-gated source/profile route independent of the
500 mm runner and 486 mm spacer. Source the unchanged STEP through
`aikea-source-hardware-cad`; store it in
`hardware/hettich/ka-4532-silent-system/9114274/source/9114274.stp`.
The manifest is `assets/hettich/ka-4532-400/hardware-assets.json`.

Run the bounded source check before constructing its installation:

```sh
python <drawer-skill>/scripts/verify_hettich_ka_4532_400.py <source-directory> --output <project>/reviews/ka4532-400-source-check.json
```

`HettichKa4532FourHundredStepLoader` preserves the four exact native solids and
classifies both hands independently of import order. The opening checker verifies
all twelve axes against cylindrical source boundaries and unobstructed fixing
corridors. A wrong size, duplicate member, changed checksum or missing opening
fails before placement. No vendor CAD is distributed with the skill.

## Installation evidence

Use the 400 mm row on page 2 of [Hettich MS 10547.00.000](https://web2.hettich.com/hbh/addon/montage/MS_10547_00_Montageanleitung_KA4532-SiSy.pdf).
The fixed-member axes are 37, 165 and 229 mm from cabinet front; the moving-member
axes are 37, 165 and 291 mm from drawer front. The first two moving fixings use
the centres of vertical Ø4.4 x 4 slots, the last a round Ø4.4 opening. Fixed
openings are Ø6.4. These are hardware opening dimensions, **not wood pilot sizes**.
Native depth gains 11.5 mm to reach each front datum; native front -9.5 mm becomes
the drawn 2 mm setback. Never scale or trim the longer native bounding envelope.

The [official product](https://shop.hettich.com/us_EN/p/9114274) specifies a 400 mm
drawer, 404 mm minimum cabinet depth, 46 x 12.7 mm section and 35 kg load class.
The installation sheet gives +0.8 mm spacing tolerance and recommends drawer
width no more than 550 mm. It permits cabinet screws Ø6 x 14 or Ø4 x 14 and
moving-member screws Ø4 x 14. Select exact purchases and their material-specific
pilots before machining; these generic callouts do not approve a substitute screw.

## Continue to one complete drawer

This check proves source identity, member classification and drawing/opening
alignment. It is not a completed installation generator. Derive actual support
frames and door/hinge-clearance spacers, select screw/pilot inputs, and use common
panel construction for one complete drawer with its captured bottom and both
runner hands. Reconcile full cabinet grids and all panel setup faces before
repetition. Do not inherit the 500 mm profile's fixing positions, spacer or stock.

Native fixed-to-moving outer planes are 12.5 mm apart while installation spacing
is nominally 12.7 mm. Keep that source/contact allowance explicit; do not move or
rescale an individual member to silently erase it. Source contact, intermediate
stage representation, full travel, material engagement, load and machining
qualification remain separate installation gates.
