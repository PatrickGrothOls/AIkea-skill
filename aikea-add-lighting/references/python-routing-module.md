# Python lighting route

Use `LightingRouteSpec` and `RoutedLightingFeature` for a recessed light with a
rear cable relief and an optional connector pocket. This composes with the same
assembly feature path as ordinary lighting; do not also add the old lighting
feature for this run, because that would duplicate both its cut and purchase.

## Coordinate contract

- `face` is the part's chosen `<Z` or `>Z` broad machining face.
- `front_edge_mm=(start, end)` names an actual straight boundary segment in that
  face's coordinates from `PartFaceFrameBuilder`. The left normal of this
  directed edge points into the panel. Reverse or transform coordinates when
  changing faces; they are not global assembly coordinates.
- `inset_mm` locates the route centerline behind this front edge. End margins
  trim the usable route. Endpoints may describe an oblique edge; no global
  vertical/horizontal assumptions are used.
- `connector_end` is `none`, `start` or `end`, relative to the directed edge.
  A connector needs an explicit `ConnectorPocket`; `none` forbids one.
- Pocket dimensions are the installed, clearanced envelope in route axes,
  including tool corner radii. `light_setback_mm` is the distance from that
  route end to the light body. It need not equal the pocket length.
- `cable_depth_mm` is **total depth from the face**, not extra depth. The cable
  channel is narrower than the profile seat so shoulders remain. Check its
  usable space below the profile against actual insulated wires and bending.
- `minimum_stock_mm` is an explicit design input, not a verified strength rating.
  Real outlines and prior machining are checked, but stock/material/load and
  supplier retention requirements still need qualification.

The profile seat extends one cutter radius beyond each light endpoint to avoid
putting a rectangular light into uncut rounded corners. Reserve this overrun in
the end margins; actual profile ends and connectors still need a fit check.

## Generated assembly feature

Save the selected route next to its owning part/feature. For example, in the
owning assembly's `lighting/feature.py`:

```python
"""Scope: Apply the saved routed lighting selection to this assembly."""
from routed_lighting_feature import RoutedLightingFeature
from .plan import ROUTE

FEATURE = RoutedLightingFeature(ROUTE)
```

`plan.py` imports `LightingRouteSpec` and `ConnectorPocket` from
`lighting_route_spec` and declares `ROUTE` with the selected product dimensions.
Register `lighting.feature` in the existing feature manifest and review it from
`complete_builder`. The shortened light body, purchase length and emitter all
use the same resolved run. Service requirements remain unresolved.

For lower-level assembly composition:

```python
from lighting_route import LightingRoute
from panel_machining_feature import PanelMachiningFeature

resolved = LightingRoute().build(host_part_spec, ROUTE)
machined = PanelMachiningFeature().apply(assembly, (resolved.machining,))
light_plan = resolved.light_plan
```

That lower-level path only machines the panel. Use `RoutedLightingFeature` when
the purchased light and its review geometry are required too.

## Reproducible dimensional example

From the allowed project root, run `examples/routed_lighting_coupon.py` using its
direnv-managed CadQuery runtime. It exports STEP coupons for `none`, `start` and `end`, with a JSON
material-removal/setup report:

```sh
direnv exec . python <package>/aikea-add-lighting/examples/routed_lighting_coupon.py <output-folder>
```

The example is complete runnable Python. Every hardware dimension is a synthetic
test value, explicitly unrelated to a qualified Domus product. It illustrates
how to declare the face, edge, offsets and pocket; do not copy its numbers into
a manufacturing order. Domus compatibility and cable/profile seating are pending.

## Wiring boundary

For the approved separate-feed arrangement, only the slope uses a connector
pocket. The right-side light uses `connector_end="none"`; its connector is under
the base. This module owns one host part. It does not yet generate a cross-panel
cable bend, the side-to-base transition, base drilling or electrical distribution.
Those must be composed from one shared connection frame and checked through
every crossed board before claiming a continuous installable route. See
[base cable routing](base-cable-routing.md).

The common `stepped_surface_recess` unions its intentional overlapping regions
once. Existing unrelated holes/joints cannot silently become part of the recess:
the common construction checks still reject those collisions. Validate on the
actual built parts, and keep fabrication readiness false until installation,
tool reach, workholding and supplier fit are qualified.
