# CNC deployment configuration

## Explicit private target

Copy `infra/deployment.example.json` to ignored `infra/deployment.local.json` and
replace all example values privately. Required string fields are `AccountId`,
`Region` and `AcceptedBucket`. No credentials belong in this file; use your normal
AWS profile. Bucket names are restricted to DNS-safe lowercase names without dots.
These ARN/endpoint builders support the commercial AWS partition only.

Every deployment and policy generator requires `--config`. Missing fields, malformed
identifiers and unknown fields fail before AWS calls. Safe example configuration
can generate review artifacts, but `--apply` refuses example accounts/buckets.
A syntactically valid configuration is not evidence of access: apply compares STS
caller identity with AccountId before any cloud writes. AWS validates resource
existence and service/region availability. Deployment helpers do not change IAM
permissions automatically.

Generate outputs only in an ignored `deployment.local/` directory. Review the
configured resources and conditions before attaching generated IAM policies. The
notification generator additionally requires `--email` and pins SNS subscription
to exactly that address and the email protocol. Never replace these constraints
with wildcards. Public examples use `123456789012`, `example-aikea-cnc-requests`
and `cnc-operator@example.com`; these are not a working deployment.

Hosted clients consume trusted stack outputs, including AccountId and Region.
Existing client configuration must be regenerated or updated with those fields.
The client still pins its exact Cognito login and quarantine bucket to the configured
deployment; do not accept configuration from an untrusted design/source package.

## Keeping private data out of Git

`local-evidence/`, environment files, local deployment output and credential files
are ignored. Run `direnv exec . python scripts/check_private_files.py` before
committing. CI runs the same check against tracked/indexed content, including files
force-added despite ignore rules. Only filenames, line numbers and rule names are
reported; matching values are never printed. This heuristic check is not a full
secret-history scan and cannot identify every private fact or obfuscated credential.

Back up `local-evidence/` in every other clone **before pulling the cleanup**.
Git may delete tracked copies when applying their removal. Current-clone files
are preserved with `git rm --cached`. Current-tree cleanup does not erase earlier
commits, forks, existing clones, PR diffs, release artifacts or external caches.
Any exposed credential requires separate revocation/rotation; history rewriting
is outside this change and is not performed.
