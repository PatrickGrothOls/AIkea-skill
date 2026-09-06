# AIkea architecture

This document records the reusable construction and conversation contracts.
It contains no active client project or local development handover.

### Overall philosophy

AIkea should feel like an experienced carpenter taking responsibility for a
layperson's furniture project. The client supplies the measured space and the
visible choices that genuinely belong to them. AIkea turns those facts into a
coherent, adjustable, manufacturable design and leads continuously to the next
useful result.

The model is the orchestrator and design partner, not the source of manufacturing
geometry. Written project specifications, deterministic calculators, reusable
CadQuery builders, versioned construction profiles, and exact purchased-hardware
data are the construction authority. One saved definition must drive the part,
its machining, its assembly placement, its review model, and its later fabrication
output. The model may reason about intent and choose among supported solutions; it
must not redraw proven geometry from prose.

The skill should state strategic goals and the physical evidence required to
reach them. It should retain room to solve unfamiliar furniture intelligently.
Narrow prohibitions belong in the skill only after a recurring observed failure,
not as an ever-growing script of anticipated mistakes.

### Confirmed decision canon

#### Client experience

- Speak about the client's room and furniture: what is being decided or checked,
  why it matters physically, and what result or answer comes next.
- Keep repositories, branches, files, schemas, scripts, CAD mechanics, tests, and
  skill routing backstage unless the client asks for technical detail.
- Take the lead whenever the supplied facts are sufficient. Ask only for a real
  measurement or preference that can change the furniture.
- End every client-facing message with the next concrete action. Acknowledgement
  releases the next unfinished stage; it must not produce another passive pause.

#### Project truth and ownership

- `aikea.yaml` owns measured-space facts and shared visible choices. Chat is not a
  substitute for the written and validated specification.
- Each generated assembly owns its local specification, parts, builders, joints,
  child assemblies, and purchased-hardware placements.
- Every part and assembly has an explicit local origin, axes, and mapping into its
  parent and global frame. Position reports prove those mappings before review.
- Reusable construction belongs in the skill. Project measurements, generated
  furniture, downloaded vendor CAD, and client-specific choices stay in the
  active project.

#### Measurement and layout

- Establish units, the front-view outline, labelled physical edges, placement
  boundaries, and then only the measurements that reveal the actual fit.
- Preserve raw readings. Repeated readings compare the same trapped boundaries;
  open dimensions normally need one useful reading. Explicit client statements
  are valid design evidence.
- The built-in 2 mm fitting allowance applies only to a dimension enclosed at
  both ends. Cabinet-to-cabinet gaps are calculated tolerances, not a recurring
  client design question.
- Deterministic calculation resolves limiting measurements, clearances, assembly
  positions, cabinet widths, and heights. The model presents the useful result,
  not the formulas.
- Cabinet count and front division must be feasible for the selected door
  hardware before local cabinet generation. A wider opening can become paired
  doors; unsupported oversized single leaves must not be discovered at the end.

#### Construction and manufacture

- Build each sheet as a local manufacturable part, orient it correctly, then
  assemble it through explicit transforms. The preview may never bypass the
  project-owned builders.
- Shared joints generate matching work on both participants from one definition.
  Cabineos use at least two connectors per seam, no more than 300 mm between
  connectors, and no more than 200 mm from either seam end.
- Generated side panels own the System 32 datum: 5 mm holes on a 32 mm vertical
  pitch with 37 mm front and rear mounting lines. Shelves, hinge plates, runners,
  and later fittings reserve both their fixing nodes and their physical envelopes.
- Panels that exceed usable CNC travel are divided into assembly-ready modules.
  Machine capacity and cutter clearance belong to a manufacturing profile rather
  than to the client's wardrobe measurements.
- Visual realism supports inspection, but it is not geometric proof. Local/global
  position reports, contact and overlap checks, matched machining, movement checks,
  and focused code tests establish the physical claim.

#### Modular furniture capabilities

- Cabinet geometry must support arbitrary valid widths, heights, flat or sloped
  tops, and reusable arrangements rather than a catalogue of a few fixed shapes.
- Door length and plinth presentation are independent choices. Full-length or
  above-plinth doors and flush or recessed plinth fronts remain composable options.
- A fitted door includes its slab, selected relationship, matching cabinet and
  door machining, exact purchased hinge and plate, and checked closed/open states.
  The standard proposal for a single door is left-hinged; only an explicit client
  choice after visual review changes it.
- Drawers are independent repeatable child assemblies, not a special three-drawer
  stack. Every drawer may have its own height, depth, row, runner profile, and
  review extension. Front and back panels span the complete outside width with
  the sides captured between them.
- Exact runner selection follows the available cabinet depth and verified
  manufacturer CAD; hardware is never scaled to impersonate another product.
  Drawer-stack heights should use the available capacity deliberately while
  preserving clear movement and shared hardware reservations.
- Recessed lighting starts from the fewest practical purchased components. Its
  groove, purchased body, placement, inward illumination, and clearance from
  doors and hinges derive from the same saved part-local run.

#### Proof and repetition

- Build one complete representative assembly first. If it has doors, drawers,
  lighting, or bought hardware, those features must be physically present in the
  approval model rather than promised for a later stage.
- Show the same saved assembly in the views needed to judge fit and movement.
  The client's visual approval comes before repetition or the model eval for that
  feature; focused deterministic checks then lock the approved relationship.
- Only after the first complete assembly is approved should AIkea repeat the
  capability across the remaining furniture.

## Current release boundary

The alpha package provides nine skills, deterministic cabinet and feature
builders, recursive assembly review, and a fabrication-readiness checker.
The [README](../README.md) describes installation and the current limitations.

Material advice records confirmed product choices, but generated parts do not
yet carry the exact material identity required by the fabrication checker.
Full manufacturing output and a complete fresh fabrication proof remain
unfinished. The checker must continue rejecting incomplete evidence.

The connector receiver includes a user-designed enlargement for brass threaded
inserts. Changes to cutter sourcing must preserve that geometry; the standard
wood-screw receiver is not an interchangeable replacement.

## Documentation audit

- 2026-09-06: Public-release cleanup retains the reusable architecture contracts
  and replaces historical personal-project handovers with the current alpha
  boundary. The private development history is preserved locally.
