# Closed construction position evidence

Configured and authored designs use `ConstructionPositionEvidence` and
`FurnitureGeometryCheck`. They inspect every manufactured part and purchased item
in its actual closed frame. Physical paths retain their root and `part:` or
`hardware:` kind; shortened viewer labels are not manufacturing identities.

The authored root declares `ENVELOPE` as one CadQuery shape and may declare
`CONTACT_ALLOWANCES`. The standard configurator adapts the saved measured space,
including its sloped top and the existing root datum, to the same envelope
interface. Its generated root explicitly declares
`ENVELOPE_SOURCE = "configured_measurements"`. An authored `ENVELOPE` takes
precedence; a saved report cannot choose a different source. Regenerate an older
configured root through the conflict-preserving generator before using this
evidence path. It retains the older wardrobe relationship check as an additional
compatibility check; an authored root does not need a base/cabinet taxonomy.

`build_furniture_design.py <project> --assembly <root-id>` produces the viewer
and `assemblies/construction-position-check.json`, plus the declared envelope STEP.
The fabrication gate reimports that envelope, compares it with current declared
inputs, and recomputes actual fit/intersections. It also verifies current input
hashes and exact physical paths/bounds. Editing a saved success flag, removing an
item, or enlarging the exported envelope cannot substitute for rebuilding.

## Uncertain source CAD

The shared checker compares intersection volume with the material removed from
each participant. Contradictory results are `uncertain_intersections` and make
geometry invalid. They establish neither a measured collision nor clearance.
Retain the exact source and reported gap; do not loosen tolerances or invent a
contact allowance to clear uncertainty. A valid source solid alone is insufficient.

## Intentional contact

Touching faces with no positive-volume overlap need no allowance. Positive-volume
intersections fail unless the root supplies a `ContactAllowanceSpec` from
`assemblies.contact_allowance` with all of:

- A stable `allowance_id` and exactly two complete `subject_paths`.
- Finite `minimum_mm` / `maximum_mm` bounds in the root frame.
- A verified positive `maximum_volume_mm3` for the permitted intersection.
- The exact owning `evidence_feature` path and an explanatory `basis`.

The complete intersection must fit inside both the region and volume limit.
One declaration cannot cover a hardware family or a different pair. For example,
a verified threaded interface can describe the exact insert/panel intersection;
derive its region and limit from that interface's checks, never an arbitrary
large box intended to hide a collision.

The owning feature registers its affected panels and purchased hardware through
`CabinetFeatureManifest`. Its existing current manufacturing report includes an
identical JSON contact declaration in `contact_allowances`, passed applicable
checks, current STEP hashes and `construction_sha256`. Both participants must
belong to that scope. Use `ConstructionContactEvidence.records(allowances)` to
serialize typed declarations consistently. Missing, stale or differently bounded
evidence leaves the intersection unresolved. Removing a feature must remove its
owned allowances as well as its machining/purchases.

## A fabrication review for any root

Run `build_furniture_design.py <project> --assembly <root-id> --fabrication-review`
to create a proposal using the existing closed-model decision mechanism. It uses
the compatibility filename `assemblies/full_wardrobe_review.glb` for any furniture
root. It returns `review_record` only when current shared geometry is valid.
The standard full-review command likewise exposes `construction_position_status`
and `construction_position_check`; invalid geometry exits 2, retains an inspection
GLB and withholds a proposal. A skipped open/presentation check cannot reuse an
older valid report to produce a new fabrication proposal.

Serve an eligible model and record through the existing viewer. A decision needs
a current valid schema-2 position record and matching construction hash. Missing,
invalid or stale evidence makes an already-open session return HTTP 409, while
the historical proposed/approved record stays unchanged. Regenerate the relevant
closed checks before requesting another decision. This is visual review only;
the complete fabrication gate below still determines readiness.

After the client's decision, run `check_fabrication_readiness.py
<project>/aikea.yaml --assembly <root-id>`. The same complete parts, material,
hardware, machining, feature, position and current-approval checks still apply.
A visually valid assembly can remain blocked by unresolved support, load, motion,
product or manufacturing requirements. Review poses, hidden items and overlays
do not produce new closed-construction position evidence.
