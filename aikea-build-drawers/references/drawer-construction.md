# Drawer construction

Use this reference for the saved files, coordinate frames, and proof sequence of
one AIkea drawer child.

## Project ownership

The existing cabinet remains the parent assembly and keeps its original builder.
The drawer generator adds:

```text
assemblies/<cabinet-id>/
├── drawer-layout.yaml
├── drawer_installation.py
├── with_drawers_builder.py
└── drawers/
    └── <drawer-id>/
        ├── spec.py
        └── builder.py
```

`drawer-layout.yaml` records the local design and selected hardware identity.
The drawer spec owns its calculated box and parts. The composed parent builder
returns the original cabinet plus a declared and built child assembly.
`drawers/generated-files.json` records the last AIkea-owned drawer result so a
later proposal can revise untouched files without claiming locally edited work.

## Coordinate chain

- Project zero: measured-space front-left floor point; X right, Y back, Z up.
- Cabinet zero: cabinet lower-front-left floor point in the project.
- Drawer zero: lower-front-left outside corner of the closed wooden box; X right,
  Y back, Z up.
- Part zero: each rectangular blank's canonical lower-left manufacturing origin,
  with thickness along its positive local Z before placement.

The saved drawer origin and all three axes map drawer coordinates into the cabinet.
The cabinet's existing project placement then maps that result into the measured
space. Position evidence must report both mappings from the placed CadQuery
geometry.

## Physical sequence

1. Read the cabinet's clear width, inside depth, panel thicknesses, shelves, and
   top boundary from its generated local specification.
2. Select the longest registered runner whose complete required depth fits.
3. Convert the sourced runner profile into generic box-sizing values.
4. Build every wooden sheet through `BlankSheetBuilder` in its canonical part
   frame and place it through `DrawerPartLocator`.
5. Save the drawer child and its explicit cabinet-local placement.
6. Build the composed cabinet, check the closed drawer, and write the position
   report before applying an open review pose.
7. Move only drawer-owned review geometry along the drawer's local opening axis.
   Cabinet-owned runner hardware remains fixed, while drawer-owned locking
   devices move with the box when their verified CAD is added.

## Required evidence

The drawer proof is valid when the chosen runner depth fits, the complete closed
box remains inside the cabinet opening, no drawer sheet occupies cabinet material,
all three saved child axes form the frame used by CadQuery, and the same composed
cabinet appears in both close-up and full-run exports.

Purchased hardware uses the manifest in `assets/blum/movento/`. A verified local
STEP is imported without scaling, recentering, mirroring, or changing its native
manufacturer frame; its later rigid placement is a separate saved transform.
