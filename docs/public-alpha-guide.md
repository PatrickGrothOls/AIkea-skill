# Public alpha documentation and privacy cleanup

## Scope

Describe the tested alpha honestly, provide a first-project entry point, and
remove personal project handovers from the source tree intended for publication.
Preserve private development history locally. Public history cleanup is a
separate release operation after the final source tree is verified.

## Workpackages and tasks

### WP1 - Public guide

- [x] Describe working capabilities and the current fabrication limitation.
- [x] Explain local manufacturer-CAD acquisition and the unresolved spacer fixings.
- [x] Add a first-project prompt and tested-platform boundary.
- [x] Link bundled license notices and explain safe bug-report inputs.

### WP2 - Personal-content cleanup

- [x] Replace the old personal architecture handover with reusable contracts.
- [x] Remove personal-name references from development and evaluation records.
- [x] Verify tracked files contain no former personal paths, room names, or email.
- [x] Review the documentation diff for a coherent checkpoint.

## Current state

Public documentation describes the existing implementation and its known gaps.
The large architecture record now retains its reusable design contracts without
the old personal room and workstation handovers. The existing historical Git
objects remain local and are not suitable for the eventual public snapshot.
The subsequent cutter replacement preserves the enlarged brass-insert receiver
while removing the imported STEP inputs; see `authored-cabineo-cutter.md`.

## Audit log

1. 2026-09-06 - The user authorized execution of the public-release review fixes,
   including personal-content cleanup and an honest description of alpha limits.
2. 2026-09-06 - The user clarified that the connector's female cutter was enlarged
   for brass threaded inserts. Documentation now preserves that requirement;
   substituting a standard wood-screw hole would change the user's design.
3. 2026-09-06 - Generated `PartSpec` still lacks `material_id` while the fabrication
   checker requires it. The guide records that observable gap rather than
   implying that invoking the checker completes manufacturing work.
4. 2026-09-06 - The authored cutter now reproduces the existing panel cuts.
   The release snapshot will contain neither the imported inputs nor the old
   private development history.
