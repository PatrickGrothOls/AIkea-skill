# Drawer bays in configured and custom furniture

A drawer recipe needs two actual support panels and clear space. It does not
need the parent to be registered as a wardrobe, cabinet or seating design.

Standard cabinet inputs are adapted automatically. For a custom parent, save an
explicit declaration beside `SPEC` in `assemblies/<parent-id>/spec.py`:

```python
from drawer_host import DrawerHostSpec

# SPEC is this parent's PanelAssemblySpec, with these two owned physical panels.
DRAWER_HOST = DrawerHostSpec(
    left_part_id="support_a",
    right_part_id="support_b",
    front_mm=50,
    inside_depth_mm=564,
    bottom_mm=132,
    top_mm=932,
)
```

The numbers illustrate an interface, not recommended furniture dimensions. All
limits are in the local parent frame: X across, Y into the opening, Z up. The
panels must declare their real `inside_face` and `local_to_parent`; the recipe
reads their actual inside X coordinates. It supports opposing upright broad
faces with each panel's local Y pointing up. Sloped panel outlines are allowed,
subject to actual drilling and clearance checks. Place the whole parent within a
larger arrangement through its ordinary child frame. Tilted runner installation
requires a separately supported interface.

Use the existing selected-runner generator with this parent's assembly ID.
The generator installs the same manifest-based `complete_builder.py` used by
standard cabinets, preserving differing authored files through the existing
conflict check. Use that complete entry point in an authored parent composition
so its declared features are included. The five-panel drawer remains one child;
physical support panels are retained once under the parent.

For direct in-memory use, construct `DrawerHost(SPEC, DRAWER_HOST)` and pass it to
the existing drawer planner. `DrawerBoxPlanner` still accepts just clear width,
depth and a selected sizing profile when only the box recipe is needed.

KA 5332 selects a physical height shared by both panel grids, maps reservations
to the actual support IDs and frames, and transforms the selected fixing pattern
into each panel. An offset opening need not reuse the panel's front grid column;
exact-hole reuse is recorded only when its geometry matches. KA 4532 keeps the
cabinet-front and drawer-front inputs explicit; its cabinet-front value must
match `DRAWER_HOST.front_mm`. Its longer screw and pilot remain unresolved.
MOVENTO keeps its selected source hardware and locking-device ownership.

Changing the host, selected hardware or drawer layout requires regeneration and
fresh review. Confirm body/host clearance, exact hardware mounting and movement;
the fit rectangle alone does not certify an unobstructed sweep or sufficient
load support. Existing KA 4532 proof helpers still need the next host-aware proof
slice before they can qualify renamed or offset custom supports. Treat that as
unresolved evidence, not as permission to bypass a failing check.
