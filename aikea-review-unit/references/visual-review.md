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

## Viewer

The skill bundles a prebuilt browser viewer and a loopback-only Python server. The
server requires no application backend, package installation, database, Docker,
or Node runtime. It serves only the bundled viewer and the chosen GLB, opens the
browser automatically, and remains active until stopped.

The client can drag to rotate and point at any visible detail before scrolling or
pinching to zoom directly toward it. Keep the viewer open while asking for the
visual decision; do not make the client locate files or run terminal commands.

## Completion state

The stage is complete only when the GLB is open and the client has one clear
decision to make about the cabinet's visible result. Until they approve it, the
project state is `awaiting_visual_approval` and later cabinets remain unbuilt.
