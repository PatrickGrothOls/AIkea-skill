---
name: aikea
description: Design, revise, check, and export generic frameless sheet-material cabinet runs from measured spaces. Use for new or existing AIkea projects involving multiple cabinet bays, flat or sloped ceilings, shared cabinet dimensions, structural plinths, Cabineo connectors, equal-thickness miters, STEP models, BOMs, or cut lists. Also use to inspect or diagnose AIkea measurements and geometry. AIkea v1 excludes LED grooves, drawers, face frames, and machine-specific NC output.
---

# AIkea

Build from saved measurements and shared design settings. Never treat chat history or generated geometry as the source of truth.

## Start from project state

- If `aikea.yaml` exists, read it and continue from its saved values.
- If the user asks only to inspect or check a project, perform only that operation.
- If no `aikea.yaml` exists, start with the overall wardrobe measurements below.

## Collect the overall wardrobe inputs

1. Read `references/overall-wardrobe-inputs.md` completely.
2. Inspect only the user's request, user-identified attachments, and the target project's AIkea files.
3. Ask only for required values that remain missing or contradictory. Never guess a measurement.
4. Copy `assets/aikea.yaml` into the project root and fill only user-supplied measurements and confirmed design settings.
5. Run `python scripts/calculate_overall_wardrobe.py <project>/aikea.yaml` from this skill folder.
6. Correct reported input problems with the user. Do not generate cabinet geometry until the check passes.

Never take project measurements from this skill's assets, examples, eval fixtures, development documentation, legacy wardrobe code, or another project. Those files are implementation knowledge or test data, not measurements for the active cabinet run.

Keep these responsibilities separate:

- AIkea chooses the correct construction method, part face, and reference edge.
- Deterministic scripts calculate dimensions, placements, and machining.
- Evals prove the completed geometry fits and matching cuts align after assembly.

## Current implementation

The implemented slice collects and checks overall wardrobe inputs. Cabinet construction, joinery, geometry, and exports will be added only with their own deterministic scripts and evals. Do not improvise an unimplemented capability.
