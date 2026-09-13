# Exploded inspection of an existing assembly

Use the current real generated GLB and the bundled `serve_unit_review.py` viewer.
Do not write a dresser-specific explosion script, change part geometry, or
regenerate manufacturing files just to separate the pieces on screen.

Add `explode=0.65` to the viewer URL to start separated, or `explode=2` for more
space. The supported range is 0 to 3 (0–300%). The same controls are available
without the URL option:

1. **Whole assembly** separates the root parts and child assemblies. All parts
   belonging to a child move together. Mounted fittings stay with their carrier:
   cabinet-side runners with the real supports, drawer-side components and clips
   with the drawer. Do not scatter hardware independently at this level.
2. Choose a child in **Assembly or part** to inspect it alone. Its own panels and deeper
   child assemblies can then be separated. Fittings with an explicit mounting
   panel stay on that panel. Choose the panel itself to separate its fittings;
   the panel must remain visible as their reference. This works at each named
   tree level, so hardware only detaches during an explicitly deeper inspection.
3. Adjust **Separation** from 0% to 300%. Above 100%, additional spreading opens
   gaps between aligned units such as stacked drawers. Every physical part is
   available in **Assembly or part**. Alternatively, click a piece and choose
   **Inspect selected part**. A panel includes its declared mounted fittings;
   set Separation to 0% to inspect them attached, or raise it to separate them.
   A selected individual fitting is shown alone. Rotate, zoom and pan to inspect
   its faces and cuts. Names and multi-surface geometry remain intact.
4. **Restore assembly** reveals the complete original model and restores its
   exact part positions. Existing rotate, zoom and pan controls remain available.

GLTF can render one panel as many surface meshes. The viewer keeps primitives
belonging to one exported part node together. The shared complete-tree exporter
records structured inspection paths from the real assembly ownership. A
`PurchasedHardwareSpec.mounting_part_id` names its mounting panel in the same
owning assembly; set it when installing each independently represented hardware
member. The MOVENTO installer supplies its actual support and clip-rail IDs.
Physical item names, purchases, source CAD and closed placements stay unchanged.

Never infer attachments from proximity or names. Do not split or duplicate a
combined manufacturer runner model to invent separately mounted members. Preserve
its sourced component boundaries and identify any missing member authority.
Older GLBs without inspection metadata retain the `assembly__part` convention;
flat imports expose individual pieces. Those imports do not gain mounting
ownership automatically. Display labels are not manufacturing identities.

Separation is a visual layout based on original bounds. It does not establish
assembly order, collision-free removal, drawer travel, fixing access or structural
support. The exploded pose uses interactive rendering and cannot present the
visual-approval controls. A collapsed isolated child is also not the complete
assembled review. Missing purchased parts remain missing; name them explicitly
rather than treating the view as a complete assembly guide.

For the client, show the whole exploded piece and one useful component, such as
a drawer. Check that each runner and drawer-side fitting follows its declared
carrier, panels remain intact, spacing is legible and reset restores the full
model. Save actual screenshots for mobile review and keep the live viewer
available. The existing closed geometry and fabrication checks remain the only
manufacturing evidence.
