# Shared construction for drawer children

The five-panel drawer calculators are optional recipes. Their saved
`DrawerAssemblySpec` exposes explicit parts, joints, machining and requirements,
and every generated child uses `PanelAssemblyBuilder`. An authored composition
can reuse these values in `PanelAssemblySpec` or place the result as one child of
a different parent. Keep each physical panel and purchased item owned once.

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

KA 4532 with its spacer currently emits no drawer drilling because its selected
fixing details remain unresolved. MOVENTO retains its existing unmachined box
and exact declared locking-device placeholders. Hardware hydration still resolves
their exact source geometry through the existing profile-specific path.

Every recipe separately declares box joinery/bottom support, mounting and installed
movement requirements. Successfully machining a pilot does not resolve drawer
joinery or prove load capacity. Deleting a declared drilling request leaves its
mounting requirement missing. Do not remove the requirement to obtain a pass.

The child migration does not make every existing host adapter universal. Cabinet
layout still uses the current opening, side frames, reserved hardware rows and
selected product checks. Use a host only when it satisfies that documented
interface; the subsequent host migration makes those inputs and operations explicit.
Do not invent cabinet metadata on an unrelated arrangement to bypass its fit check.

See the [shared construction protocol](../../aikea-build-units/references/shared-construction.md)
and [surface drilling](../../aikea-build-units/references/surface-drilling.md).
