# Authenticated CNC upload gateway

## Scope

Stacked on `codex/cnc-upload-validation`. Build the cloud intake boundary for
external AIkea clients. No customer receives Patrick's AWS credentials. No
database is introduced; bounded request reservations are immutable S3 objects.

## Work packages

- [x] Implement authenticated request reservations and daily upload quotas.
- [x] Issue short-lived, exact-key, exact-size, checksum-bound S3 POST policies.
- [x] Validate quarantined bytes and publish immutable accepted requests.
- [x] Keep deployment resources in the next infrastructure branch.
- [x] Define the runtime boundary for the following infrastructure slice.
- [x] Test cross-user access, replay, partial writes and authorization failures.
- [x] Commit and publish branch documentation as authorized.

## Current state

Runtime implemented; 32 focused tests pass. No external endpoint deployed. Sign-in choice and
documentation publishing clarification were asked; implementation defaults to
separate AWS Cognito sign-in. Initial access is invitation-only. Customer browser
sign-in and source upload integration follows as a separate stacked branch.

## Audit log

1. Patrick approved the proposed gateway and requested uploading branch docs.
2. Separate quarantine storage and a server-only ready marker implement the
   approved isolation and validation boundary. Pending uploads expire; accepted
   requests use the existing notification pipeline and retention behavior.
3. S3 conditional writes provide reservation and acceptance idempotency without
   introducing a database schema. Limits: five requests per invited user per UTC
   day, 16 MB ZIP, 64 MB expanded source and 4 MB preview; five-minute grants.

## Security and operational limits

Uploads are untrusted code, never executed by intake. Extension, archive and hash
checks are not a malware verdict or machining approval. Downstream regeneration
needs a disposable isolated environment. Presigned grants are bearer capabilities
and replayable until expiry; checksum binding restricts replay to identical bytes.
Daily quotas constrain distinct requests; repeated S3 traffic within a grant's
lifetime remains a cost risk. API throttling is best effort, not a spending cap.
Invite-only registration bounds who can obtain grants during the pilot.

## Verification

Actual SDK-generated POST policies bind exact key, size and checksum. Offline
tests reject absent identity, cross-user completion, disabled accounts, expired
reservations, changed metadata and tampered uploads. Partial publication retries
produce one ready marker; daily quotas allow idempotent retries.
