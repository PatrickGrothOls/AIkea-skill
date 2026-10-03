# Shared CNC preferences

## Scope
Remove image-transport knowledge from metadata-only preference validation.

## Work packages
- [x] Extract the common preference contract into QuotePreferences.
- [x] Compose it from local inline-preview and hosted metadata validation.
- [x] Include the shared owner in the Lambda artifact.
- [x] Verify transport parity (24 focused tests passed).
- [x] Complete fresh independent review: round 3 passes all lanes.
- [x] Publish and merge.

## Current state
The fake PNG has been removed; each transport keeps its own image boundary. The 24-test focused suite passes; fresh independent round 3 passes all lanes.

## Audit log
- 2026-10-01: Under Patrick's authorized review/fix loop, accepted the responsibility finding at IntakeContract.validate. A shared preference owner removes fabricated preview input without changing accepted preference values or PNG rules.

Release evidence and remaining limits: [desktop4-release.md](desktop4-release.md).
