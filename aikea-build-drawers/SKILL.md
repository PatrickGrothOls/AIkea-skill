---
name: aikea-build-drawers
description: Add a calculated wooden drawer subassembly to an existing generated AIkea cabinet, select a depth-matched runner profile, save the drawer's local project files, and review that same built child in its cabinet and complete furniture run. Use when adding, checking, opening, or visually reviewing a drawer in an AIkea project.
---

# AIkea build drawers

## Goal

Turn a drawer design inside an existing generated cabinet into a project-owned
child assembly. Resolve its wooden parts from the cabinet's real clear opening,
verify the selected purchased-hardware CAD, preserve every local-to-parent
frame, and prove the saved cabinet can be rebuilt before showing it in review.

Use the supplied implementation as the construction authority. The model chooses
the intended cabinet and drawer arrangement, runs the deterministic builders,
and discusses the physical result with the client. It does not recreate drawer
geometry from prose.

## Build drawer children from verified source CAD

1. Resolve the active AIkea project and require its completed `aikea.yaml` and
   generated `assemblies/` folders.
2. Read [references/drawer-construction.md](references/drawer-construction.md)
   completely. For MOVENTO, also read
   [references/movento-760h-hardware.md](references/movento-760h-hardware.md).
   For Hettich KA 5332, instead read
   [references/hettich-ka-5332-hardware.md](references/hettich-ka-5332-hardware.md).
3. Identify the existing cabinet that will own each drawer. Resolve every
   drawer as an independent child with its own height, depth, vertical position,
   runner selection, and review pose. Repeating a drawer is ordinary collection
   composition; it is not a separate stack design.
4. Resolve the exact source STEP files named by the selected runner profile. If
   they are absent, load `$aikea-source-hardware-cad` and resume with the returned
   project-local `hardware_directory`. For the implemented MOVENTO generator, run:

   `python <skill-directory>/scripts/generate_cabinet_drawer.py <project>/aikea.yaml --assembly <cabinet-id> --drawer <drawer-id> --bottom-height-mm <height-above-carcass-bottom> --hardware-directory <download-directory>`

   For KA 5332, save the visually approved result into the cabinet first:

   `python <skill-directory>/scripts/generate_hettich_ka_5332_cabinet_drawer.py <project>/aikea.yaml --assembly <cabinet-id> --drawer <drawer-id> --bottom-height-mm <height-above-carcass-bottom> --box-height-mm <height> --box-depth-mm <depth> --hardware-directory <hardware-directory>`

   Run the command once per requested drawer. A later call revises the named
   drawer while preserving the cabinet's other generated drawer children.

   Then review that saved child and its exact runner source:

   `python <aikea-review-unit-directory>/scripts/generate_hettich_ka_5332_prototype.py <project>/aikea.yaml --assembly <cabinet-id> --hardware-directory <hardware-directory> --output-directory <review-directory>`

5. Treat the generated cabinet-local files as the source for this drawer. The
   composed cabinet builder must load the original cabinet builder and its saved
   drawer child rather than reconstructing either assembly. Later proposals may
   regenerate files still owned by AIkea, while a locally changed file stops the
   complete revision for client review.
   Require the resolved runner center to occupy a real shared System 32 row and
   save its cabinet and drawer machining plus physical hardware reservation with
   the generated child.
6. Run:

   `python <aikea-review-unit-directory>/scripts/generate_drawer_wardrobe_review.py <project>/aikea.yaml --assembly <cabinet-id> --drawer-state open --hardware-directory <download-directory>`

7. Require both the drawer position report and the complete wardrobe position
   report to pass. Present the close-up first, then the complete furniture run
   containing that same composed cabinet. Use closed, open, and removed review
   states when the client needs to compare the fitted box, its movement, and the
   cabinet-owned runner locations. Require the runner movement report when the
   drawer is shown open.
8. Explain the useful physical result in client-facing language and end with one
   concrete visual decision about the drawer's size or position.

## Current capability

The implemented KA 5332 slice composes any number of independently sized and
positioned five-panel drawer children beneath an existing cabinet. Each drawer
owns one purchased runner pair, both source-side member placements, and its
cabinet-local frame. Review can assign a different extension to every child
while the closed collection remains the fit authority. Depth selection accepts
only a registered exact runner length with verified source CAD; the current
public profile is the approved 500 mm article. Its resolved System 32 node,
five cabinet-side fixings, five drawer-side pilots, and full installed envelope
are now produced and checked on both hands. Drawer-box joinery and manufacturing
toolpaths remain later construction gates.

## Responsibility boundary

This skill owns drawer-local calculation, child-folder generation, hardware
profile selection, and the drawer-to-cabinet fit gate. The existing cabinet owns
the purchased runner system; the drawer child owns the moving wooden box. A
runner system's saved member placements define how its purchased components
follow those two assemblies. The shared cabinet hardware map prevents a runner,
hinge plate, shelf, or later fitting from occupying the same fixing node or
physical panel space.
`$aikea-review-unit` owns presentation and global placement, while the overall
`aikea.yaml` remains unchanged because drawer arrangement is local to its cabinet.
