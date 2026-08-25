# Unit arrangement

## Responsibility

This stage owns only the purposes, left-to-right order, and relative widths of the physical units across the measured space. The global specification owns this arrangement because changing one unit's width changes the available width and position of the others.

Local assembly specifications later own geometry that affects only one unit, such as bench height, supports, doors, and subparts. Joint specifications later own matching machining.

## Universal interior hole pattern

Every relevant full-height unit receives the supplied universal shelf-and-hanger
hole pattern. It supports both adjustable shelving and hanger hardware without a
client choosing an internal use for each unit.

The versioned construction profile owns the exact hole sizes, offsets, spacing,
eligible panels, and supported hardware. The deterministic assembly-generation
stage applies that profile to local part geometry. This arrangement stage must not
invent those dimensions, ask what a unit will store, or ask the client to choose
between hanging space, shelves, or a mixture.

## Required starting state

- `aikea.yaml` exists in the active project.
- Overall space measurements and shared settings have been checked.
- No unresolved conflict changes the usable width.

Do not take project values from skill assets, eval answers, examples, legacy code, or another project.

## Global specification contract

Store the ordered arrangement under `design_settings.assembly_run`:

```yaml
assembly_run:
  left_clearance: 0
  right_clearance: 0
  gap: 2
  ceiling_clearance: 10
  assemblies:
    - id: tall_storage_01
      purpose: tall_storage
      width_share: 1
    - id: bench_01
      purpose: bench
      width_share: 0.5
    - id: tall_storage_02
      purpose: tall_storage
      width_share: 1
```

List order is physical order from left to right. Do not add a second order field or a separate assembly count; both are already expressed by the list.

Each assembly requires exactly:

- `id`: stable internal identity in lowercase snake case with a two-digit occurrence suffix;
- `purpose`: the client's confirmed functional purpose in lowercase snake case;
- `width_share`: one positive relative width value.

## Translate existing projects

When replacing `design_settings.cabinet_run`:

- preserve `left_clearance`;
- preserve `right_clearance`;
- rename `cabinet_gap` to `gap` without changing its value;
- preserve `ceiling_clearance`;
- replace `cabinet_count` and `cabinet_width_shares` with the ordered `assemblies` list;
- remove `cabinet_run` only after the complete replacement is ready.

Preserve `measured_space`, `design_decisions`, `fit_allowance`, `fitted_dimensions`, `base`, `doors`, `materials`, and every other unrelated project value exactly.

## Stable IDs

Build a new ID from the confirmed purpose and its occurrence among assemblies with that purpose. For `tall storage, bench, tall storage`, use `tall_storage_01`, `bench_01`, `tall_storage_02`.

During revision, identity outranks position. Keep an existing ID when that physical unit remains, even if it moves or its width changes. Create an ID only for a newly added unit; remove an ID only when the client removes that unit.

## Width relationships

The client speaks in ordinary relationships: equal, half as wide, twice as wide, narrower, wider, or an explicit intended width. Translate those relationships privately.

Use the first assembly as share `1` and express every later assembly relative to it. Examples:

- three equal units become `[1, 1, 1]`;
- matching tall units with a half-width bench become `[1, 0.5, 1]`;
- a second unit twice the first becomes `[1, 2]`.

Do not round away a confirmed relationship. When words such as “a little narrower” are not precise enough to calculate, offer numbered choices or help the client settle the relationship before saving.

## Completion states

- **Missing:** Ask only for the missing purpose/order or width relationship.
- **Contradictory:** State the exact conflict in client language and ask only for its correction.
- **Complete:** Save the exact arrangement, summarize it, and continue directly into automatic assembly generation without an internal-use question.

Every response must end with the next obvious action. Ask the exact next question and provide a numbered reply instruction only when the client's answer can change the design. Otherwise take the next automatic action. Never invent a client question to bridge stages or end with a passive statement that the system is available whenever the client chooses to continue. Treat an acknowledgement such as "great" as a continuation signal and take the next unfinished action immediately.

The room's flat, sloped, or stepped boundary does not select a unit shape. A later deterministic calculation clips that boundary to each assembly's allocated span. A local unit such as a bench may stop at its own chosen height; that local choice is not part of this arrangement.
