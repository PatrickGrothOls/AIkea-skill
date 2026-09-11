# Shared hinge machining

Generated slab-door features save their drilling in `door_hinges/machining.py`.
Each hinge has a source-derived cup pattern and an explicit pair of mounting-plate
holes. The shared panel tool applies and validates both operations. Existing whole
System 32 holes are reused only after matching their geometry; absent mounting
holes are made by the declared operation.

The generated file is editable, like other construction inputs. A later generator
run preserves authored files or reports a conflict. Regenerate and review whenever
the plan, dimensions, drilling or selected hardware changes. The complete builder
retains every earlier part, child, operation and purchased item.

The standard recipe retains 5 mm diameter, 13 mm deep System 32 mounting holes for
the F000049 plate. Its source profile requires 12 mm hole depth. Cup geometry is
from F000001; the existing 2.5 mm by 10 mm cup pilot choice remains a separate
unresolved screw/material suitability requirement. Valid cutter geometry is not
manufacturing approval. Exact hinge/plate identities and opening evidence are
still required, with the purchased instances included in the feature's scope.

This slice retains the existing slab-door host convention. Custom door-host
declarations are the next migration step. Review regeneration rebuilds the host
without its old door feature, retaining other composed features, before replanning.
