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
bounds. Passing this gate proves the source files only. The later hardware
position report proves their saved placement and reports machining still owed.

## Verified 500 mm mounting frame

The official attachment graphic and the native STEP features resolve one shared
manufacturer frame for both hands:

- native X maps to owner X;
- native Y maps to owner Z;
- native Z maps to negative owner Y;
- the manufacturer origin is 37 mm behind the wooden drawer front and 9.575 mm
  above the drawer side's lower edge;
- native X zero is the relevant inside cabinet-wall plane.

For a 15 mm drawer side, the `LW - 42` relationship leaves 6 mm between the
drawer outside and each cabinet wall. The left locking-device frame is therefore
6 mm left of the drawer zero; the right frame is 6 mm right of the drawer's
outside width. After the drawer frame is composed into the cabinet, each locking
device and its runner share the same manufacturer origin and axes.

The runner STEP contains the catalogue-matching system-screw axes at native Z
`0` and `-256`. They become fixing depths 37 and 293 mm from the wooden drawer
front. The 9.575 mm vertical translation places the T51 mounting pads on the
drawer's lower edge; adding another 0.2 mm causes material interference.

## Placed hardware proof

The review builder uses those saved frames without recentering either component.
The runners remain fixed to the cabinet while the locking devices inherit the
drawer pose. Before export, the hardware position report must prove:

- each runner meets its own inside cabinet face without entering the side panel;
- each locking device meets the wooden drawer front without entering it;
- the handed runner and locking device share their manufacturer origin and axes;
- no hardware enters unrelated cabinet or drawer material;
- any rear intrusion is contained within the lower drawer-back preparation that
  the manufacturer requires.

The current exact 500 mm proof passes those relationships. Its lower rear
intrusion remains explicit as required preparation rather than being accepted as
finished wood geometry.

## Static CAD and open review

The official left and right runner download records offer STEP, Parasolid,
Collada, and other static exchange formats. Inspection of the available STEP,
Parasolid, and Collada files found the same two flattened product bodies and no
kinematic joints or separately identified telescoping members. They therefore
prove closed geometry and placement, not internal runner movement.

Keep those exact files unchanged as the closed and removed-position authority.
The open visual review uses a separate movement preview derived only from facts
the saved frames establish: the cabinet-side path stays fixed, and the
drawer-side attachment plus locking device travel with the drawer. The preview
does not infer intermediate members, extension ratios, clearances, machining, or
toolpaths and is never manufacturing authority.

The resolved transform does not complete machining. The unmachined drawer back
still occupies the runner's required rear hook/notch space, and the official
rear preparation must be applied before manufacture. The manufacturer runner
and lock solids also overlap in their apparent closed engagement; do not move
one component merely to remove that vendor-CAD overlap without an installation
datum proving the change.

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
  asset ownership. The mounting profile separately owns placement; rear drawer
  preparation and mounting machining remain unresolved gates.

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
- [MOVENTO planning and attachment brochure](https://d2.blum.com/services/BEC003/me17392873_ep_dok_bau_%24sen-id_%24aof_%24v2.pdf)
