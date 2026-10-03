# Match appearance to the physical build

Read before assigning source materials for a Blender presentation. The saved
construction and finish choices are the authority for both the render and the
parts, material and finishing lists. A successful bake only preserves its input;
it cannot establish that an invented source material represents the real stock.

## Resolve faces and cut edges

For every panel, identify its selected stock, broad-face surface, exposed core,
grain direction and treatment of each exposed edge from the active specification.
Use the material's physical construction: exposed plywood shows its laminated
core; bare MDF shows its fibre core; veneered boards expose their underlying core
unless a different edge treatment is specified. Do not treat an edge as merely a
lighter version of the face grain. Do not infer an edge treatment from the face
coating, a normal direction, a generic wood texture or an attractive reference.

Absent edge-treatment information is unresolved. Resolve it before presenting a
finished appearance. A colour swatch without the relevant core structure cannot
stand in for a finished exposed-plywood edge.

Edge banding, lipping, fillers and opaque coatings may appear only when specified
for that surface and included in the corresponding material/finishing quantities
and operations. Account for their physical thickness where it changes dimensions
or fits. Roundovers and other profiles must already exist in the checked CAD and
manufacturing plan; shaders must not add them or conceal construction gaps.

## Evidence and review

Retain the mapping from each part/surface to its saved stock and treatment beside
the source-material GLB. Record the reference for the face and core appearance:
an actual sample or supplier reference when available, otherwise a clearly
identified representative material with the correct construction and treatment.
Generic stock does not establish an exact veneer species, ply count, colour,
grain pattern or coating sheen. Do not claim an exact physical colour match from
screen appearance; natural material, finish and lighting vary.

Before delivering the finished presentation:

- Reconcile visible surfaces against those saved choices and the material and
  finishing lists. Any unselected treatment or missing core appearance blocks
  finished-appearance approval; correct the source material and rebake.
- Inspect a face-to-cut-edge close-up under neutral lighting as well as the
  studio overview. Check the selected treatment remains legible after baking.
- Check the original-material inspection view uses the same stock/treatments;
  switching views must not substitute another material or disguise bare edges.
- Keep unresolved material choices explicit. A labelled material study can show
  alternatives, but must not be delivered as the specified finished product.

The current automated geometry/coverage gate does not validate this material
mapping or the physical sample. These are required source and visual review checks;
do not describe them as an existing automatic material-fidelity guarantee.
