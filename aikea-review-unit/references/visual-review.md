# First cabinet visual review

## Required starting state

- The active project contains a complete `aikea.yaml`.
- `assemblies/specification.py` and every calculated local unit folder exist.
- No later unit has been produced as a visual or manufacturing model.

## Review artifact

Use the first assembly in the saved left-to-right run as the review cabinet.
Execute its generated assembly builder, place the returned local CadQuery parts
through explicit assembly locations, combine them in one named CadQuery assembly,
and use CadQuery's GLB exporter. The mock-up includes every calculated carcass
panel, complete shaped back and door outlines, every top-boundary segment, and
the door opened from its calculated hinge edge so the cabinet can be inspected.
It preserves any construction already produced by the generated assembly builder;
the review stage itself neither adds nor approximates missing manufacturing work.

The generator writes exactly one file:

```text
assemblies/<first-assembly-id>/<first-assembly-id>.glb
```

Do not create GLBs for later assemblies before approval.

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

## Viewer

The skill bundles a prebuilt browser viewer and a loopback-only Python server. The
server requires no application backend, package installation, database, Docker,
or Node runtime. It serves only the bundled viewer and the chosen GLB, opens the
browser automatically, and remains active until stopped.

The client can drag to rotate the cabinet around its center, bring a visible
detail into view, and then scroll or pinch to move straight closer without
changing the viewing direction. Keep the viewer open while asking for the visual
decision; do not make the client locate files or run terminal commands.

The same viewer accepts `view=top`, `view=bottom`, or `view=structure` in its URL
when a fixed base angle explains the result more clearly than an interactive
perspective. `title` supplies the short client-facing label shown with that view.

## Completion state

The stage is complete only when the GLB is open and the client has one clear
decision to make about the cabinet's visible result. Until they approve it, the
project state is `awaiting_visual_approval` and later cabinets remain unbuilt.
