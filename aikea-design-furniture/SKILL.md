---
name: aikea-design-furniture
description: Design sheet-material furniture from an envelope and functional requirements by composing panels, joints, nested assemblies and purchased hardware. Use for new furniture, mixed layouts, or designs that do not match an existing cabinet template.
---

# Design furniture from construction tools

The model owns the design: translate the client's envelope and requirements into
parts, connections and working mechanisms. Tools calculate and build that design.
A purpose such as bench, side-opening cupboard or stepped shelving is a description,
not a key that must exist in a furniture catalogue.

Read [the client conversation contract](../aikea/references/client-conversation.md)
for client-facing work. Use only this project's measurements and decisions.

## Lead the design

- Establish the usable envelope, obstacles and a few functional requirements.
  Reuse supplied facts. Make ordinary construction decisions yourself; record
  assumptions and ask only when an unresolved choice materially changes the result.
  Honour explicit permission to assume for a prototype. Assumptions are not site
  measurements, customer approval, or evidence of load capacity.
- Save those facts and a requirement-to-part checklist in the active project.
  Preserve an existing `aikea.yaml`; a new composition does not need fictitious
  cabinet counts, doors or plinth settings just to enter a template calculator.
- Design the whole arrangement: partition its space, define owned assemblies,
  and derive every part dimension and placement from current inputs. Share
  partitions where appropriate. Account for thickness, access, movement,
  fastening, support and assembly order. Keep decisions in local specifications,
  rather than hiding independent dimensions in rendering code.
- Select materials and real hardware that suit those requirements. Use
  `$aikea-choose-materials` for material advice and `$aikea-source-hardware-cad`
  for discovery and exact sources. Keep local material records when a design's
  parts do not fit the legacy cabinet-wide material groups.

## Compose and build

Read [the construction tool map](references/construction-tools.md), then
[the authored assembly contract](references/authored-assemblies.md).

Initialise shared project contracts and author executable local specifications
and builders. Reuse the existing geometric and machining tools. Give each part
an explicit manufacturing frame and each child an explicit parent placement.
Represent joints once and resolve work for both participants from that joint.
Semantic labels must never silently choose geometry or drill holes.

Existing cabinet, drawer, door and lighting builders are useful components when
their real interfaces fit. Adapt a feature's owning panels and clear space to its
contract; do not pretend an arbitrary assembly is a standard cabinet. Reuse exact
hardware and machining plans in the final assembly tree.

If a needed operation is absent, inspect related tools and manufacturer evidence,
then implement the smallest coherent operation or project-local builder and test
it on its actual participants. A new furniture purpose does not require a new
purpose registration. A genuinely missing machining or hardware operation does
require implementation and verification; prose and placeholder solids do not
substitute for it. Keep reusable operations free of dimensions from this project.

## Check the complete result

Build the complete intended assembly tree and run the envelope and exact-solid
checks. Use failed checks to revise the design and rebuild affected parts. An
isolated probe can diagnose a problem; return its result to the main design.

Check each requirement against the actual output, including every requested
feature, access, support, fasteners and motions. Closed geometry checks establish
neither mechanical strength nor hardware suitability. Check moving mechanisms
in relevant positions and the shared assembly, using exact purchased geometry.
Keep unresolved evidence visible without marking the result fabrication-ready.

Open the real result with `$aikea-review-unit`. Show the overall arrangement and
the relevant detailed views. A visual prototype may contain explicitly marked
unfinished mechanisms, but do not call it a complete construction. Obtain visual
approval before repeating finished detailed construction or releasing fabrication
outputs; use the user's existing prototype/test authorisation for exploratory work.
