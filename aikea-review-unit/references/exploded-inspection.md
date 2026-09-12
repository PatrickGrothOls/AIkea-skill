# Exploded inspection of an existing assembly

Use the current real generated GLB and the bundled `serve_unit_review.py` viewer.
Do not write a dresser-specific explosion script, change part geometry, or
regenerate manufacturing files just to separate the pieces on screen.

Add `explode=0.65` to the viewer URL to start separated. It is a fraction from 0
to 1. The same controls are available without the URL option:

1. **Whole assembly** separates the root parts and child assemblies. All parts
   belonging to a child move together.
2. Choose a child in **Assembly** to inspect it alone. Its own panels and deeper
   child assemblies can then be separated. This works at each named tree level.
3. Adjust **Separation** from 0% to 100%. Click a piece to display its exported ID.
4. **Restore assembly** reveals the complete original model and restores its
   exact part positions. Existing rotate, zoom and pan controls remain available.

GLTF can render one panel as many surface meshes. The viewer keeps primitives
belonging to one exported part node together. Named tree grouping follows the
existing `assembly__part` export convention. Flat imports still expose individual
parts. Displayed names are inspection labels, not replacements for complete
manufacturing identities or a purchased-hardware manifest.

Separation is a visual layout based on original bounds. It does not establish
assembly order, collision-free removal, drawer travel, fixing access or structural
support. The exploded pose uses interactive rendering and cannot present the
visual-approval controls. A collapsed isolated child is also not the complete
assembled review. Missing purchased parts remain missing; name them explicitly
rather than treating the view as a complete assembly guide.

For the client, show the whole exploded piece and one useful component, such as
a drawer. Check that panels remain intact, spacing is legible and reset restores
the full model. Save actual screenshots for mobile review and keep the live
viewer available. The existing closed geometry and fabrication checks remain
the only manufacturing evidence.
