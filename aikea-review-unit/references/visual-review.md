# First cabinet visual review

## Required starting state

- The active project contains a complete `aikea.yaml`.
- `assemblies/specification.py` and every calculated local unit folder exist.
- When the first cabinet has a fitted hinged door, its complete door relationship
  and exact purchased hinge hardware have been built before review.
- No later unit has been produced as a visual or manufacturing model.

## Review artifact

Use the first assembly in the saved left-to-right run as the review cabinet.
Execute its generated assembly builder, place the returned local CadQuery parts
through explicit assembly locations, combine them in one named CadQuery assembly,
and use CadQuery's GLB exporter. The result includes every calculated carcass
panel, complete shaped back and top-boundary segments, and the supplied removable
shelves.

Treat every configured fitted door as a physical relationship rather than a
visible slab. Its first review must come from `$aikea-build-doors` and include the
machined door, matching cabinet-side work, exact purchased hinges and plates, and
the checked closed and open positions. The plain unit mock-up is the review path
only when the assembly is intentionally doorless. The review stage preserves the
construction produced by the owning builders; it neither adds nor approximates
missing manufacturing work.

An intentionally doorless review writes exactly one file:

```text
assemblies/<first-assembly-id>/<first-assembly-id>.glb
```

The complete fitted-door review instead uses its door skill's checked closed and
open GLBs. Its first model also loads the project-wide door-opening review record.
That record lists every cabinet's checked hand while later cabinets remain saved
specifications rather than additional visual models. The client approves the
complete opening proposal or requests one cabinet change directly from the
viewer. Do not create GLBs for later assemblies before approval.

## Structural base review

Once the first cabinet is approved, execute the generated `base_01` builder and
place its deck, front and back rails, and braces from the base specification. The
parts must close the complete base bounds without overlapping material. Rails and
braces meet at their edges, braces bear the deck, and the cabinet sides begin on
the deck's top face. The review must show the selected door lower line and
plinth-front position while keeping the structural deck beneath the complete
cabinet footprint.

The base review generator writes:

```text
assemblies/base_01/base_01.glb
assemblies/base_01/<first-cabinet-id>_with_base.glb
assemblies/base_01/assembly-position-check.json
```

The first file contains the complete segmented base. The combined file contains
the first cabinet and the base module directly beneath it, keeping their contact
large enough to inspect without generating later cabinet models.

## Full wardrobe review

After the first cabinet and its base relationship are approved, execute every
generated cabinet builder and the complete base builder. Place each assembly from
its saved local zero into the shared project coordinates. Show the cabinet doors
closed when the client is judging the complete facade, gaps, lower line, and
overall proportions. When the client wants to inspect the inside or the
relationship between neighbouring doors, choose each cabinet door independently:
closed in its physical position, open around its calculated hinge edge, or absent
from the review so it cannot hide another feature. Keep each exported node
associated with its source assembly and part.

Write both artifacts at the generated assembly root:

```text
assemblies/full_wardrobe_review.glb
assemblies/full_wardrobe_open_review.glb
assemblies/full_wardrobe_door_states_review.glb
assemblies/full-wardrobe-position-check.json
```

Alternate door files are produced only when requested. Every view uses the same
checked physical assembly, and omitted doors remain represented in the position
report. The report must pass before export. It proves that the base spans the complete
run, every cabinet occupies its saved width, each carcass bears on the deck,
cabinet gaps remain open, all doors reach their selected lower line, and the
plinth front remains at its selected depth.

## Viewer

The skill bundles a prebuilt browser viewer and a loopback-only Python server. The
server requires no application backend, package installation, database, Docker,
or Node runtime. It serves only the bundled viewer and the chosen GLB, opens the
browser automatically, and remains active until stopped.

The client can point at a visible detail and scroll to bring that exact area
closer without losing it beneath the pointer. Dragging rotates the cabinet around
the measured center of the complete model, including after an off-center close-up.
Holding Shift while scrolling pans along the supplied wheel or trackpad direction;
holding Shift while dragging gives free two-dimensional panning. Panning changes
only the camera position, leaving the furniture and its rotation center unchanged.
Keep the viewer open while asking for the visual decision; do not make the client
locate files or run terminal commands.

Perspective review should make the generated cabinet easy to judge as a finished
physical object. Use the packaged photographic lighting and material presentation,
keep a clean interactive image visible while the client moves or while photographic
samples are still gathering, then fade into the refined image after the client
settles on an angle.

Drawer review supports closed, open, and removed states without changing the
checked physical design. Closed and removed views use the genuine static runner
CAD in its checked mounting frames. The open view uses separately named movement
guides because the available manufacturer files do not expose articulated runner
members. Require its movement report, keep the genuine locks with the moving
drawer, and exclude every guide from manufacturing, machining, and collision
claims.

The same viewer accepts `view=top`, `view=bottom`, or `view=structure` in its URL
when a fixed base angle explains the result more clearly than an interactive
perspective. `title` supplies the short client-facing label shown with that view.

## Completion state

The stage is complete only when the GLB is open and the client has one clear
decision to make about the cabinet's visible result. A fitted-door review is
approved only after the model has loaded and the client confirms the labelled
opening proposal. Until then, the project state is `awaiting_visual_approval`
and later cabinets remain unbuilt.
