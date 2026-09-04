---
name: aikea-build-drawers
description: Add a calculated wooden drawer subassembly to an existing generated AIkea cabinet, select a depth-matched runner profile, save the drawer's local project files, and review that same built child in its cabinet and complete furniture run. Use when adding, checking, opening, or visually reviewing a drawer in an AIkea project.
---

# AIkea build drawers

Before any client-facing message, including progress commentary, read
[../aikea/references/client-conversation.md](../aikea/references/client-conversation.md)
completely and apply it throughout this stage.

## Goal

Turn a drawer design inside an existing generated cabinet into a project-owned
child assembly. Resolve its wooden parts from the cabinet's real clear opening,
verify the selected purchased-hardware CAD, preserve every local-to-parent
frame, and prove the saved cabinet can be rebuilt before showing it in review.

Use the supplied implementation as the construction authority. The model chooses
the intended cabinet and drawer arrangement, runs the deterministic builders,
and discusses the physical result with the client. It does not recreate drawer
geometry from prose.

## Select the runner profile

Preserve an exact runner choice already saved in the active project or stated by
the client. Otherwise, when the client asks for verified Hettich runners without
naming a product, select Hettich KA 4532 Silent System article `9114276` together
with one exact purchased article `13952` spacer on each cabinet side. Do not fall
back to KA 5332 merely because it was implemented earlier. Use KA 5332 only when
the active project or client explicitly selects it.

## Build drawer children from verified source CAD

1. Resolve the active AIkea project and require its completed `aikea.yaml` and
   generated `assemblies/` folders.
2. Read [references/drawer-construction.md](references/drawer-construction.md)
   completely. For MOVENTO, also read
   [references/movento-760h-hardware.md](references/movento-760h-hardware.md).
   For Hettich KA 5332, instead read
   [references/hettich-ka-5332-hardware.md](references/hettich-ka-5332-hardware.md).
   For Hettich KA 4532 mounted on the approved spacer profile, instead read
   [references/hettich-ka-4532-spacer-hardware.md](references/hettich-ka-4532-spacer-hardware.md).
3. Identify the existing cabinet that will own each drawer. Resolve every
   drawer as an independent child with its own height, depth, vertical position,
   runner selection, and review pose. Repeating a drawer is ordinary collection
   composition; it is not a separate stack design. When the client has not fixed
   the box heights, resolve the mounting rows and the drawer stack's upper
   boundary, then use `DrawerStackHeightPlanner` to turn the available intervals
   into useful box capacity with a deliberate clear gap. Keep explicitly chosen
   heights unchanged.
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

   For KA 4532 with article 13952, generate only the first requested drawer:

   `python <skill-directory>/scripts/generate_hettich_ka_4532_spacer_cabinet_drawer.py <project>/aikea.yaml --assembly <cabinet-id> --drawer <drawer-id> --bottom-height-mm <height-above-carcass-bottom> --box-height-mm <height> --box-depth-mm <depth> --drawer-front-mm <drawer-front> --hardware-directory <hardware-directory>`

   Do not repeat it yet. This command preserves one unchanged spacer STEP on
   each cabinet side, verifies the official rail axes against both purchased
   STEPs, and records only the unresolved longer screw and cabinet pilot.

5. Treat the generated cabinet-local files as the source for this drawer. The
   composed cabinet builder must load the original cabinet builder and its saved
   drawer child rather than reconstructing either assembly. Later proposals may
   regenerate files still owned by AIkea, while a locally changed file stops the
   complete revision for client review.
   For MOVENTO and KA 5332, require the resolved runner center to occupy a real
   shared System 32 row and save its cabinet and drawer machining plus physical
   hardware reservation with the generated child. For KA 4532 with article
   13952, require both panel reservations, the four official fixed-member axes,
   exact-CAD evidence that every axis crosses the spacer's solid centre web, and
   the remaining screw-and-pilot blocker. Do not select the spacer's separate
   preformed openings or infer a fastener or pilot.
6. For MOVENTO and KA 5332, run:

   `python <aikea-review-unit-directory>/scripts/generate_drawer_wardrobe_review.py <project>/aikea.yaml --assembly <cabinet-id> --drawer-state open --hardware-directory <download-directory>`

   For KA 4532 with article 13952, instead run:

   `python <aikea-review-unit-directory>/scripts/generate_hettich_ka_4532_spacer_proof.py <project>/aikea.yaml --assembly <cabinet-id> --output-directory <review-directory>`

   When the cabinet has a fitted door, append
   `--state <cabinet-id>/door_hinges=open` so the door is held open in both
   compared drawer states.

7. For MOVENTO and KA 5332, require both the drawer position report and the
   complete wardrobe position report to pass. Present the close-up first, then
   the complete furniture run containing that same composed cabinet. Use closed,
   open, and removed review states when needed, and require the runner movement
   report when the drawer is shown open.

   For KA 4532 with article 13952, require only the saved recursive
   `ka4532-spacer-movement-collision-check.json`: it must have no failed checks
   and must retain `manufacturing_authority: false`. Do not substitute the
   legacy position reports for this proof or treat its machining blocker as a
   requirement to invent missing fixing data.
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

The exact KA 4532 article `9114276` and Hettich spacer article `13952` are
registered together as a paired hardware option. The single-drawer generator
checksum-gates their project-local STEP files, classifies every runner member,
places the same unchanged spacer solid on both cabinet sides, and saves exact
hardware ownership and panel reservations. Recursive review now checks closed
and open movement, exact endpoint intersections, and conservative linear swept
envelopes. The official 37, 165, 261, and 325 mm cabinet fixing axes are checked
against the exact runner openings and the exact spacer's complete 25 mm support
corridors on both hands. Repetition and fabrication readiness remain blocked
until one complete cabinet passes and an approved longer screw plus
cabinet-material pilot diameter and depth are supplied.

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
