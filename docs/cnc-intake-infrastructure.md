# CNC intake infrastructure

## Scope and current state

Reusable infrastructure for invitation-only Cognito, JWT-scoped API Gateway,
private quarantine storage and bounded Lambda processing. Public files do not
record deployment identities, account status, failed stacks or private incidents.
Templates and offline tests are available; operators must verify their deployment
and sign-in/upload flow privately before claiming a live customer service.

## Prepare and deploy

Provide [explicit deployment configuration](cnc-deployment-configuration.md).
Prepare artifacts without AWS calls:

```sh
direnv exec . python infra/cnc-intake/deploy_intake.py --config infra/deployment.local.json --output infra/cnc-intake/deployment.local
```

`deployment_permissions.py` accepts the same `--config` and `--output` directory
and generates combined/core/identity IAM policies. Checked-in JSON policies are
safe examples only; regenerate policies for the private target and review them.
They fit the managed-policy size limit and are intended exclusively for a trusted
operator, never a customer's model. API tagging remains restricted by Service tag.

Only an explicitly authorized `--apply` invocation deploys. It rejects example
configuration, checks STS account identity before uploads or resource changes,
uploads only its code artifact under `aikea/deploy/cnc-intake/`, and writes client
configuration to the private output directory. There is no default production target.
Failed-stack recovery requires fresh operator inspection of retained resources;
never delete shared storage or unrelated notification resources as a recovery shortcut.

## Access and storage boundaries

Self-registration is disabled. Administrators invite customers separately; deployment
sends no invitations. The runtime checks enabled accounts and verified email on each
request. Access tokens last five minutes; already-issued S3 grants expire normally
after account disablement. The client distributes no AWS secret or refresh token.

Both routes require `aikea/submit`. No anonymous upload, public function URL, arbitrary
key, object-read or ready-marker upload grant is introduced. Exact checksum/size/key
constraints and server-side hashing pin accepted bytes; conditional writes prevent
replacement. Intake never executes source. Accepted writes are restricted to the
four named package objects, and bucket listing remains limited by prefix.

The new quarantine bucket blocks public access, requires encryption and TLS, and
has no CORS. Temporary uploads expire after one day; reservations/quotas after
seven days. Lifecycle expiration is asynchronous. Accepted storage retention and
existing shared-bucket privacy settings are unchanged.

Client outputs include AccountId, Region, GatewayUrl, LoginUrl, ClientId and
QuarantineBucket. The client validates the configured account/region and pins the
exact account-derived Cognito and quarantine destinations; it rejects redirected
upload destinations. Obtain configuration from the trusted operator.

## Validation limits

Offline tests cover scoped JWT routes, private storage, least-privilege IAM,
reproducible packaging, policy limits, missing/invalid configuration and account
mismatch. Live deployment, login, S3 enforcement and inbox delivery are separate
operator checks. No AWS deployment is part of this privacy cleanup.
