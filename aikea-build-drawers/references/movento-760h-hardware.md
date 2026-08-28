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
bounds. It does not store Blum STEP bytes. The local resolver accepts either the
normalised AIkea filename or the unchanged official download filename. When both
exist, it admits only checksum-matching bytes and prefers the normalised name.

`HardwareStepImporter` preserves the STEP file exactly in its manufacturer frame:

- origin `(0, 0, 0)`;
- native X, Y, and Z axes unchanged;
- millimetres;
- no recentering;
- no scaling;
- no inferred mirroring.

The consistent imported wrapper is the normalised representation. Placement into
a drawer or cabinet is a later explicit rigid transform, not part of import.

`DrawerHardwareSetVerifier` admits a drawer generation only after the selected
profile's left and right runners and matching left and right locking devices all
prove build-ready state, identity, handedness, checksum, solid count, and native
bounds. Passing this gate means source CAD is verified but unplaced; it does not
prove installation, mating, or machining.

## Registered 500 mm pair

- The official 500 mm product download resolves to two verified local STEP
  files. Each file contains two solids and remains outside the public skill.
- The left asset embeds `760H5001S_L` and `T75S746M00_L`; its positive-X
  native frame also matches the verified `T51.7601 L` frame convention.
- The paired file embeds `760H5001S` and `T75S746M00` without an `R` suffix.
  Its right-handed ownership is therefore an explicit inference from the paired
  official download and its negative-X frame matching the verified
  `T51.7601 R` convention.
- Registration proves exact bytes, product identity, native bounds, and handed
  asset ownership. Cabinet placement, drawer mating, and mounting machining are
  separate unresolved gates.

## Unresolved CAD

- The downloaded 550 set candidate embeds `760H5501S` and represents only one
  handed runner. It is inspection-only until the matching handed component is
  identified.
- The 550 candidate must never stand in for the 500 runner and must never be
  shortened or scaled.
- If cabinet depth selects the 550 mm profile, generation stops until its own
  complete handed hardware set is registered. It does not fall back to 500 mm.

Official sources:

- [Blum Product Database](https://www.blum.com/us/en/services/e-services/productdatabase/)
- [MOVENTO catalogue page](https://publications.blum.com/2024/catalogue/en/504/)
