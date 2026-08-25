# Unit taxonomy

## Required starting state

- The active project contains a complete `aikea.yaml`.
- Overall measurements and shared settings have passed their deterministic check.
- `design_settings.assembly_run` contains the complete ordered run with stable IDs,
  purposes, and width relationships.

## Generated ownership

The generator creates one local owner for every supported unit:

```text
assemblies/
  specification.py
  <stable-assembly-id>/
    spec.py
    builder.py
    joints/
      spec.py
    parts/
      <stable-part-id>/
        spec.py
        builder.py
```

The unit `spec.py` is authoritative for its local boundary, resolved parts, and
physical joint relationships. Each part `spec.py` exposes only its own finished
part value from that unit specification. Each builder returns an immutable build
plan for the next construction capability.

The local top boundary begins at `0` and ends at the unit width. It preserves every
confirmed project-boundary change that falls inside the unit instead of reducing
the unit to left and right heights.

## Full-height tall storage

The current construction taxonomy produces:

- left and right side panels;
- one back panel retaining the complete local outline;
- one door panel;
- one top panel for every segment of the local top boundary;
- one authoritative list of the physical relationships between those parts.

This taxonomy establishes ownership and exact resolved dimensions. Joinery and
machining capabilities later enrich each physical relationship from one shared
joint definition.

## Safe regeneration

The generator renders and checks the complete write set before changing the
project. Missing files are created. Existing identical generated files are left
unchanged. If an existing local file differs, generation stops and reports every
conflicting path without overwriting any of them.

## Command result

Success returns JSON with `status: generated` and every generated assembly path.
Invalid project values or local-file conflicts return `status: invalid` with the
specific problems. Only `generated` completes this stage.
