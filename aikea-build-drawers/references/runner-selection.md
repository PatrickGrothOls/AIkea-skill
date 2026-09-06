# Runner selection and construction handoff

This reference owns cabinet fit requirements and the transition from a sourced
product to verified drawer construction. Manufacturer discovery and downloads
belong to [$aikea-source-hardware-cad](../../aikea-source-hardware-cad/SKILL.md).

## Establish the requirements

Read the active cabinet's generated specification, drawer layout and hardware
reservations. Record the owning cabinet/drawer and the facts that constrain its
runners:

- Clear inside depth from the installation datum to the back obstruction; front
  and back construction, inner fronts and required setbacks. Overall furniture
  depth is only an upper bound, not the runner's available installation depth.
- Clear opening width, intended drawer width/height and drawer material and
  thickness. Account for door hinges, side spacers, shelf fittings and other
  obstructions along both the closed and opening paths.
- Required load including the moving drawer's own weight, useful extension,
  closing/opening behavior, mounting arrangement and any client constraints on
  manufacturer, product, budget or supply location.

Use known project facts without asking again. Ask only for missing requirements
that change suitability, such as intended heavy contents; do not invent a load
rating or choose a different cabinet depth to accommodate existing hardware.
Preliminary discovery can use confirmed bounds, but label unresolved dimensions
and do not declare fit until the actual installation space is known.

An exact client-selected article remains the selection. If its published
requirements conflict with the cabinet, explain the specific conflict and obtain
the client's choice before changing either the product or the furniture.
Without an exact selection, treat brand/family preferences as search constraints.

## Source against those requirements

Pass the requirements, explicit preferences and any exact existing selection to
the sourcing skill. It should return exact product identities, official planning
and installation evidence, required companion parts, and the source/download
state. Follow that skill's manufacturer directions rather than treating the
bundled profiles as a shopping list.

Evaluate candidates against the complete requirements, including width/load
limits and the installed envelope of accessories. Nominal length alone does not
prove fit. Among otherwise suitable products, use the available depth and desired
extension to propose useful drawer capacity. Ask the client only about tradeoffs
that change fit, capacity, cost or requested behavior; do not require them to
choose a model number when the technical requirements already decide it.

Keep the requirements, candidate comparison, exact chosen identity, official
links and unresolved evidence together in the active project's local hardware
notes. These notes support the decision; the verified generated drawer records
remain the construction authority. A catalog miss is a discovery trigger. A
manufacturer search with no suitable result must name what was searched and the
constraint or unavailable evidence, without claiming universal unavailability.

## Verify and connect the selected product

1. Recheck the exact article's planning values against the cabinet. Follow the
   sourcing skill for missing installation documents, handed CAD and companion
   components; preserve its original bytes and provenance.
2. Verify the actual CAD identity, native units/bounds, separate handed or paired
   members and accessories. Resolve manufacturer mounting datums, fixing axes,
   drawer sizing, material/pilot requirements and motion evidence for this exact
   article. A hash identifies bytes; it does not verify their geometry or fit.
3. Match that evidence to the construction implementation. Reuse an existing
   profile only when its exact identity and evidence match. For a new length or
   product, integrate its own planning profile, source manifest, importer/member
   classification, mounting/machining and motion model. Reuse compatible generic
   calculations; do not copy another length's hole pattern, checksum, bounds or
   approvals, scale its STEP, or relax a verifier to admit the new file.
4. Verify the actual generator and saved builder consume that selected identity.
   A new profile row alone is insufficient if an importer, generator or rebuild
   still selects another article. Check a rebuilt drawer's identity, dimensions,
   source members, reservations and machining before returning to construction.
5. Generate one drawer in its owning cabinet and run the existing source, fit and
   complete-assembly checks. Prove closed containment and opening clearance with
   the cabinet's other features; show that same saved assembly for visual review.

### Existing integration points

- KA 5332: `HettichKa5332RunnerProfile` and `HettichKa5332RunnerCatalog` hold
  exact planning data; `HettichKa5332CabinetDrawerPlanner` accepts a catalog.
  The product manifest, STEP loader, generator and rebuild path must also support
  the new identity. A custom planner catalog alone does not extend the CLI.
- MOVENTO: `MoventoRunnerProfile` carries the exact handed asset set and mounting
  profile. Its catalog, manifest, verifier, generator and rebuild must agree.
- KA 4532 with spacer: the current planner and STEP signatures describe exact
  articles 9114276 and 13952. They are not a generic KA 4532 family adapter.

These are implementation entry points, not permission to alter shared skills
during an ordinary furniture project. Complete reusable integration when that
implementation work is authorized. Otherwise preserve the sourced candidate and
state the exact construction support still needed. Do not ask the client to
research profiles or reinterpret an integration gap as a cabinet-size problem.

## Report the reached state

- **Candidate found:** official identity and planning evidence are available;
  unresolved fit requirements remain visible.
- **CAD sourced:** the complete required source set is stored with provenance.
- **Construction supported:** the exact profile, source verification and saved
  builder path work for this product.
- **Fit reviewed:** the composed cabinet passes its required placement/movement
  checks and has been visually inspected. Client approval remains distinct.

Advance automatically while the evidence and authorized work permit. A protected
download, missing manufacturer datum or unsupported construction has its own
concrete next action; none is a successful complete drawer build.
