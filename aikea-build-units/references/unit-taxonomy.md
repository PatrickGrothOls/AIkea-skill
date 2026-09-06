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
CadQuery part in its canonical local frame. The assembly builder resolves the
machining implied by the unit's supported joints, gives each part builder only
the work owned by that part, and returns the built parts with the unit's joint
list and resolved cuts.

The local top boundary begins at `0` and ends at the unit width. It preserves every
confirmed project-boundary change that falls inside the unit instead of reducing
the unit to left and right heights.

## Full-height tall storage

The current construction taxonomy produces:

- left and right side panels;
- one back panel retaining the complete local outline;
- one door panel;
- three removable shelf panels whose supports use rows shared by both sides;
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
shelf closes the clear opening between the side panels and stops at the front face
of the structural back. Its support row must exist in both side-panel hole patterns,
including when a confirmed top profile gives the two sides different heights.

The default structural carcass uses a load-bearing back and the lower support
assembly as physical participants. On a flat unit, the top spans and bears directly
on the side panels. Each square side/back, side/top, and top/back seam is a paired
Cabineo joint; the side/top connector is machined from the side's inside face toward
its top edge so the matching receiver enters the top from below. Angled
equal-thickness top seams use one paired miter cut shared by both panels. A back that
is too thin for the selected connector profile must fail construction instead of
producing a through-cut receiver.

## Structural base

The base is one generated assembly beneath the complete cabinet run. Its local
specification owns the calculated base modules and each module's deck, front and
back rail, and full-height braces. Overall base height includes the deck; the
support frame fills the remaining height. Cross-brace length closes between the
front and back rails, and the brace count follows the local construction spacing.
The plinth-front choice positions the front rail and the front end of every brace.
A recessed front shortens that support span while the deck retains the complete
cabinet footprint. This choice is independent of the door lower line.

Long bases divide at useful cabinet boundaries so every deck and rail fits the
selected CNC working area. Each module begins and ends with a brace, and each seam
between modules remains visible in the joint specification. Every brace owns one
paired Cabineo joint to the front rail and one to the back rail. Each joint derives
the brace pockets and matching blind rail receivers from the same geometry. Module
seam machining, cabinet-to-base receiving features, assembly placement, and visual
approval remain later construction checks and must not be claimed merely because
the folders exist.

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
