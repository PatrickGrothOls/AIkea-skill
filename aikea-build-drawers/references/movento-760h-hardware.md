# MOVENTO 760H planning and local CAD

Use this reference when selecting a MOVENTO runner or resolving its user-supplied
STEP geometry. The manifest at
`assets/blum/movento/hardware-assets.json` is the machine-readable source.

## Planning facts

- `760H5000S`: 500 mm, 40 kg, BLUMOTION S, Blum item `05083446`.
- `760H5500S`: 550 mm, 40 kg, BLUMOTION S, Blum item `07086828`.
- Drawer inside width: cabinet clear width minus 42 mm, with +0/-1.5 mm tolerance.
- Drawer side length: nominal runner length minus 10 mm.
- Drawer side thickness: at most 16 mm.
- Drawer-bottom underside recess: 12-15 mm.
- Minimum ordinary cabinet inside depth: nominal runner length plus 3 mm.
- With an inner wooden front of thickness `X`: nominal length plus `X` plus 3 mm.
- The 500 mm runner has 21 mm mounting width, 28.5 mm bearing height, and
  40.9 mm cabinet-profile width.
- Matching locking devices: `T51.7601 L` and `T51.7601 R`.

The registered catalogue selects the longest runner whose required depth fits.
For example, 564 mm inside depth with a 15 mm inner front requires 518 mm for
the 500 runner; the 550 runner would require 568 mm and therefore does not fit.

## Local CAD boundary

The package stores product identity, source links, checksums, and observed native
bounds. It does not store Blum STEP bytes. Resolve a file supplied by the user,
then verify it through `HardwareAssetResolver` before importing it.

`HardwareStepImporter` preserves the STEP file exactly in its manufacturer frame:

- origin `(0, 0, 0)`;
- native X, Y, and Z axes unchanged;
- millimetres;
- no recentering;
- no scaling;
- no inferred mirroring.

The consistent imported wrapper is the normalised representation. Placement into
a drawer or cabinet is a later explicit rigid transform, not part of import.

## Unresolved CAD

- The 500 mm runner STEP has not yet been obtained or verified.
- The downloaded 550 set candidate embeds `760H5501S` and represents only one
  handed runner. It is inspection-only until the matching handed component is
  identified.
- The 550 candidate must never stand in for the 500 runner and must never be
  shortened or scaled.

Official sources:

- [Blum Product Database](https://www.blum.com/us/en/services/e-services/productdatabase/)
- [MOVENTO catalogue page](https://publications.blum.com/2024/catalogue/en/504/)
