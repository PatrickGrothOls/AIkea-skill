# Shared hinge machining

Generated slab-door features save their drilling in `door_hinges/machining.py`.
Each hinge has a source-derived cup pattern and an explicit pair of mounting-plate
holes. The shared panel tool applies and validates both operations. Existing whole
System 32 holes are reused only after matching their geometry; absent mounting
holes are made by the declared operation.

The generated file is editable, like other construction inputs. A later generator
run preserves authored files or reports a conflict. Regenerate and review whenever
the plan, dimensions, drilling or selected hardware changes. The complete builder
retains every earlier part, child, operation and purchased item.

The standard recipe retains 5 mm diameter, 13 mm deep System 32 mounting holes for
the F000049 plate. Its source profile requires 12 mm hole depth. Cup geometry is
from F000001; the existing 2.5 mm by 10 mm cup pilot choice remains a separate
unresolved screw/material suitability requirement. Valid cutter geometry is not
manufacturing approval. Exact hinge/plate identities and opening evidence are
still required, with the purchased instances included in the feature's scope.

Save `DOOR_HOST = DoorHostSpec('front_id', 'support_id')` next to `SPEC` in a
custom assembly's `spec.py`. Both are actual owned parts, built with the common
panel builder. The NC70 host supports an upright slab with its back on local Z=0
and a support whose inside broad face points into the selected opening. An inset
front and either support-face orientation are supported. The named door and
support are saved in the plan, feature scope and machining; no standard part
names or cabinet dimensions are required for this route.

Load the feature-free assembly with `GeneratedAssemblyBuilderLoader.load_assembly`
using `exclude_features=('door_hinges.feature',)`, resolve its declaration through
`DoorHostLoader.load(project_root, built.spec, hinge_side)`, then pass that host to
`DoorHingePlanner.plan`. Write the resulting installation plan and call
`CabinetDoorFeatureGenerator.generate(project_root, built.spec, plan, profile)`.
The ordinary complete builder and registered door review feature build and show
the same result. The standard workflow performs these steps automatically.

Use `DoorMassEstimator.estimate(host, densities_kg_m3, coatings_kg_m2,
attached_hardware_kg=..., basis=...)` with explicit maps keyed by each physical
panel's material ID. It uses actual slab outlines or the real panels of a
multi-part front, never a filled bounding rectangle. Include coating on both
faces/edges and moving fittings/handles, with sources or stated assumptions.
Save this estimate with the door evidence and pass `mass_estimate=...` to
`DoorHingePlanner.plan`. Missing finished mass remains `None` and a compatibility
issue; no plywood density is silently substituted. An estimated mass alone does
not qualify the manufacturer's hinge count or installation load.

Custom hosts must pass relevant `PanelHardwareReservation` entries to the planner
and complete parent-level position/contact and opening checks. These reservations
use canonical support front-to-back depth and support-bottom height, even if its
local X points backwards. Standard cabinets retain the existing shelf adapter.
The host contract does not infer every structural obstacle or certify movement.

Review regeneration rebuilds the host without its old door feature and retains
other composed features. A plan with changed dimensions, overlay or mismatched
door/support fixing heights is rejected before generated files are written.
Hinge quantity is still height-based and retains a manufacturer load/count
qualification issue even when finished mass is known. Material-specific strength
and multi-part/framed front construction require their own applicable evidence.
