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
3. Resolve the complete hardware set owned by that exact runner profile. Verify
   every handed file, paired assembly, and companion component required by that
   profile in its unchanged manufacturer frame before producing drawer files.
4. Convert the sourced runner profile into generic box-sizing values.
5. Build every wooden sheet through `BlankSheetBuilder` in its canonical part
   frame and place it through `DrawerPartLocator`.
6. Save the drawer child, its explicit cabinet-local placement, and the resolved
   source-CAD mounting frames.
7. Build the composed cabinet, check the closed drawer, and write the position
   report before applying an open review pose.
8. Use the source CAD's actual member structure when it is available. Keep
   cabinet members fixed, let drawer members inherit drawer travel, and move any
   intermediate members only through the selected runner's saved review model.
9. When a source file has no articulated members, keep its static geometry as
   the closed-position authority and label any open movement preview separately.
10. In the removed view, leave every cabinet-owned source member in place so its
    saved installation can be inspected directly.

## Drawer box panel relationship

The front and back panels span the complete outside width of the drawer. The
left and right side panels fit between their inner faces. Keep the purchased
runner profile's calculated side-panel length unchanged; derive the complete
outside depth by adding the front and back thicknesses. The bottom fills the
clear opening between all four walls. Use `DrawerBoxPlanner` and
`DrawerPartLocator` as the construction authority rather than recreating these
relationships in project builders.

## Vertical drawer density

Resolve the runner rows and the upper boundary of the intended drawer zone before
choosing automatic box heights. Pass those physical positions to
`DrawerStackHeightPlanner`; its result is the construction value. It fills each
available interval while retaining the chosen clear gap, can equalize a matching
set when the design calls for it, and reports the actual remaining space above
every box. A client-fixed height remains fixed and its resulting gap stays visible
for review.

Use the calculated height in each saved drawer child and show the resulting stack
before repeating it. The model should choose the desired visual or hand clearance
with the client, not recreate the spacing arithmetic in conversation.

## Required evidence

The drawer proof is valid when the chosen runner depth fits, the complete closed
box remains inside the cabinet opening, no drawer sheet occupies cabinet material,
all three saved child axes form the frame used by CadQuery, and the same composed
cabinet appears in both close-up and full-run exports. The generation gate must
also prove the exact selected source-CAD set before any project drawer file is
written. The open review additionally requires a passing movement report whose
preview geometry is explicitly excluded from manufacturing authority.

Purchased hardware uses the manifest owned by its selected profile. A verified
local STEP is imported without scaling, recentering, mirroring, or changing its
native manufacturer frame; its later rigid placement is a separate saved
transform.
