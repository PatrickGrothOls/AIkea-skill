# Optional framed-door design skill

## Scope

Package the successful backing-and-applied-frame construction as an optional
AIkea skill and reusable project helper. Door shape and construction remain
model-owned choices. Preserve the current wardrobe and all existing door paths.
This branch is stacked on `feat/white-painted-review` (`e3aa9d3`), which supplies
the authored assembly route; it is current with fetched `origin/main` (`52f3dbc`).

## Work packages

- [x] Inspect the proven project builder and existing skill/runtime contracts.
- [x] Add an optional framed-door skill with focused construction guidance.
- [x] Add configurable project helpers using existing part and assembly values.
- [x] Link the option from furniture design and door fitting; preserve alternatives.
- [x] Verify real geometry, nested placement, CNC rejection and repeated setup.
- [x] Run an independent synthetic forward test and package/discovery validation.
- [x] Review the coherent feature slice and expose the skill for local discovery.

## Current state

The framed-front helper passes 27 focused tests; metadata and all 11 skill
discovery/link checks pass. The independent first-build test also passed: a
560 × 980 mm front with 15+5 mm layers, unequal borders and R5 opening corners,
beside a separate custom sloped 20 mm slab. Actual solids, the three-piece cut
list and the complete GLB passed inspection. No viewer or hinge validation was
claimed for that construction prototype. The current wardrobe remains unchanged.
The helper covers a rectangular backing and continuous applied frame with
configurable borders, thicknesses and opening corner radius. This is a reusable
operation, not a catalogue restricting all door designs.
The skill is linked from both repository discovery folders and
`~/.codex/skills/aikea-design-framed-doors` to this persistent worktree. This
document accompanies the local feature commit; no publication or merge is implied.

## Audit log

1. Patrick requested a framed-door skill that makes this construction easy while
   retaining freedom to design any other door. This sets the routing boundary.
2. Extract the successful two-piece construction, replacing project dimensions
   with explicit inputs. Save each part and its glue relationship independently.
3. Use existing `PartSpec`, `BuiltAssembly`, placements, CNC limits and review
   tools. No new door-style registry or fixed material/hardware default is needed.
4. Keep the hinge adapter's slab limitation explicit: a built framed leaf does
   not prove that existing hinge machining already supports both physical layers.

5. Patrick clarified that a hinge should place its hardware pattern on a supplied surface. The new skill now describes that boundary. A second focused branch will extract surface-based drilling from the existing adapter while preserving its current results.
6. The independent test used different dimensions and an unframed sloped leaf to
   verify both reuse and design freedom. It required no package changes. The
   report and artifacts are preserved in the thread's visualization directory
   under `framed-door-forward-test` rather than added to the shipping skill.
