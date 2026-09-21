# Require verified Blender presentations

## Scope

Enforce the user's required Blender presentation at the shared viewer boundary.
The original material model remains available only for open/exploded inspection.
Do not change furniture geometry, materials, machining or fabrication approval.

## Current state

Implemented a shared session gate that requires passing Blender presentation,
coverage and geometry reports with matching immutable model hashes, approved
4096 atlas/16-or-more samples and unchanged 0.002 mm geometry tolerance. The
browser also rejects an unbaked or incomplete model pair. No bypass flag exists.
The skill's delivery instructions and bundled viewer have been updated.

47 focused Python tests and 67 viewer tests passed; the viewer build, skill
metadata and 11-skill package checks passed. The actual raw wardrobe file from
the previous drawer review was rejected by the CLI before opening a server.
Positive gate tests use explicitly synthetic reports; no new furniture bake or
visual-quality approval is claimed. Existing Blender engine tests are unchanged.

## Work packages

### WP1: Enforce the presentation contract

- [x] Require passing bake evidence and hashes matching both served snapshots.
- [x] Require approved presentation quality and existing coverage/geometry checks.
- [x] Reject raw CAD and incomplete asset pairs before opening the viewer.
- [x] Update skill commands to use the required bake workflow.

### WP2: Validate and record

- [x] Test raw, missing, failed, stale and valid presentation evidence.
- [x] Retain asset switching and immutable approval behavior.
- [x] Validate the skill package and review the diff.
- [x] Commit the focused change.

## Audit log

- 2026-09-21: User explicitly requires the skill to allow only Blender-backed
  presentation. A hard viewer gate implements that existing intent instead of
  relying on an agent remembering prose. Simplified inspection remains subordinate
  to a verified presentation, as already agreed for moving parts.
- 2026-09-21: Kept approval authority tied to the displayed primary artifact and
  construction evidence. Bake verification does not grant fabrication approval.
  Tests preserve immutable serving, stale-record rejection and decision tokens.
- 2026-09-21: The initial dependency installation could not write npm cache data
  in the sandbox. The authorized retry succeeded; dependency versions are unchanged.
