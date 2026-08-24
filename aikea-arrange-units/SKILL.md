---
name: aikea-arrange-units
description: Arrange the physical units in a measured AIkea furniture project from left to right and save their purposes and relative widths. Use after the overall space is checked when deciding, revising, or reviewing an arrangement containing tall storage, benches, or other sheet-material units, before local unit design, parts, joinery, or folder generation begins.
---

# AIkea arrange units

Settle one ordered furniture arrangement and save it in the global project specification. Speak like a carpenter helping a client; keep project-file fields and calculations private.

## Establish the project state

1. Resolve the active project folder from the user's request and current working directory.
2. Require an existing `aikea.yaml` with checked overall measurements and shared settings. If that work is unfinished, return to `$aikea` and ask only for the missing earlier information.
3. Read `references/unit-arrangement.md` completely before changing the project.
4. Preserve every measurement, design decision, and shared setting that this stage does not own.

## Arrange the units

1. Ask what the furniture should contain from left to right. Let the client describe purposes naturally; do not offer a fixed catalogue of geometric shapes.
2. Once the purposes and order are known, ask how their widths should relate. Never ask for width shares or percentages. Offer numbered choices when the relationship is missing.
3. Ask about only one unfinished topic per response. Do not repeat a question whose answer is already supplied.
4. If purpose, order, and width relationships arrive together, save the complete arrangement without asking another question.
5. When revising an arrangement, keep stable IDs for units that remain. Change only the purposes, order, or width relationships the client changed.

## Save the arrangement

1. Translate the confirmed client description into the exact `assembly_run` contract in the reference.
2. Generate stable IDs privately from purpose and occurrence, such as `tall_storage_01`, `bench_01`, and `tall_storage_02`. Never ask the client to name IDs.
3. Preserve the existing run-wide left clearance, right clearance, gap, and ceiling clearance. Rename `cabinet_gap` to `gap` when replacing a legacy `cabinet_run`.
4. Replace `cabinet_run` only when the new arrangement is complete. Never keep both representations.
5. Check that every ID is unique, every purpose is non-empty, every width share is positive, and list order matches the confirmed left-to-right order.
6. Summarize the saved arrangement in client-facing language and stop. Do not begin local unit design in the same response.

## Keep later design out

Do not ask for or decide heights, shelves, doors, panels, supports, plinth construction, joint types, Cabineo placement, miters, machining, or manufacturing output. Do not create `assemblies/` folders in this stage. Those responsibilities begin only after the arrangement has been saved and checked.

## Current implementation

Guide, save, and review the ordered `assembly_run`. Folder generation and local design are later deterministic stages.
