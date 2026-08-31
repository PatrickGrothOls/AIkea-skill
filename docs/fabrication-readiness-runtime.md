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

- [ ] Replace specialized drawer additions with tree-owned pose overrides.
- [ ] Keep closed geometry as fabrication authority and open poses review-only.

### WP3 - Fabrication gate

- [ ] Define machine-checkable fabrication-ready evidence.
- [ ] Reject missing geometry, placement, joints, machining, or validation proof.
- [ ] Keep visual approval as an explicit required gate.

### WP4 - Fresh combined-feature run

- [ ] Generate a fresh measured wardrobe and complete first cabinet.
- [ ] Compose drawer, door, exact hardware, and lighting through one builder.
- [ ] Build the wardrobe root, run fit/machining checks, and export GLB.
- [ ] Open the interactive viewer for visual approval.

## Current state

The recursive source architecture and reproducible source-environment contract
are complete. The exact Python, CadQuery, VTK, PyYAML, pytest, Node, and npm
versions are declared. The repository-local Python command path, 22 viewer
tests, and production viewer build pass. A completely isolated Python install
could not be retained on this machine because the volume has less than 1 GiB
free; the declarations were validated against the matching existing CadQuery
runtime through a repository-local virtual environment.

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

1. 2026-08-31 - Kept runtime locks and viewer source tooling repository-only;
   the downloadable skill will receive prebuilt static viewer assets.
