# CNC request delivery

## Scope

Send the prepared design's editable source package to an explicitly configured
private CNC request bucket. No database, payment or fabrication approval is introduced.
Public documentation describes behavior; deployment receipts and operational status
belong in private evidence.

## Delivery boundary

This slice uses credentials on the trusted local viewer host through AWS CLI.
Credentials never enter the browser or design bundle. This is the current local
prototype, not an anonymous customer upload service. Distribution to customers
requires an authenticated hosted intake service; do not ship operator credentials.
The host explicitly identifies the source repository and design subdirectory.
The package includes repository code/configuration and the selected design's
uncommitted source, with original relative paths and an exact content manifest.
STEP and other generated exports are excluded. It is an editable working-copy
snapshot, not Git history. A quote request does not approve files for cutting.

## Verification

Source tests cover dirty and new design code, tracked deletions, STEP/render and
environment-file exclusion, other designs, and symlink refusal. Delivery tests
cover partial upload failure, same-ID retries, concurrent double clicks, altered
retry rejection, and authorization. Real loopback HTTP tests reject foreign
origins, wrong Host and bad tokens; failures return 502, never a false receipt.
AWS CLI adapter tests verify conditional writes and identical-content recovery.
The existing viewer model tests pass with loopback access. The viewer builds and
all 68 existing JavaScript tests pass. The pre-existing large-bundle warning
remains. New or modified maintained code files are under 150 lines.

An upload receipt means S3 accepted the complete package. It does not confirm
email delivery, CNC feasibility, machining approval, or an offer. No real design
has been uploaded by this work.

## Host configuration

Before starting the existing verified viewer command, set
`AIKEA_CNC_SOURCE_REPO` to the source repository root and
`AIKEA_CNC_PROJECT_PATH` to the chosen design's relative subdirectory, e.g.
`assemblies/wardrobe`. Optional `AIKEA_CNC_AWS_PROFILE` defaults to `default`.
For trusted-host delivery, `AIKEA_CNC_DEPLOYMENT_CONFIG` must point to the private
[deployment configuration](cnc-deployment-configuration.md). Hosted customer delivery
instead uses `AIKEA_CNC_GATEWAY_CONFIG` from the trusted operator.
No repository path means delivery is disabled. Invalid or empty source fails at
startup. The source package is frozen when the viewer starts, alongside its GLB
snapshot; restart the viewer after editing source or regenerating the model.

The recipient unpacks `source-repository.zip`: `repository/` preserves the code
layout and dependency files, and `source-manifest.json` records the base commit,
selected design path and file hashes. This contains current working files, not
Git history. Regeneration is performed locally using the included code; no STEP,
STP, GLB, STL or DXF exports are sent. External hardware assets remain external.
