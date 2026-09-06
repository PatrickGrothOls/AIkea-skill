---
name: aikea-choose-materials
description: Advise on and confirm materials for an AIkea cabinet or fitted-furniture project using current local pricing, appearance, durability, construction quality, and fabrication constraints. Use when choosing or comparing carcass, shelf, door, or back-panel materials; when a client asks what material is best; or before AIkea asks for panel thicknesses without an approved material choice.
---

# AIkea choose materials

Before any client-facing message, including progress commentary, read
[../aikea/references/client-conversation.md](../aikea/references/client-conversation.md)
and [references/material-selection.md](references/material-selection.md) completely.

## Goal

Help the client choose a buildable material system whose real appearance, total
cost, and service quality fit this project. Treat carcasses and shelves, doors,
back panels, and exceptional wet or high-wear parts as separate groups;
combine groups only when the same construction genuinely suits them. The current
global specification can represent one thickness for all carcass and shelf
panels, one for doors, and one for back panels. Treat any requirement
outside those groups as unresolved construction work, not an implemented choice.

## Establish the decision

1. Resolve the active project and read its `aikea.yaml` when present. Preserve
   all confirmed project facts and never import choices or prices from another
   project.
2. Reuse the room, furniture purpose, dimensions, finish intent, location,
   currency, budget, and fabrication constraints already supplied.
3. Follow the reference's intake, inference, appearance, source-trust, comparison,
   and persistence method. Ask one ordinary-language question only when its answer
   can change the shortlist; infer technical requirements from documented project
   facts instead of asking the client for engineering values.

## Research and compare

1. Compare no more than three current, locally purchasable material systems using
   supplier evidence for price and availability and manufacturer evidence for
   physical claims.
2. Present one recommendation and one runner-up. Make the installed-cost basis,
   appearance, quality consequences, decisive trade-off, sources, and remaining
   unknowns clear.

## Confirm and save

1. Treat the material stage as complete only when the carcass and shelves,
   doors, and back panels each have a confirmed `design_decisions` entry
   and no `unresolved_material_requirement` is blocked. Numeric thicknesses alone
   are legacy inputs, not evidence of material approval.
2. Present the recommendation as a proposal and ask one concrete confirmation
   question. Do not write the choice as approved before the client confirms it.
3. Keep dated comparison evidence in
   `<project>/materials/material-comparison.md`; this research record is not the
   global design authority.
4. When no generated parts or review or fabrication evidence exists, update the
   existing `aikea.yaml` without adding schema fields: record one
   `design_decisions` entry per representable material group and set each numeric
   thickness only in its dedicated cabinet, door, or back-panel field.
5. If the project already has generated downstream artifacts and complete
   material decisions, do not change its approved material decision or
   `aikea.yaml`. Save the new choice as a proposal only and explain that a
   revision workflow must invalidate and regenerate the affected artifacts
   before the material can change safely.
6. If generated artifacts exist but the three required material decisions are
   absent, stop with a material-migration blocker. Do not mutate `aikea.yaml`,
   report the material stage complete, or return to `$aikea`; doing so would loop
   or bless evidence generated without explicit material authority.
7. If an exceptional part needs a material or thickness the global groups cannot
   represent, preserve the build-blocking requirement using the reference's
   stable marker. Do not claim that the current construction will generate it.
8. If only a material family is confirmed, say that exact product sourcing is
   still open. Do not claim fabrication readiness until every manufactured part
   receives a verified material identity in the manufacturing records.
9. Return to `$aikea` only after the stage is complete. It resumes the first
   unfinished global choice and runs its
   calculator only after the complete specification is valid.

## Responsibility boundary

This skill owns material advice, evidence, and the client's confirmed material
decision. `$aikea` owns global dimensions, `$aikea-build-units` owns part geometry
and construction, `$aikea-build-drawers` owns drawer-box and drawer-front
materials, and fabrication records own the exact material identity for each
manufactured part. Never apply the global door choice to drawer fronts
implicitly.
