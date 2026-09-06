# Fabrication readiness runtime

## Scope

Make the repository reproducible for contributors and prove the recursive
assembly architecture on one fresh combined-feature project. The public skill
package keeps prebuilt viewer files; source-development locks remain repository
only.

## Workpackages and tasks

### WP1 - Reproducible source environments

- [x] Pin the supported Python version and Python dependencies.
- [x] Confirm the viewer Node version and committed package lock.
- [x] Add one documented setup and verification command path.

### WP2 - Remaining review migration

- [x] Replace specialized drawer additions with tree-owned pose overrides.
- [x] Keep closed geometry as fabrication authority and open poses review-only.

### WP3 - Fabrication gate

- [x] Define machine-checkable fabrication-ready evidence.
- [x] Reject missing geometry, placement, joints, machining, or validation proof.
- [x] Keep visual approval as an explicit required gate.
- [x] Close independent-review false-green probes against saved evidence.

### WP3.1 - Exact material authority

- [x] Block fabricated parts without an explicit authoritative material ID.
- [ ] Add exact user-selected cabinet, door, back, base, and drawer material IDs
      to the project input and generated part contracts.
- [ ] Regenerate the target project after the maintainer confirms those products.

### WP4 - Fresh combined-feature run

- [x] Generate a fresh measured wardrobe and complete first cabinet.
- [x] Compose drawer, door, exact hardware, and lighting through one builder.
- [x] Export every feature state through the reusable recursive review command.
- [x] Open the closed and open interactive viewers for visual approval.
- [ ] After approval, repeat the approved construction through the wardrobe root,
      run fabrication checks, and export the complete wardrobe GLB.

## Current state

The recursive source architecture, reproducible source-environment contract,
and generic review-pose layer are complete. Any assembly subtree can now be
moved or hidden by path, and non-authoritative overlays attach through an owner
path. The wardrobe renderer contains no drawer-specific branch. Closed saved
frames remain fabrication authority. The fabrication gate now rejects incomplete
tree geometry, hardware, joints, machining, STEP and DXF exports, BOM, cut list,
feature evidence, validation, or stale visual approval. STEP solids and DXF
topology are compared to built geometry; feature evidence has exact owner-relative
part scope; position evidence carries the complete current-tree fingerprint; and
approval must match a freshly rebuilt canonical closed GLB. Invalid command runs
replace any old ready report, while viewer decisions serialize across processes
and always serve immutable startup bytes. The exact Python, CadQuery, VTK, PyYAML,
pytest, Node, and npm versions are declared. The repository-local Python command
path, 347 Python tests, 72 subtests, 23 viewer tests, and production viewer build
pass. A completely isolated
Python install could not be retained on this machine because the volume has
less than 1 GiB free; the declarations were validated against the matching
existing CadQuery runtime through a repository-local virtual environment.
The clean proof run completed the first cabinet through the recursive physical
tree: three drawer children, six exact Hettich runner assemblies, three shelves,
one recessed light, one machined left-hand door, and five exact Riex hinge/plate
pairs. The packaged command exported 40-item closed and exact door-open GLBs and
opened both interactive viewers. Feature-state selectors and manifest resolution
now use the full generated assembly lineage. Wardrobe-root reviews find sibling
cabinet packages, while repeated child IDs resolve through their parent paths.
The command now writes a checksum-bound `.review.json` beside each GLB with every
rendered item and its placed bounds. This moves the final generic inspection out
of client projects; registered feature reports remain the fit evidence until the
separate fabrication gate can grant manufacturing authority.
Earlier stopped runs exposed and closed three behavioral gaps: door hand was
being inferred from room position, another client project could be opened as an
example, and missing generic review evidence encouraged local inspection
scripts. The entry contract, fresh-project isolation rule, and packaged report
now prevent those paths. Exact material identity is deliberately not inferred
from thickness, role, or BOM prose: current generated projects remain blocked
until the selected material IDs are propagated into every generated part
specification. After that input is confirmed, the remaining project work is to
regenerate, repeat the approved cabinet architecture, produce the full
manufacturing pack, validate the complete wardrobe, and approve its exact closed
GLB.

## Audit log

- 2026-08-31: The isolated CadQuery run exposed a stale 56 mm rear-clearance
  assertion. The complete 520 mm drawer depth includes its 490 mm clear depth
  plus 15 mm front and back sheets, leaving 26 mm behind an 18 mm inset drawer
  in the 564 mm cabinet interior. The saved recursive frame is authoritative.
- 2026-08-31: The required separation-of-concerns review found the 166-line
  end-to-end drawer wardrobe test coherent as one expensive integration fixture;
  no split is warranted for the one corrected physical assertion.
- 2026-08-31: Pinned Python 3.10.16, CadQuery 2.4.0, VTK 9.2.6, PyYAML 6.0.2,
  pytest 9.0.1, Node 24.4.1, and npm 11.4.2. Node remains repository-only.
- 2026-08-31: Replaced cabinet-specific review additions with generic tree
  motions, exact-item/subtree visibility, and owner-frame overlays. Open drawer
  travel is presentation-only; closed saved frames remain physical authority.
- 2026-08-31: The required scope review found the 153-line drawer review
  generator coherent as one delegated application workflow; no split is
  warranted unless result mapping grows into a separate responsibility.
- 2026-08-31: Defined fabrication readiness as the conjunction of the closed
  recursive physical tree, a complete per-part manufacturing pack, valid
  feature and position evidence, and approval bound to the exact GLB checksum.
- 2026-08-31: Generalized the prebuilt viewer decision panel so the client can
  approve either door-opening proposals or the exact closed fabrication model.
- 2026-08-31: The first blind combined-feature run exposed an instruction-order
  leak: the entry router described a right-hinged first door before loading the
  door builder. Repeated the already approved left-hand invariant at the router
  boundary and added a focused regression check; no construction policy changed.
- 2026-08-31: The properly isolated rerun proved generic physical composition
  but invented project-local approval composition and fit scripts. Added an
  optional feature-review registration and one recursive review command so a
  feature owns only its state contribution and the skill owns orchestration.
- 2026-08-31: The first direct recursive-review invocation exposed an eager
  CadQuery import before runtime handoff. Deferred the implementation import to
  the command boundary so a clean project can reach the packaged CAD runtime.
- 2026-08-31: Full regression found one stale viewer test still naming the
  superseded door-only panel. Pointed it at the generic review panel and retained
  assertions for both the door and fabrication decision copies.
- 2026-08-31: Made review discovery recursive and state selectors path-scoped.
  This preserves generic composition when nested branches reuse local child IDs.
- 2026-08-31: A fresh-run audit caught another project being opened for lighting
  placement. Strengthened the package-wide isolation contract: another client
  project is never an input, even as an apparent example.
- 2026-08-31: The clean proof run used the recursive GLB command but invented a
  local bounds inspector. Added the same item-and-bounds manifest to the packaged
  command and prohibited local inspection or collision scripts during review.
- 2026-08-31: The resumed clean proof used only packaged assembly commands,
  produced checksum-matched closed and open reports for all 40 rendered items,
  and opened both interactive viewers. This completes the first-cabinet visual
  gate; it does not grant fabrication authority to the unrepeated wardrobe.
- 2026-09-01: the maintainer directed repair of every failed independent review.
  Extracted feature discovery from builder execution and resolved manifests by
  generated assembly lineage, closing sibling-cabinet and repeated-ID gaps.
- 2026-09-01: Limited the legacy drawer overlay to replacing its own runners and
  locking devices. Door and lighting hardware now remain in combined reviews.
- 2026-09-01: Made every motion, hidden item, hidden subtree, and overlay owner
  prove its path against the closed tree before hardware or review geometry runs.
- 2026-09-01: Made recursive review reports validate the GLB header and length,
  exact checksum, unique named positive-volume parts, finite placed bounds, and
  feature states before writing `status: valid`.
- 2026-09-01: Replaced non-empty-file fabrication checks with real CAD checks.
  Each STEP must boolean-match its built local solid; each DXF must parse to a
  closed face with the same millimetre footprint. Placeholder and stale exports
  now block readiness.
- 2026-09-01: Made BOM, cut-list, and machining coverage exact: duplicates,
  extras, wrong quantities, dimensions, hardware identity, and unresolved joint
  operations now block. Position reports require real checks and recursive
  feature evidence must checksum-bind its affected STEP artifacts.
- 2026-09-01: Removed approval persistence from the generic wardrobe renderer.
  Only the explicit full-wardrobe command now issues a proposal, and only for
  its canonical all-closed result.
- 2026-09-01: Bound viewer decisions to one validated immutable GLB snapshot.
  The loopback POST now requires its ephemeral token, exact same-origin request,
  and JSON media type; atomic persistence records the served checksum and refuses
  stale or already-decided proposals.
- 2026-09-01: Full regression exposed the legacy Blum runner IDs as
  `runner_left` and `runner_right`, not drawer-prefixed IDs. Corrected the
  drawer overlay ownership filter while retaining door and lighting hardware.
- 2026-09-01: The second independent review found same-bounds DXFs, unrelated
  feature STEP evidence, and weak position records. DXF topology now matches the
  authoritative blank; feature manifests declare exact affected parts; and saved
  position data must have complete structure and the current tree fingerprint.
- 2026-09-01: Bound closed-model approval to a freshly regenerated canonical GLB
  from the current tree. Structurally empty scenes, stale frames, duplicate tree
  paths, missing material identity, and stale ready reports now block.
- 2026-09-01: Replaced in-process viewer locking with a stable sidecar file lock
  and removed project files from static resolution. Concurrent processes cannot
  both decide, and encoded model routes return only immutable startup bytes.
- 2026-09-01: The material-contract audit confirmed generated specs expose
  thickness but not exact board identity. The gate blocks safely; selected
  product IDs must be propagated separately instead of inferred or generalized.
- 2026-09-01: The required 157-line drawer generator test review separated
  `DrawerLayout` identifier validation from the generator integration contract.
- 2026-09-01: The repeated independent review found fabrication feature scope
  still accepted one unique shallow suffix. Matched its owner rule to the review
  loader: only full lineage or one explicit outer-root segment may be omitted.
- 2026-08-31: Kept runtime locks and viewer source tooling repository-only;
   the downloadable skill will receive prebuilt static viewer assets.
