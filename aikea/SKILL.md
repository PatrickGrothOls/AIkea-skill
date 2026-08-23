---
name: aikea
description: Design, revise, check, and export generic frameless sheet-material cabinet runs from measured spaces. Use for new or existing AIkea projects involving multiple cabinet bays, flat or sloped ceilings, shared cabinet dimensions, structural plinths, Cabineo connectors, equal-thickness miters, STEP models, BOMs, or cut lists. Also use to inspect or diagnose AIkea measurements and geometry. AIkea v1 excludes LED grooves, drawers, face frames, and machine-specific NC output.
---

# AIkea

Use explicit user messages to create or revise the saved measurements and shared design settings. Once saved, treat `aikea.yaml`—not chat, prose, or generated geometry—as the project source of truth. Use the skill to choose the workflow and the bundled scripts to calculate results.

## Work from the active project

1. Resolve the active project folder from the user's request and current working directory.
2. If `aikea.yaml` exists, read it and preserve every value the user has not changed.
3. If the user asks only to inspect or check a project, perform only that operation.
4. If the project has no `aikea.yaml`, start the overall wardrobe intake.

## Run the overall wardrobe intake

1. Read `references/overall-wardrobe-intake.md` completely.
2. Read only the user's messages, user-identified attachments, and the active project's AIkea files for project values.
3. Classify the current inputs as missing, contradictory, or complete.
4. For missing inputs, ask once for all remaining required values, grouped as measured space and shared design settings. Do not ask for values already supplied.
5. For contradictory inputs, identify the exact conflict and ask only for the correction needed. Never repair a measurement silently.
6. For complete inputs, copy `assets/aikea.yaml` only when the project file does not exist, fill the exact schema, and run `python <skill-directory>/scripts/calculate_overall_wardrobe.py <project>/aikea.yaml`.
7. If the calculator rejects the file, report its specific problems and return to the missing or contradictory state.
8. If the calculator accepts the file, report the saved path and the calculated cabinet widths, positions, heights, and depths.

Never overwrite an existing `aikea.yaml` with the blank template. Never ask a follow-up question when every required value is present and consistent.

Never take project measurements from this skill's assets, examples, eval fixtures, development documentation, legacy wardrobe code, or another project. Those files are implementation knowledge or test data, not measurements for the active cabinet run.

## Keep ownership separate

- Store only measured space and shared geometry choices in the global project file.
- Keep Cabineo dimensions, cutter placement, part faces, and reference edges inside the Cabineo capability.
- Keep rail spacing, rail count, and module construction inside the structural plinth capability.
- Acknowledge later construction requests without inventing unimplemented geometry or adding unsupported global fields.
- Let deterministic scripts calculate dimensions, placements, and machining.

## Current implementation

Collect, save, and check overall wardrobe inputs. Do not improvise cabinet construction, joinery, plinth geometry, or exports that the bundled implementation does not yet provide.
