# Door host interface: scope review

Reviewed 2026-09-12 on `feat/door-host-interface`, baseline `2bb1737`.
Scope: the 162-line reservation test fixture and the door host/planning/
machining/rendering boundaries. This is a responsibility review, not approval
of geometry or fabrication behavior. The reviewer changed only this report
and ran no tests; implementation and regression testing are handled separately.

**Keep the test fixture local. The one identified production ownership issue
has been resolved by moving the unchanged rigid frame into shared build tools.**

| Concern | Location | Assessment |
| --- | --- | --- |
| Fixed reservation scenario | `tests/test_panel_hardware_reservations.py:22-76` | The door frame, two support frames and dimensions describe one cabinet used by these tests. Adding the door frame completes that fixture contract; it does not create a reusable geometry engine. |
| Shared reservation behavior | same file, lines 82-158 | Node occupancy, physical envelopes and hinge/runner/shelf placement remain one coherent cross-feature concern. No external fixture consumers were found. Extraction solely to reduce line count would add indirection. |
| Resolve owned panel identities and current transforms | `door_host.py:19-85` | This belongs in `DoorHost`. It derives front, bottom, inside face, door edge and overlay from the referenced parts and declares the supported orientation. |
| Compare a saved plan with current host geometry | `door_host.py:87-98` | The agreement check belongs at the host boundary. Product hinge quantity, compatibility and drilling rules remain in their planner/recipe collaborators. |
| Consume the host in planning and machining | `door_hinge_plan.py:92-133`; `riex_nc70_machining_recipe.py:16-53` | Appropriate split: the planner selects positions; the recipe combines exact product rules with current host frames and emits shared drilling requests. |
| Place hardware and render declared parts | `riex_nc70_hardware_frame.py:32-86`; `cabinet_assembly_geometry.py:20-37` | Exact product offsets remain in the hardware resolver. The cabinet renderer should place and color already-built parts, so removing its mandatory standard-part names improves its scope. It does not assume responsibility for assembly completeness. |

Resolved ownership finding: the initial `DoorHost` imported its neutral frame
from the drawer-specific mounting-plan module. The primary agent moved
`HardwarePlacement` and `Vector3D` unchanged into
`aikea-build-units/scripts/hardware_placement.py`. Source inspection confirmed
that the class fields, transformations and axis method are unchanged, both
`DoorHost` and `DrawerHost` now import that shared module, and
`drawer_hardware_mounting_plan.py` retains compatibility imports and exports.
This removes the door-to-drawer ownership dependency while preserving one
class and one transformation implementation. No new engine was introduced.

The test fixture should remain explicitly limited to this one named cabinet.
If later cases require variable panels or differently oriented shelves, use
explicit fixture placements rather than extending name-based inference. No
separate fixture file is justified by the current consumers.
