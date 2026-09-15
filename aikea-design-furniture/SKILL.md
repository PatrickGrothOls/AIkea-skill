---
name: aikea-design-furniture
description: Design and compose sheet-material furniture using shared construction tools and optional standard component configurators. Use for standard furniture, custom layouts, mixed assemblies, or adapting an existing design.
---

# Design and compose furniture

Use this construction protocol for both standard and custom designs. The model
owns requirements and arrangement; shared tools build and check the construction.
Cabinet, drawer and front configurators are editable shortcuts within that same
path. Furniture purpose describes the brief and never selects a private cutting
engine. A missing recipe does not mean the requested design is unsupported.

Read [the client conversation contract](../aikea/references/client-conversation.md)
for client-facing work. Reuse the active project's measurements and decisions.
Keep implementation details out of the customer conversation unless requested.

## Select the construction

Read [the manufacturing process](references/manufacturing-process.md) before
placing panels or joints. The standard process is three-axis CNC with one chosen
broad machining face per physical part and no flipping. Selected fixed structural
sheet connections use paired Cabineo/insert work. This constrains the arrangement,
including all hardware fixing holes.

For floor-standing cabinets, use the current Korrekt adjustable feet, deck and
front kickboard; there is no brace-base fallback. Read the [base recipe](../aikea-build-units/references/base-recipe.md)
and retain the required outside height when checking hardware/deck compatibility.
Ordinary storage shelves default to actual adjustable supports and matching bores.
Read the [storage-shelf policy](../aikea-build-units/references/storage-shelves.md);
record any fixed Cabineo shelf choice and keep its pockets on the hidden underside.
Structural cabinet floors/tops are separate. These defaults apply equally to
custom compositions and generated recipes.
Cabinet side panels also default to the [full System 32 grid](../aikea-build-units/references/panel-construction.md#machine-the-cabinet-hardware-grid).
Declare it before fitting shelves, hinges, runners and lighting. Omitting,
shortening or moving it requires a recorded design override with affected panels,
reason and replacement arrangement; custom composition alone is not an override.

Save the envelope, obstacles, chosen materials and functional requirements in the
active project. Preserve an existing `aikea.yaml`; use its wardrobe calculator
when that schema describes the arrangement. Custom compositions can retain their
own typed inputs and requirements without inventing cabinet counts to fit it.
Mark prototype assumptions as assumptions, not measurements or client approval.
Reuse confirmed material choices. For an unconfirmed choice or requested material
revision, load [$aikea-choose-materials](../aikea-choose-materials/SKILL.md) and use
its part-specific route for an authored composition. Apply a choice only within
the user's authorization; a prototype assumption remains a recorded proposal.

For an image-led brief, record the visible form, proportions, fronts, handles,
supports and edge treatments before choosing hidden construction. Perspective
does not supply measured dimensions, material identity or a joint specification.
Keep proposed dimensions and concealed details explicit, then compare the whole
generated object with the supplied reference during visual review.

Read the [construction tool map](references/construction-tools.md) and inspect the
relevant operations or [component interfaces](references/component-interfaces.md)
before authoring construction. Choose a standard configurator where its inputs
fit; adapt its explicit recipe or compose parts directly elsewhere. Both paths
use `PanelAssemblyBuilder`, `PanelMachiningFeature` and the same output checks.
Use [the project contract](references/authored-assemblies.md) for initialization,
ownership, evidence and full-tree review commands.

Give each manufactured piece a stable ID, material, blank dimensions and local
frame; give each purchased component its exact product and purchase identity.
Keep shared panels under one owner. Let a connection resolve both participants'
machining, and let a component own its purchases, host effects and review states.
Changing a name or purpose must not add or remove machining.

Whenever the design contains drawers, load
[$aikea-build-drawers](../aikea-build-drawers/SKILL.md) before generating them.
Its complete runner, mounting-hole and hinge-clearance spacer contract applies
equally to custom panel compositions and configurators. Resolve the installation
before sizing the box; unresolved hardware is not permission to deliver bare
drawer boxes and defer their holes to a later manufacturing stage.

Reuse existing standards and selected hardware within their supported interfaces.
New operations remain possible: first establish the missing capability, then use
the shared extension contract and independent checks on actual participants.
Do not recreate a known cutter in a design script, copy a frozen runtime, suppress
a failed check or label an unknown operation as a supported one. A valid solid
does not qualify a novel operation for fabrication.

## Review the complete design

Run the mandatory setup and connection checks in
[the manufacturing process](references/manufacturing-process.md) on the complete
current tree. A geometrically valid preview with missing holes or conflicting
entry faces is not a completed CNC design.

Build one complete tree, including configured components, custom parts and bought
hardware. Reconcile declared requirements with operations, actual physical items
and inventory. Preserve unresolved support, attachment, material, load and motion
questions explicitly; the checker cannot discover an unrecorded design obligation.

Use [the shared review and evidence path](../aikea-review-unit/references/construction-position.md)
for current geometry and bounded contact allowances. Show the real GLB with
[$aikea-review-unit](../aikea-review-unit/SKILL.md), including applicable moving
states. After changes, rebuild and invalidate affected evidence. A component probe
must return to the full parent before claiming the design works.

Use the existing visual-approval/repetition boundary and fabrication gate. Respect
the user's existing prototype or test authorization. Preview success does not
certify missing engineering work, vendor compatibility or machine setup.
