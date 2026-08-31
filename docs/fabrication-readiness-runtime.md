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
feature evidence, validation, or stale visual approval. The exact Python,
CadQuery, VTK, PyYAML,
pytest, Node, and npm versions are declared. The repository-local Python command
path, 22 viewer tests, and production viewer build pass. A completely isolated
Python install could not be retained on this machine because the volume has
less than 1 GiB free; the declarations were validated against the matching
existing CadQuery runtime through a repository-local virtual environment.
The clean proof run completed the first cabinet through the recursive physical
tree: three drawer children, six exact Hettich runner assemblies, three shelves,
one recessed light, one machined left-hand door, and five exact Riex hinge/plate
pairs. The packaged command exported 40-item closed and exact door-open GLBs and
opened both interactive viewers. Feature-state selectors use the full assembly-
tree path, so repeated child IDs in different branches remain unambiguous.
The command now writes a checksum-bound `.review.json` beside each GLB with every
rendered item and its placed bounds. This moves the final generic inspection out
of client projects; registered feature reports remain the fit evidence until the
separate fabrication gate can grant manufacturing authority.
Earlier stopped runs exposed and closed three behavioral gaps: door hand was
being inferred from room position, another client project could be opened as an
example, and missing generic review evidence encouraged local inspection
scripts. The entry contract, fresh-project isolation rule, and packaged report
now prevent those paths. The remaining work begins only after visual approval:
repeat the approved cabinet architecture, produce the full manufacturing pack,
validate the complete wardrobe, and bind approval to its exact closed GLB.

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

1. 2026-08-31 - Kept runtime locks and viewer source tooling repository-only;
   the downloadable skill will receive prebuilt static viewer assets.
