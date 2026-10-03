# A complete front assembly as the hinge host

Keep the backing, frame or other pieces inside one child with its physical back
datum at local (0,0,0). Local X is width, Y height, +Z toward the visible face.
Use the normal upright door placement in the parent. The supporting upright panel
is owned by that parent and declares its real inside broad face. This first host
supports a direct flat child of explicit panels; the shared drilling recipe needs
parallel broad faces and complete circular sections with continuous material.

Save `DOOR_HOST = DoorHostSpec("front_01", "support", "front_01")` in the parent's
`spec.py`. The first ID names the planning datum, and the third selects the real
front child. No datum panel is added to the physical tree or bill of materials.

```python
from door_host_loader import DoorHostLoader
from door_hinge_plan import DoorHingePlanner
from door_hinge_side import DoorHingeSide
from cabinet_door_feature_generator import CabinetDoorFeatureGenerator
from riex_nc70_hinge_profile import RIEX_NC70_FULL_OVERLAY

# Load the current parent excluding this feature before regenerating it.
host = DoorHostLoader().load(project, current_parent, DoorHingeSide.LEFT)
plan = DoorHingePlanner().plan(host, RIEX_NC70_FULL_OVERLAY, DoorHingeSide.LEFT)
CabinetDoorFeatureGenerator().generate(project, host, plan, RIEX_NC70_FULL_OVERLAY)
```

The generator preflights the actual parent/child machining and purchase IDs before
writing or registering the feature. It saves the installation plan in the same
conflict-checked write set; do not overwrite the active plan before generation.
The feature's `recipe(parent)` exposes parent and front drilling requests. It
reuses the existing cup/plate patterns, splits cup and pilot depth among the real
layers, and applies ordinary shared machining. An opening, edge, material gap or
earlier cut in the required bore rejects; it never treats the combined thickness
as sufficient evidence. The mounting support receives its paired plate holes.
Purchased F000001 hinges and F000049 plates remain owned by the parent and count
once. Layer materials and blank dimensions stay on the original child parts.

Generate the complete tree with the ordinary complete-review CLI and select
`--state <owner>/door_hinges=open` (or `closed`/`removed`).
Opening applies one generic child motion to every front piece, including any
parent placement/motion. Removal hides the child and this feature's hardware;
unregistering the feature physically restores the base build's unmachined parts.
Saved source is retained but inactive. Exact vendor CAD is required for visual
hardware; schematic test bodies are not CAD authority.

The current generated owner has one registered `door_hinges.feature`. Multiple
independent doors need distinct owners or deliberately distinct feature and
purchase identities; do not reuse IDs or duplicate a shared physical support.
The original assembly-run review command remains a slab compatibility command.
Use this explicit host path for a multi-part child.

Current geometry and review poses do not certify adhesive, retained screw
engagement, cup pilot selection, material/load suitability or full opening-sweep
clearance. Those requirements remain unresolved. A material or geometry change
requires fresh construction/evidence; an incompatible moved host rejects the old plan.
