---
name: aikea-build-drawers
description: Build a complete drawer installation with compatible runners, mounting holes and any required hinge-clearance spacers. Use whenever an AIkea design contains drawers, including custom compositions, configurators, or changes to an existing drawer or its surrounding doors.
---

# AIkea build drawers

Every drawer must include its runners and mounting holes. Read and apply the
[complete installation contract](references/complete-drawer-installation.md)
before generating drawer parts. Include spacers automatically where door or hinge
intrusion obstructs installation or travel. Use compact purchased spacers or narrow
manufactured mounting strips/blocks with verified attachments; do not silently
replace them with full-height inset support panels. Follow the contract's compact
support and load checks before sizing the drawer. Missing source or fixing data starts
the [hardware recovery flow](../aikea-source-hardware-cad/references/resolve-missing-hardware.md);
pause only the dependent geometry while actively resolving the missing input.
A box-only prototype or a cabinet with the requested drawers omitted does not
satisfy this skill.

For a wooden drawer, capture the bottom in grooves in all four walls so joining
the walls retains it. Keep wall-connector pockets and tool access above the floor;
do not fasten this bottom with Cabineos or let it cover their openings. Apply the
shared captured-bottom construction in the MOVENTO panel route below. Other
runner routes still require their own compatible retention and machining proof;
a plain box-sizing result does not establish that construction.

Before any client-facing message, including progress commentary, read
[../aikea/references/client-conversation.md](../aikea/references/client-conversation.md)
completely and apply it throughout this stage.

Read [the manufacturing process](../aikea-design-furniture/references/manufacturing-process.md)
before placing the drawer or its runners. Include cabinet and drawer fixing holes
in the chosen-face plan alongside their existing joinery.

## Goal

Turn a drawer design inside an existing generated cabinet into a project-owned
child assembly. Resolve its wooden parts from the cabinet's real clear opening,
verify the selected purchased-hardware CAD, preserve every local-to-parent
frame, and prove the saved cabinet can be rebuilt before showing it in review.

Use the supplied implementation as the construction authority. The model chooses
the intended cabinet and drawer arrangement, runs the deterministic builders,
and discusses the physical result with the client. It does not recreate drawer
geometry from prose.

The sizing recipes are optional conveniences over shared construction. Read
[shared drawer construction](references/shared-drawer-construction.md) when
adapting their output or using a drawer in a custom parent. Generated child
builders use the same panel/operation protocol as other furniture. Respect the
remaining host-interface limits and keep unresolved construction explicit.
For an authored parent, declare its [drawer host](references/drawer-host-interface.md)
and use the same selected-runner generator. Read its supported face orientation
and remaining proof boundary before claiming that a custom installation is verified.

## Select the runner profile

For a custom four-sided drawer constrained to one broad CNC face per panel,
inspect the [MOVENTO panel installation candidate](references/movento-panel-installation.md).
Its shared installer adds wood, both runners, both clips and host preparation
together. It remains an engineering candidate with explicit source-fit and
qualification gaps; those must be resolved for normal completed-drawer delivery.
Do not mistake a panel helper or an unavailable complete route for an optional
drawer: keep every requested drawer in scope and repair/source its installation.

Preserve an exact runner choice already saved in the active project or stated by
the client. For a request for verified Hettich runners without a named product,
evaluate the registered KA 4532 Silent System article `9114276` with one exact
article `13952` spacer on each cabinet side. This paired option is usable only
when it fits the actual opening and its fixing blockers are resolved. Its length
and spacer width are not furniture defaults. Source a compatible exact option
when needed; do not silently substitute a different length or omit the runners.
Use KA 5332 only when the active project or client explicitly selects it.

For a 400 mm KA 4532 candidate, use the [exact article 9114274 source/profile
verification](references/hettich-ka-4532-400-hardware.md). This checks both hands
and the size-specific official fixing axes; continue through the complete
installation contract before generating or repeating a drawer.

## Use a drawer in an authored parent

For an authored or mixed tree, follow [the explicit host contract](references/drawer-host-interface.md)
and [shared project setup](../aikea-design-furniture/references/authored-assemblies.md).
Use the selected-runner generator with that parent's real ID and save the child
through the common feature manifest. Review its complete parent/root using
`build_furniture_design.py` and `generate_complete_assembly_review.py`, selecting
the registered drawer state from the returned feature selectors. These commands
do not require a legacy wardrobe arrangement. Keep the selected profile's source,
installation and movement proof requirements; for KA 4532 use the host-aware proof
command below with the actual parent ID. Generic visual states alone do not
substitute for a profile's manufacturing or full movement evidence.

The following run-wide command sequence applies to configured wardrobes. Its
source-CAD, purchase ownership and conflict-preservation rules also apply to the
authored-host route above.

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
   the box heights, resolve a floor-adjacent, closely stacked layout and its
   cap shelf first, derive the mounting positions, then use `DrawerStackHeightPlanner` to turn the available intervals
   into useful box capacity with a deliberate clear gap. Keep explicitly chosen
   heights unchanged.
4. Resolve the exact source STEP files named by the selected runner profile. If
   they are absent, load `$aikea-source-hardware-cad` and resume with the returned
   project-local `hardware_directory`. Before invoking a generator, also resolve
   its installation and pilot data under the complete installation contract.
   Source CAD alone is insufficient. The capability gaps below remain blockers
   even when a command can emit geometry. Once resolved, for MOVENTO run:

   `python <skill-directory>/scripts/generate_cabinet_drawer.py <project>/aikea.yaml --assembly <cabinet-id> --drawer <drawer-id> --bottom-height-mm <height-above-carcass-bottom> --hardware-directory <download-directory>`

   For KA 5332, save the visually approved result into the cabinet first:

   `python <skill-directory>/scripts/generate_hettich_ka_5332_cabinet_drawer.py <project>/aikea.yaml --assembly <cabinet-id> --drawer <drawer-id> --bottom-height-mm <height-above-carcass-bottom> --box-height-mm <height> --box-depth-mm <depth> --hardware-directory <hardware-directory>`

   Run the command once per requested drawer. A later call revises the named
   drawer while preserving the cabinet's other generated drawer children.

   Then review that saved child and its exact runner source:

   `python <aikea-review-unit-directory>/scripts/generate_hettich_ka_5332_prototype.py <project>/aikea.yaml --assembly <cabinet-id> --hardware-directory <hardware-directory> --output-directory <review-directory>`

   For KA 4532 with article 13952, the current command below is a hardware
   integration probe, not a complete drawer generator. Do not use it for normal
   drawer delivery until its missing fixing implementation is resolved:

   `python <skill-directory>/scripts/generate_hettich_ka_4532_spacer_cabinet_drawer.py <project>/aikea.yaml --assembly <cabinet-id> --drawer <drawer-id> --bottom-height-mm <height-above-carcass-bottom> --box-height-mm <height> --box-depth-mm <depth> --drawer-front-mm <drawer-front> --hardware-directory <hardware-directory>`

   Do not repeat an incomplete probe. This command preserves one unchanged spacer STEP on
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

   For a KA 4532 integration probe with article 13952, inspect the saved recursive
   `ka4532-spacer-movement-collision-check.json`: it must have no failed checks
   and must retain `manufacturing_authority: false`. Do not substitute the
   legacy position reports for this proof or treat its machining blocker as a
   requirement to invent missing fixing data.
8. Reconcile every drawer with its own runner set, required spacers and actual
   mounting cuts using the complete installation contract. Only then present the
   complete drawer and its next concrete visual decision. If blocked, explain the
   missing physical information and the exact action needed to resolve it.

## Current capability

The authored MOVENTO panel installer now provides a six-panel construction with
Cabineo joinery, locking pilots, rear-hook preparation and both host fixing
patterns. Its purchased runner and clip ownership is added in the same operation.
See its reference above for the exact source-fit and production limitations.

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

### Default frontage and vertical layout

Use one functional structural front wall as the visible drawer front. Maximize its width within the verified unobstructed travel opening while preserving the intended hinge layout and mounting pattern. Measure left/right obstruction deductions independently, then use the governing required clearance on both visible sides for centered, aligned fronts. Derive the runner-compatible box and necessary supports separately; do not automatically add a fascia or doubled front. Place the first drawer close above the cabinet floor, stack shallow drawers with small operating gaps, and cap every stack with a shelf. These are AIkea defaults unless the user explicitly requests an exception. Apply the detailed [frontage and compact-stack contract](references/complete-drawer-installation.md#frontage-and-compact-stacks) to geometry, joints, captured bottoms, machining and full travel.
