# Project construction and review

Run commands through the active CadQuery environment (`direnv exec .` in this
repository). Use an active project directory; all example values must come from
that project's saved brief.

```sh
python <package>/aikea-build-units/scripts/init_furniture_design.py <project>
```

Initialization supplies current shared project contracts without choosing a layout
or overwriting differing local files. Inspect and reconcile a conflict deliberately.
Do not load an old project's private runtime to make a new build appear compatible.

The existing review/readiness CLIs locate the project through `aikea.yaml`. If that
file is absent in an authored project, create a minimal YAML mapping (`{}` is
sufficient) before the first build/evidence record. Keep the real measurements and
requirements in the authored inputs. Preserve existing YAML; this metadata file
does not require fabricated wardrobe fields or running the wardrobe calculator.

The project root builder at `assemblies/<root_id>/builder.py` exports `BUILDER`
(an object with `build()`) and a measured CadQuery `ENVELOPE` in root coordinates. Keep it as a `Workplane`
containing one solid/compound (for example `cq.Workplane("XY").box(w, d, h, centered=False)`);
do not call `.val()` on the envelope.
Use stable IDs such as `furniture_01`. A complete builder may compose registered
features; the official loader honors it. Return one `BuiltAssembly` tree with
declared parts, child placements and hardware matching the actual built members.

Each manufactured piece has one `PartSpec`, material ID and manufacturing frame.
An outline lies in local XY; +Z is stock thickness. Keep outline bounds and blank
dimensions consistent. A non-sheet rod remains its own physical item. Workplanes
contain one Shape; use a compound for multiple solids that are one real item,
not to hide separately purchased/cut pieces. Shared boards have one owner.

Standard configurators return editable recipes. Preserve their applicable checks
when using `dataclasses.replace` or composing directly. Use common local machining
and paired joint tools; [the shared contract](../../aikea-build-units/references/shared-construction.md)
contains exact examples, extension requirements and operation/evidence paths.

Declare support, attachment and movement needs independently of the operations
that may satisfy them. `requirements=None` means unassessed; an empty tuple does
not cover existing physical items. Explicit unresolved requirements stay visible.
Loose parts and floor contact need a reason. Missing selected hardware, material
compatibility or load evidence cannot be inferred from a closed solid.

```sh
python <package>/aikea-review-unit/scripts/build_furniture_design.py <project> --assembly <root_id>
python <package>/aikea-review-unit/scripts/serve_unit_review.py <project>/reviews/<root_id>.glb
```

The first command applies common construction output checks, envelope/overlap
checks and requirement reporting to any builder. Inspect the report, not only the
exit code or appearance. `construction_status: incomplete` can coexist with a
geometrically valid preview. A failed build's earlier GLB is not fresh evidence.

For registered component states, use the generic complete review command:

```sh
python <package>/aikea-review-unit/scripts/generate_complete_assembly_review.py <project>/aikea.yaml --assembly <root_id> --output <project>/reviews/open.glb --state <owner_id>/door_hinges=open
```

Select the actual registered feature ID/state from the result or manifest. The
command's `aikea.yaml` argument locates the project; it does not require a custom
design to masquerade as a legacy cabinet run. Review motion changes presentation,
not source fabrication geometry. Follow [position evidence](../../aikea-review-unit/references/construction-position.md)
for bounded contact allowances and current evidence binding. Run the existing
fabrication gate for the same root before manufacturing claims.

Count physical items with [the inventory tools](../../aikea-review-unit/references/physical-item-counting.md).
Reconcile complete tree instances and installed purchase units, then generate
sheet input from actual material/thickness/blank data. A proposed 16 mm or split-
back stock scenario stays a proposal until geometry is rebuilt and rechecked.
