# Structural-base recipe

The existing sheet base is an optional dimension recipe over `PanelAssemblyBuilder`.
It is useful when the design calls for a segmented deck supported by rails and
braces. Other support arrangements can use the same construction contracts.

## Inputs and placement

`BaseTaxonomyBuilder` takes the cabinet spans, depth, height, panel thickness and
plinth-front/recess choice. It divides long decks and rails using the existing
CNC work area and calculates brace locations with the existing construction
profile. Its output passes through the same part-placement resolver and spec
renderer as the rest of the generated run.

The resulting `BaseAssemblySpec` contains explicit part outlines/sizes and
`local_to_parent` frames, paired joints, requirements and `machining=()`.
Empty local machining means no implicit shelf grid or drilling selected by a
part's name. Add only supported, explicit operations when adapting the recipe.

In the configured wardrobe, the root places the base alongside its other children.
A custom parent can wrap the same result in `BuiltChildAssembly` using its declared
frame, or use its parts/joints in `PanelAssemblySpec`. Keep every physical panel
owned once; do not copy a shared deck into both the base and a cabinet inventory.
Preserve requirements, placements, children and purchases when adapting the spec.

## Effects and evidence

Brace-to-rail Cabineo joints machine both participants and contribute one connector
and one insert per occurrence through the existing inventory reconciliation.
Deck attachments, module seams and unsupported support decisions stay declared
and unresolved. A valid set of cuts does not establish load capacity, anchoring,
floor suitability or the missing connection mechanism.

All generated assembly and individual-part entry points use the complete shared
construction result. Regenerating a saved project uses its generated-file hashes;
an authored change stops regeneration before files are overwritten. Preserve and
reconcile older unrecorded builders instead of guessing their provenance.

Removing the component removes its owned parts, joints, cuts and purchases from
the composed tree. Requirements on other owners that still reference it must be
revised explicitly; they should become missing-work findings if left behind.
Do not remove those requirements simply to obtain a passing check.

Adjustable purchased feet are a separate component. Replacing the sheet support
requires the chosen mounting interface, screw/receiver checks and support evidence;
this recipe does not imply that a particular leg can support the result.
