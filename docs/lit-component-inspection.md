# Detailed furniture inspection

## Scope
Patrick requires an exploded view that opens up cabinets, retains visible lights
and mounted hardware, and uses bounded memory. Preserve the approved Blender
appearance in the intact view and actual CAD geometry throughout.

## Work packages
- [x] WP1: Add explicit all-panel separation while retaining hierarchical inspection.
- [x] WP1: Keep hardware and luminaire render members attached to their host panels.
- [x] WP1: Keep visible emitters and modest live illumination in inspection; no path tracer.
- [x] WP1: Test transformed grouping, exact reset, visibility and moving light positions.
- [ ] WP2: Select baked/intact and ordinary inspection assets in one viewer with resource disposal.
- [ ] WP2: Verify actual corrected cabinet, lighting, appearance and single-tab resource use.
- [ ] Review each coherent slice, record evidence and commit locally without publication.

## Current state
WP1 implemented: all-panel separation is the UI default; hardware follows its
declared panel and lights follow their moved geometry. Source intensity reduced
from1800 to15 for inspection, pending visual calibration on the corrected cabinet.
Inspection unmounts the optional path tracer. Geometry and machining remain owned
by the construction branch. Finished-view asset selection and real cabinet review
remain pending; the rejected braced-base trial must not be presented as corrected.

Validation:59 viewer tests pass,5 lighting component tests pass, production bundle
build passes, and git diff whitespace check passes. No CAD geometry was modified.

## WP1 responsibility review
Reviewed with review-code-boundaries. PASS: lighting ownership belongs to the
lighting component; the generic assembly exporter only forwards existing metadata.
InspectionGrouping owns separation policy; AssemblyPresentation applies transforms;
LightingSource derives visible transformed emitters; React owns renderer lifecycle.
No hardware-specific rules entered the exporter or generic rendering infrastructure.
Modified production files remain below150 lines (largest exporter145); no mandatory
large-file refactor report was triggered. Real-model visual verification is pending.

## Audit log
1. 2026-09-15: Patrick explicitly requested the previous finished render quality,
   cabinet-opening explosion and visible lighting without exhausting RAM. This
   authorizes these behavior changes and preserves all manufacturing geometry.
2. 2026-09-15: Keep the construction corrections on codex/cabinet-defaults. This
   viewer slice will be stacked on its completed commit before final validation.
3. 2026-09-15: WP1 tests and boundary review passed. Preserve hierarchical mode as
   an explicit choice and deep panel focus for inspecting its attached fittings.
4. 2026-09-15: Bake integration requires unique body/emitter leaf IDs under their
   shared luminaire/host path. Added those leaf identities; physical inventory
   still comes from the one purchased luminaire, never from rendered mesh count.
