# CNC request notifications

## Scope and current state

The notification infrastructure implements a private source-only CNC quote pipeline:
S3 ready marker → SQS → Lambda → SNS email. This is reusable deployment guidance,
not a record of a particular account, recipient, deployment or inbox delivery.
Keep deployment status, request IDs, receipts and incident notes in private evidence.

## Configure and prepare

Follow [deployment configuration](cnc-deployment-configuration.md). A configuration
file and notification recipient are required; there is no production default.
Prepare a CloudFormation template without AWS calls:

```sh
direnv exec . python infra/cnc-requests/deploy.py --config infra/deployment.local.json --email cnc-operator@example.com --output infra/cnc-requests/deployment.local
```

The address above is an example; choose the real recipient privately. Render the
matching IAM policy with `infra/cnc-requests/deployment_permissions.py`, using the
same `--config` and `--email`, and an `--output` JSON file inside `deployment.local/`.
The checked-in policy template contains placeholders and must not be attached as-is.
Only a trusted operator should receive deployment permissions.

Deployment requires an explicitly authorized invocation with `--apply`. It checks
STS against the configured account before any writes and rejects example targets.
The helper backs up existing bucket notifications, merges only its named queue
hook, and rechecks concurrent changes. S3 provides no conditional notification
configuration write; coordinate other bucket changes during deployment.
No CORS or public upload endpoint is installed. Confirm the SNS subscription
privately and verify synthetic delivery independently of template preparation.

## Preserved boundaries

Notifications filter prefix `aikea/cnc-requests/` and suffix `/ready.json`.
The worker verifies source, preview and preferences before publishing, and writes
`notified.json` only after SNS accepts the message. No STEP exports are stored.

IAM remains scoped to named CNC resources and request prefixes. Email subscription
is restricted to the configured recipient and email protocol. Role passing remains
bound to Lambda; event-source creation remains bound to the named function. Broad
read-only metadata permissions remain only where AWS does not support resource scope.
Deployment roles can manage their named runtime role and must never be distributed
to customer agents. Existing bucket hooks, privacy and retention settings are preserved.

Delivery is at least once. A crash between publish and receipt can duplicate email;
deduplicate by request ID. Failed messages enter a dead-letter queue after five
receives and trigger an alarm. Queue and log retention are 14 days; no S3 deletion
policy is introduced. SNS acceptance does not prove inbox arrival.

## Validation

Offline tests cover incomplete uploads, duplicates, publishing failures, hook merges,
configured resource scope and wrong-account refusal. Live verification belongs to
the operator's private deployment record; this cleanup does not deploy to AWS.
