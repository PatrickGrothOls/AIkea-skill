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
part value from that unit specification. Each part builder returns its real
CadQuery part in its canonical local frame. The cabinet assembly builder consumes
the explicit parts, joint and local-machining requests through the shared panel
executor. Individual part entry points read from this same finished result.
Base and older saved builders retain their earlier construction adapter until
their separate migration. Both return the existing built parts, joints and cuts.

The local top boundary begins at `0` and ends at the unit width. It preserves every
confirmed project-boundary change that falls inside the unit instead of reducing
the unit to left and right heights.

## Full-height tall storage

The current construction taxonomy produces:

- left and right side panels;
- one back panel retaining the complete local outline;
- one door panel;
- three removable shelf panels with four declared supports each, on rows shared by both sides;
- one top panel for every segment of the local top boundary;
- one authoritative list of the physical relationships between those parts.

This taxonomy establishes ownership and exact resolved dimensions. Supported
construction is derived from one shared joint definition so mating features stay
aligned when any upstream dimension changes.

The local specification also inherits the selected door lower line and its exact
resolved height. Door geometry is calculated from that shared result rather than
adjusted separately inside each assembly, so the same unit can use either a
full-length door or a door ending at the plinth.

Shelf count, dimensions, and support rows are owned by the local assembly. Each
shelf leaves 0.5 mm clearance at each side of the clear opening and stops at the front face
of the structural back. Its support row must exist in both side-panel hole patterns,
including when a confirmed top profile gives the two sides different heights.
The [storage-shelf policy](storage-shelves.md) requires actual support hardware and
matching bores; fixed Cabineo storage shelves need a recorded deliberate choice
and hidden underside pockets. Structural cabinet floors/tops are separate.

The default structural carcass uses a load-bearing back and the lower support
assembly as physical participants. On a flat unit, the top spans and bears directly
on the side panels. Each square side/back, side/top, and top/back seam is a paired
Cabineo joint; the side/top connector is machined from the side's inside face toward
its top edge so the matching receiver enters the top from below. Angled
equal-thickness top seams use one paired miter cut shared by both panels. A back that
is too thin for the selected connector profile must fail construction instead of
producing a through-cut receiver.

## Structural base

The base is one generated assembly beneath the cabinet run. It owns CNC-sized
deck and front-kickboard modules plus exact Korrekt 61854/70151 purchases and their
mounting operations. There is no rail/brace fallback. Overall base height includes
the deck. Check both the product adjustment range and the unchanged source pose,
full plate edge margins, floor access and whole-foot kickboard clearance using
[the base recipe](base-recipe.md).

Module seams, kickboard clips, screws, cabinet attachment, socket fit and load
qualification remain explicit construction requirements. A generated folder or
valid cut does not qualify these connections.

## Safe regeneration

The generator renders and checks the complete write set before changing the
project. `assemblies/generated-files.json` records the exact content produced by
the last successful run. Missing files are created, identical files are left
unchanged, and recorded files are refreshed when an overall or local input changes.
If a local file no longer matches its generated record, generation stops and
reports every conflicting path without overwriting any of them. The record is
updated only after the complete checked write succeeds.

## Command result

Success returns JSON with `status: generated` and every generated assembly path.
Invalid project values or local-file conflicts return `status: invalid` with the
specific problems. Only `generated` completes this stage and hands the first
ordered assembly to `$aikea-review-unit` for visible approval.
