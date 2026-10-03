# Authored Cabineo machining geometry

The reusable cutter is built directly by `CabineoCutterGeometry` from numerical
machining dimensions. No STEP, BRep, mesh, or purchased connector model is loaded
or embedded in that implementation. It describes the material removed from two
mating panels, not the purchased hardware itself.

## Preserved dimensions

The source edge is `y = 0`, its machined face is `z = 0`, and the connector centre
is `x = 0`. Positive `y` enters the source panel; negative `y` enters its mate.

| Feature | Dimension |
| --- | --- |
| Three overlapping pocket bores | Radius 7.5 mm |
| Adjacent bore intersections | x = ±5 mm |
| Rear bore centre from the source edge | 25.5 mm |
| Source pocket cutting depth | 10.5 mm |
| Custom brass-insert receiver | Diameter 9.1 mm × depth 12.5 mm |
| Receiver axis from the source face | 5 mm |

The three bore centres are derived from their radius, intersection width, and
rear datum. Clipping at the source edge separates the pocket from the receiving
panel. The receiver is a separate coaxial cylinder fused to that pocket.

These dimensions preserve the project's existing custom cutter. The receiver
was deliberately enlarged for brass threaded inserts; it must not be replaced
by the standard direct-to-wood screw hole. The insert's exact purchased identity
is not inferred from its pocket dimensions.

Before replacing the imported files, the authored geometry was compared against
the previous tool inside both panel volumes. Boolean subtraction in both
directions returned zero. Regression tests retain the actual receiver dimensions
and the source pocket's removed volume. Existing joint tests verify placement and
application to both mating panels.

This is a machining compatibility model, not a manufacturer certification or a
strength rating for a particular panel, insert, or screw combination. The normal
project validation and fabrication-readiness requirements still apply.
