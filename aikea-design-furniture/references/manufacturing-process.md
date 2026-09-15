# One-face construction process

AIkea's standard structural process is three-axis CNC: choose one broad face
for each physical part to face the spindle throughout its machining. Do not flip
the part, assume edge drilling or require an angled/undercut tool approach to
make an otherwise incompatible arrangement appear complete. An explicitly chosen
different process must be recorded and qualified; never infer that change from
the appearance of a reference image.

## Plan before joining

- Save each physical part path and chosen local `<Z` or `>Z` setup face in the
  active project's manufacturing plan. Local XY is its outline; Z is thickness.
- Include every structural pocket, insert receiver, rail pilot, hinge fixing,
  handle hole and other required opening. Track unselected hardware and missing
  hole patterns as unresolved obligations; omission is not a compatible setup.
- Ordinary storage shelves use adjustable supports with actual matching bores
  and purchases. A fixed Cabineo shelf needs a deliberate recorded choice and
  underside pockets; structural floors/tops remain separate. Floor-standing
  cabinet bases use the current Korrekt feet/deck/kickboard, with no brace fallback.
- Cabinet side panels require the full usable-height System 32 grid by default,
  for both recipes and custom compositions. Reconcile its expected rows and
  columns with actual holes, including lighting and hardware interference. Any
  omission, shortened run or relocated column needs a recorded design override;
  a few shelf-support bores alone do not satisfy this default.
- Use the shared paired Cabineo construction for selected fixed sheet connections and count
  one matching brass insert per verified connector. Resolve both participants
  from their actual frames, faces and material thicknesses. No self-designed
  replacement pockets or unpaired visual connector symbols.
- Audit all connections touching a part together. Opposite-side shelf receivers,
  back/front rail attachments, and inner drawer joinery versus outer runner pilots
  can conflict even if each connection works independently. Redesign the arrangement
  or attachment; a configurator does not exempt its output from this check.
- An ordinary full through-opening can share either broad setup face. A blind
  pocket, counterbore or countersink has a required entry face. Do not turn blind
  Cabineo/insert receivers into through-holes to evade an entry-face conflict.
- Check the complete tool footprint, remaining material, edge clearances, corner
  radii and reachable depth, not only hole centres or non-overlapping solid boxes.

## Verify the actual tree

After building, run the common complete geometry/operation checks and:

```sh
python <package>/aikea-review-unit/scripts/check_panel_setups.py <project> --assembly <root-id>
```

Inspect the saved `reviews/panel-setup-audit.json`, including every part's allowed
faces and its construction hash. Every chosen face must be allowed. A conflict
or unsupported operation blocks a CNC-complete claim. Reconcile the report with
the independent required openings and purchases; this checker cannot discover
holes that the model forgot to declare. Check paired cuts, physical connectivity,
remaining receiver material and exact hardware installation separately.

A compatible report proves only declared entry-face compatibility. It does not
approve tool reach, workholding, machine capability, loads, movement or CAM.
Use the existing fabrication gate for manufacturing claims. A prototype can be
shown with its precise unresolved items and must retain `fabrication_ready: false`.
This does not waive the [complete drawer installation contract](../../aikea-build-drawers/references/complete-drawer-installation.md):
resolve runners, necessary spacers and mounting preparation before generating
drawers. Missing installation data requires sourcing or a specific user handoff,
not a box-only drawer delivered as the prototype.

## Secondary finishing

When the user permits separate router work, sanding or another finishing process,
record it as an explicit stage on the same part identities. Keep a reproducible
CNC-stage tree and its setup report, then check the complete finished tree and
retained joint material. Do not silently filter inconvenient operations from a
full-tree audit or claim a secondary profile is single-setup CNC qualified.
The shared `PanelEdgeFinishSpec` records rounding through actual part cuts; its
geometry alone does not qualify a router setup. Prefer CNC profile tooling when
the selected setup, tool and clearances support it, without assuming that they do.
