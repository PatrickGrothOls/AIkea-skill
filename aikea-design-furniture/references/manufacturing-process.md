# One-face construction process

AIkea's standard structural process is three-axis CNC: choose one broad face
for each physical part to face the spindle throughout its machining. Do not flip
the part, assume edge drilling or require an angled/undercut tool approach to
make an otherwise incompatible arrangement appear complete. Retain one-face
machining whenever a viable construction exists. Use the conflict-resolution
order below; a nicer or simpler part alone does not justify a second machining
face. Never infer a process exception from a reference image.

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
- When moving a carcass face or changing stock, regenerate every dependent grid,
  pin, runner/support fixing, hinge and access hole from the same panel frame.
  A correct hole pattern with stale hardware placements is an installation error.
  Check whole-tree closed contacts after these changes, including runner/front
  slabs, screw heads, shelf supports and actual foot-plate seam margins. A
  hardware-versus-wood subset does not replace the complete contact check.

## Resolve a machining-face conflict

1. Find a viable construction using one broad CNC face per physical part. Evaluate
   the actual joints, assembly sequence, hardware support and usable space; do not
   assume splitting a panel into extra pieces is automatically a viable solution.
2. Consider machining an ordinary fixing/pilot hole all the way through from that
   face when the resulting appearance, strength and fastening remain acceptable.
   Check the exact screw/head, board material, pilot diameter, thread engagement,
   edge distances and retained stock. A clearance hole does not provide the grip
   of a pilot. Keep required countersinks/counterbores on their proper entry face.
   Do not use through-machining to bypass blind precision pockets or Cabineo/insert
   receiver requirements. A passing face audit alone does not qualify the change.
3. Only when no viable one-face construction exists, record the alternatives and
   why they fail, then develop a guided second operation. Keep it explicitly
   separate from single-setup CNC evidence; never omit its holes from the audit.

### Plugging the visible exit

A through-hole may be permanently plugged on its visible side, then trimmed or
sanded flush and coated. Record the plug, depth, retention method and finishing
sequence on the same part and include the work/materials in the production package.
Keep the plug clear of required screw engagement, hardware seating and later
assembly access. Do not assume filler or a cosmetic plug restores structural
material removed by drilling; assess the perforated part and fastening separately.

Judge the finish by the hole's location and intended material. A small, neat,
detectable plug inside a drawer or another low-visibility interior can be an
acceptable design choice; it need not meet the appearance standard of an exposed
front. Painted MDF can use a filled/plugged and coated finish. Exposed veneer or
solid wood may retain a visible plug and grain mismatch; record that appearance
rather than promise an invisible repair. Show the affected face and mark the
finishing step in the user's guidance.

### Guide an unavoidable second operation

For hand drilling, design a template that locates positively on the correct part,
face and orientation, with the verified hole pattern and controlled drilling
depth. Use unmistakable part/face markings, a keyed or asymmetric fit, suitable
clamping and drill guidance; verify tool access and that the template cannot seat
in the wrong orientation. Do not describe a template as risk-free without proof.

For CNC work, design a registered flip fixture with positive stops or locating
features that constrain translation and rotation, plus a repeatable Z reference.
One zeroing hole alone does not constrain rotation. Retain the part identity,
flip transform, clamping plan and exact second-operation toolpaths. Prove the
registration and hole locations on a test piece before applying them to production.

For either route, provide visual step sheets showing the actual part, orientation,
locators, clamps, drilling depth or zeroing procedure, and verification steps.
Reconcile both operations with the final geometry, fit and strength checks. A
fixture proposal or illustration alone is not qualified machining evidence.

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
