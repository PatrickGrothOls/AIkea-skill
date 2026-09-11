# Shared position and contact evidence

## Scope and current state

WP4c on `feat/construction-position-evidence`, based on reviewed WP4b `e09056b`.
Implementation and independent review are complete. One geometry checker handles arbitrary closed
trees; the existing wardrobe relationship check remains a compatibility check.

## Work package and tasks

- [x] Preserve full physical paths when evaluating closed geometry.
- [x] Allow intentional intersection only for two exact participants, inside an
  explicit finite region/volume bound with current registered feature evidence.
- [x] Save the declared envelope and current position evidence for any root;
  independently recompute the checks at the existing fabrication gate.
- [x] Produce common records from configured and authored review commands.
- [x] Test nested custom roots, stale evidence, valid/invalid allowances and a
  complete generic fabrication pack with the existing visual decision.
- [x] Run the `review` skill and fix/recheck its envelope-authority finding.
- [x] Commit the reviewed slice.

## Validation

- 24 focused position, contacts, custom CLI, fabrication, feature and input-evidence
  tests passed before the final review correction.
- After that correction, 10 tests passed: the source-switch regressions, fresh
  custom build-to-pack-to-decision flow and an actual generated sloped wardrobe.
  The custom approval is a synthetic test decision, not approval of Patrick's furniture.
- 11 further compatibility/contact/readiness tests passed, including the existing
  full closed-wardrobe preview API with unsaved in-memory project input. The gate
  still reads saved measurements. All nine skill packages and links verified.
- The review skill's independent testing specialist reproduced and closed the
  authority finding. Primary review found no remaining issue in this slice.
- No remote CI, push, merge or physical fabrication test is claimed.

## Audit log

1. Patrick approved bounded contact allowances and shared position checks in WP4.
   Zero-volume face contact already passes. No allowance suppresses a hardware
   family, arbitrary collision or unresolved load/motion requirement.
2. The declared envelope becomes a saved STEP validation input, bound to current
   project source and its checksum. The gate recomputes actual geometry inside it;
   a saved success flag alone is insufficient. Existing visual approval is reused.
3. The gate additionally compares the saved envelope and contact declarations to
   current root inputs or the standard measurement adapter. Updating a STEP
   checksum cannot silently enlarge the accepted boundary.
4. The configured root starts at the left base edge and carcass front. Its measured
   envelope is transformed by the already-declared left clearance and door
   thickness; this preserves the existing coordinate convention, not new geometry.
5. A fresh-process test exposed an eager dependency on the overall wardrobe input
   reader in the generic command. The configured adapter now loads inside the
   existing project runtime only when selected. The custom route remains independent.
6. The inherited 154-line fabrication test fixture received its required
   independent scope review. Its one coherent scenario and pack orchestration
   remain together; no refactor was recommended. Validation logic stays in production helpers.
7. Independent review reproduced a report switching an authored envelope to a
   larger configured measurement envelope. The current root now selects its own
   authority; an authored shape wins over a configured-source declaration. Only
   an explicit declaration enables the measurement adapter. A regression rejects
   a newly written report attempting that switch without changing the inputs.
