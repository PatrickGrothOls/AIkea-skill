# Door machining: scope review

Reviewed 2026-09-12 on `feat/door-construction-machining`, baseline `87bada6`.
The inspected `cabinet_door_hinge_review_generator.py` is 143 lines, below
150 at this snapshot. This requested review still checks its responsibility
boundaries. No production code was changed and no tests were run.

**Recommendation: retain the generator as one orchestration responsibility.**
It coordinates one door installation proposal and its review artifacts;
opening resolution, hinge planning, machining, feature persistence, hardware
placement and export already have focused collaborators.

| Concern | Generator location | Appropriate owner |
| --- | --- | --- |
| Choose the inputs for door replanning | line 65 | The generator names its owned `door_hinges.feature` exclusion; it must not implement generic feature filtering itself. |
| Resolve opening and hardware compatibility | lines 67-89 | Existing opening resolver, planner and reservation store; orchestration belongs here. |
| Generate machining and reusable door feature | lines 90-94 | Existing machining and feature-generator collaborators; do not introduce an alternate rebuild path. |
| Save installation/review evidence and closed/open views | lines 92-128 | Existing report, review-record, geometry and exporter collaborators, coordinated around the same plan. |
| Return artifact references | lines 129-140 | The result is the public output of that orchestration, not a separate responsibility requiring another file. |

The generic loader owns execution of an existing feature-composed builder.
A caller-specified exclusion belongs there: filter the exact registered
feature objects while retaining the same base builder and the order and
identity of unrelated features. Apply this within the existing project
runtime and retain normal construction-result validation. It must not encode
hinge names, reconstruct a substitute base, or drop all features to obtain an
unmachined input.

This makes the boundary explicit: the door workflow selects which owned
feature it is replacing; the loader controls composition; the existing
machining service owns cuts. Removing the previous door feature before
planning prevents its own generated cuts from becoming evidence of reusable
pre-existing machining.

No extraction is justified by this slice. If export workflows later gain
independent callers or variants, a reusable review-artifact writer may become
useful; the present closed/open pair alone does not establish that need.

Files inspected: `cabinet_door_hinge_review_generator.py`,
`cabinet_door_feature_generator.py`, `door_hinge_review_geometry.py`,
`generated_assembly_builder_loader.py`, and the generated `assembly_feature.py`.
