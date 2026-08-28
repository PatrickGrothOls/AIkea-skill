---
name: aikea-build-drawers
description: Add a calculated wooden drawer subassembly to an existing generated AIkea cabinet, select a depth-matched runner profile, save the drawer's local project files, and review that same built child in its cabinet and complete furniture run. Use when adding, checking, opening, or visually reviewing a drawer in an AIkea project.
---

# AIkea build drawers

## Goal

Turn a drawer design inside an existing generated cabinet into a project-owned
child assembly. Resolve its wooden parts from the cabinet's real clear opening,
select the longest registered runner that fits, preserve every local-to-parent
frame, and prove the closed drawer fits before showing an open review.

Use the supplied implementation as the construction authority. The model chooses
the intended cabinet and drawer arrangement, runs the deterministic builders,
and discusses the physical result with the client. It does not recreate drawer
geometry from prose.

## Build one verified drawer

1. Resolve the active AIkea project and require its completed `aikea.yaml` and
   generated `assemblies/` folders.
2. Read [references/drawer-construction.md](references/drawer-construction.md)
   and [references/movento-760h-hardware.md](references/movento-760h-hardware.md)
   completely.
3. Identify the existing cabinet that will own the drawer. Use a client-supplied
   position when one is part of the design; otherwise make one practical visual
   proposal inside that cabinet and let the client judge it in the model.
4. Run:

   `python <skill-directory>/scripts/generate_cabinet_drawer.py <project>/aikea.yaml --assembly <cabinet-id> --drawer <drawer-id> --bottom-height-mm <height-above-carcass-bottom>`

5. Treat the generated cabinet-local files as the source for this drawer. The
   composed cabinet builder must load the original cabinet builder and its saved
   drawer child rather than reconstructing either assembly. Later proposals may
   regenerate files still owned by AIkea, while a locally changed file stops the
   complete revision for client review.
6. Run:

   `python <aikea-review-unit-directory>/scripts/generate_drawer_wardrobe_review.py <project>/aikea.yaml --assembly <cabinet-id> --drawer-state open`

7. Require both the drawer position report and the complete wardrobe position
   report to pass. Present the close-up first, then the complete furniture run
   containing that same composed cabinet.
8. Explain the useful physical result in client-facing language and end with one
   concrete visual decision about the drawer's size or position.

## Current capability

The implemented slice builds one five-panel wooden drawer in one existing
cabinet, records the selected MOVENTO runner and locking-device identities, saves
the cabinet-to-drawer frame, checks clearances and material collisions, and
exports closed/open review geometry. Exact hardware CAD, mounting cuts,
drawer-box joinery, and manufacturing toolpaths remain later construction gates
and are reported separately from this visual box-and-placement proof.

## Responsibility boundary

This skill owns drawer-local calculation, child-folder generation, hardware
profile selection, and the drawer-to-cabinet fit gate. The existing cabinet owns
the fixed runner installation; the drawer child owns the moving wooden box and
its moving locking devices.
`$aikea-review-unit` owns presentation and global placement, while the overall
`aikea.yaml` remains unchanged because drawer arrangement is local to its cabinet.
