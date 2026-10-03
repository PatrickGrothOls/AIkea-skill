# Shared construction for drawer children

The five-panel drawer calculators are optional recipes. Their saved
`DrawerAssemblySpec` exposes explicit parts, joints, machining and requirements,
and every generated child uses `PanelAssemblyBuilder`. An authored composition
can reuse these values in `PanelAssemblySpec` or place the result as one child of
a different parent. Keep each physical panel and purchased item owned once.

These are intermediate construction recipes, not permission to build a box-only
drawer. Every route must follow the
[complete installation contract](complete-drawer-installation.md) before drawer
generation, including exact runners, mounting cuts and any needed spacers.

`DrawerPartSpec` retains its local outline and material identity as well as its
dimensions and frame. Empty material means unresolved selection; set the actual
material on each part. An overall price scenario does not change the construction.
When adapting a part, update its outline, size, frame and dependent operations
together. Generated-file conflict checks preserve authored modifications.

For the selected KA 5332 profile, the recipe emits one `SurfaceDrillingSpec` for
each drawer side. Their hole IDs, dimensions and frames are saved in `spec.py`,
and the common builder retains corresponding cuts. The recipe uses the selected
profile's dimensions; a later build does not silently substitute a default cutter.
The opposite surface is expressed by the existing local-to-parent frame.

KA 5332 host fixings are saved as `HOST_MACHINING` in `drawer_installation.py`,
with separate `HOST_REQUIREMENTS`. Each selected profile emits explicit holes in
both host sheets and records any exact System 32 hole reuse. The feature appends
these requests and cuts through `PanelMachiningFeature`, preserving earlier cuts,
children and purchases. The complete pattern is independently verified. Editing
or removing a drilling request does not remove its required-work declaration.

For an authored four-sided MOVENTO installation, the new
[panel installer](movento-panel-installation.md) composes the drawer, runners,
clips, host preparation and panel joinery together. It is an engineering
candidate with source-fit and material qualification still open. Use that owner
when developing this construction; do not use its intermediate panel helper alone.

KA 4532 with its spacer currently emits no drawer drilling because its selected
fixing details remain unresolved. MOVENTO retains its existing unmachined box
and exact declared locking-device placeholders. Hardware hydration still resolves
their exact source geometry through the existing profile-specific path.
These gaps block complete drawer generation and fabrication; do not use either
recipe as a fallback when its mounting preparation is still missing. Resolve
and implement the selected installation before delivering or repeating it.

Every recipe separately declares box joinery/bottom support, mounting and installed
movement requirements. Successfully machining a pilot does not resolve drawer
joinery or prove load capacity. Deleting a declared drilling request leaves its
mounting requirement missing. Do not remove the requirement to obtain a pass.

The [drawer host interface](drawer-host-interface.md) lets the same recipes use
actual supports and clear space in a custom parent. Standard cabinets adapt to
that contract. Respect its upright-face boundary and the remaining host-aware
proof work; do not invent cabinet metadata or bypass a failing mounting check.

See the [shared construction protocol](../../aikea-build-units/references/shared-construction.md)
and [surface drilling](../../aikea-build-units/references/surface-drilling.md).
