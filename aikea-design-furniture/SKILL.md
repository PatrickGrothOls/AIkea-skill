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

Save the envelope, obstacles, chosen materials and functional requirements in the
active project. Preserve an existing `aikea.yaml`; use its wardrobe calculator
when that schema describes the arrangement. Custom compositions can retain their
own typed inputs and requirements without inventing cabinet counts to fit it.
Mark prototype assumptions as assumptions, not measurements or client approval.
Reuse confirmed material choices. For an unconfirmed choice or requested material
revision, load [$aikea-choose-materials](../aikea-choose-materials/SKILL.md) and use
its part-specific route for an authored composition. Apply a choice only within
the user's authorization; a prototype assumption remains a recorded proposal.

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

Reuse existing standards and selected hardware within their supported interfaces.
New operations remain possible: first establish the missing capability, then use
the shared extension contract and independent checks on actual participants.
Do not recreate a known cutter in a design script, copy a frozen runtime, suppress
a failed check or label an unknown operation as a supported one. A valid solid
does not qualify a novel operation for fabrication.

## Review the complete design

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
