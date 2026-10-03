# Assembly positioning

## Goal

Make every assembled result traceable from each manufactured part to the measured
space. A visual review is ready only when the generated geometry proves where
every zero point lands and that supported assemblies meet without misplaced or
overlapping material.

## Coordinate systems

The measured space is the global coordinate system. Its zero point is the
front-left floor point. Positive X runs right, positive Y runs back, and positive
Z runs up.

Every assembly has its own local zero at the lower-front-left point of its outer
footprint on the floor plane. Its saved global position maps that local zero into
the measured space. Every part remains in its own manufacturing coordinates and
uses an explicit transform into the assembly.

Presentation changes, such as opening a door for inspection, happen after the
physical assembly placement. They do not change the position used for fit or
manufacturing checks.

## Required position check

Before showing assemblies together, generate `assembly-position-check.json` from
the built CadQuery parts. The report must state:

- each assembly's local zero and global zero;
- every part's local zero, its local axes in the assembly, and its global zero;
- its measured bounds in both coordinate systems;
- the contact height and footprint shared by the cabinet and base;
- the built door lower line and plinth-front depth selected by the overall project;
- the exact location and purpose of any module break that does not coincide with
  a cabinet edge;
- the exact base-module parts included beside the selected cabinet, excluding
  every part owned by a neighbouring module;
- a passing result for every required relationship.

Use the report to decide whether the geometry is ready for review. If any
relationship fails, stop before export and correct the position owner. When the
report passes, describe the physical result in client language and ask for the
next visible decision rather than relaying the checking mechanics.
