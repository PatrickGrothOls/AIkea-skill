# WP1: Shared construction inputs

## Scope and current state

Branch: `feat/shared-construction-inputs`, based on planning commit `57023a6` and
main `52facbf`. This slice defines and installs the shared input values without
changing the existing construction algorithm. WP2 supplies their shared executor.

- [x] Trace a saved mixed wardrobe and the standard generated cabinet route.
- [x] Reuse the physical tree and explicit placement contracts.
- [x] Define and install editable construction inputs and per-part material identity.
- [x] Define extension, requirement coverage and regeneration responsibilities.
- [x] Verify generated-project compatibility and review with the `review` skill.

## Trace from the actual wardrobe

Read-only source: `AIkea-korrekt-base-run/wardrobe-trial`, root
`assemblies/furniture_legs_01/builder.py`. No project files were changed.

| Requirement/feature | Current producer | Construction/output | Migration consequence |
| --- | --- | --- | --- |
| Cupboards, shelves and niche | `furniture_01/inputs.py`, `components.py`, `panels.py` | Drafts emit explicit placed panels and Cabineo joints. | Preserve input calculations; reuse common panel/joint execution. |
| Mixed layout | `furniture_01/builder.py` | Named children in one `CompositeAssemblySpec` and `BuiltAssembly`. | Keep tree/ownership; no special seat or wardrobe schema is necessary. |
| Drawers | `furniture_01/drawers.py` | Wooden panels with allowance assumptions; exact runner integration is absent from this producer. | Required mechanism selection stays unresolved until an exact component is added. |
| Doors | `components.py` | Front/side-access panels; this producer does not declare hinges. | A door-shaped panel is not evidence of a supported moving door. |
| Legs and base | `base_trial_01/builder.py`, `hardware.py`, access/pilot modules | Korrekt purchased geometry plus modifications to existing base/cabinet parts. | Host modifications and purchases need common ownership/evidence; migrate the separate Korrekt operation. |
| Shared/custom shapes | `half_lap_joint.py`, `panel_segmentation.py`, `RoutedPanelBuilder` | Custom joint and blank extensions alongside common parts. | Supported extension contract, not a prohibition on nonstandard geometry. |
| Whole-design review | `furniture_legs_01/builder.py` | Replaces the base while retaining the existing root tree. | Verify final tree and current runtime rather than unrelated preview files. |

The saved project uses a copied runtime and separate Korrekt helpers. This trace
is source evidence, not a fresh build or fabrication approval. Main already has
parts, placement, inventory and fabrication consumers; these stay authoritative.

## Common input contract

`assemblies.construction_specification.PanelAssemblySpec` owns explicit parts,
joints, child placements, purchases and local machining requests. It deliberately
has no required cabinet height, plinth, bay count or furniture-purpose lookup.
Its first six fields match the existing composition branch's panel specification.

| Value | Producer | Consumer/obligation |
| --- | --- | --- |
| `PartSpec.local_size_mm`, outline, placement and inside face | Recipe or authored specification | Shared blank/operation execution uses the manufacturing frame, never the semantic role to choose machining. |
| `PartSpec.material_id` | Saved project material selection | Existing physical counter can now retain the selection; empty remains an explicit inventory gap for older projects. |
| Existing joint specs and participant IDs | Recipe or authored connection layout | Existing joint tools produce paired `PartCut` entries. The shared boundary validates ownership and participation. |
| `PartMachiningSpec` identity, target part, operation type | Recipe or explicit authored request | WP2 operation dispatcher; unsupported requests fail construction instead of silently disappearing. |
| Existing child and hardware specs | Recipe/component or authored composition | Existing tree and purchase-unit consumers; identities must be retained rather than counting CAD sub-solids. |

Only System 32 needs the first local-machining request. This is not a generic
parameter dictionary or a new plugin language. An operation needing new explicit
parameters gets a focused typed request when its actual consumer is implemented.
The CAD runtime is not imported by these input values.

## Responsibilities beyond these values

- **Requirements:** keep the project's required attachments, support, motion and
  purchased components explicit. Each must map to a connection, feature or
  justified disposition (for example floor contact or a removable loose shelf).
  Unanswered requirements remain unresolved. WP4 connects coverage to the existing
  evidence gate; a tree alone cannot prove that requirements were not omitted.
- **Extensions:** a new blank returns one local shape per physical part. A new
  connection implements the existing `AssemblyCuts`/`PartCut` contract for its
  participants. Built children/hardware retain declared order and ownership.
  Shared execution checks apply to extension output; material, hardware, motion
  and strength evidence remain separate. Cross-child operations resolve one
  common frame and return cuts to the actual owning parts, never duplicate panels.
- **Configurators:** return ordinary immutable construction inputs. Authored code
  may adapt those values with `dataclasses.replace` before building. Recompute a
  recipe from saved parameters, then reapply deliberate authored transformations;
  do not edit exported geometry or lose dependent connection IDs.
- **Regeneration:** keep the existing generated-file fingerprints and conflict
  checks. Authored composition/override code is user-owned, outside the generated
  file set. A locally modified generated file causes a conflict rather than an
  overwrite. Parameter changes must trigger rebuilding and evidence invalidation.
- **Non-sheet stock:** existing custom rod/purchased-item types keep their own
  physical identity. This panel input is not a claim that all stock is sheet stock.

## Verification and review

`review` skill completed against parent `57023a6`: scope clean; no actionable
findings in either critical or informational pass. The required testing specialist
independently reviewed the four code/test files and compatibility callers and
reported no findings. Primary regression: **29 passed**; independent overlapping
subset: **20 passed** (not additional unique tests). `git diff --check` passed.

Command: `direnv exec . python -m pytest tests/test_construction_specification.py
tests/test_assembly_composition_contract.py tests/test_assembly_composition_rejections.py
tests/test_assembly_taxonomy_generator.py tests/test_assembly_taxonomy_revision.py
tests/test_assembly_taxonomy_upgrade.py tests/test_physical_item_counter.py -q`.

These tests verify the contract through an actual generated package and its
existing consumers; they do not certify geometry. No PR existed; network PR
lookup was unavailable. No external comments or unrelated skill setup were
changed. All changed code files remain below 150 lines.

## Audit log

1. 2026-09-11 — Implemented the approved WP1 scope using existing dataclasses and
   output contracts. Added only explicit local machining and material identity;
   no new furniture registry, serialization system, or dimensions were invented.
2. 2026-09-11 — Traced the actual mixed wardrobe. Missing selected mechanisms
   remain design gaps, not a reason to infer hardware from its appearance.

3. 2026-09-11 — WP1 passed its per-package review and compatibility regressions.
   Continued with WP2; future work is not counted as complete by this review.
