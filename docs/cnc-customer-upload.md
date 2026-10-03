# Customer CNC submission

## Scope

Stacked on `codex/cnc-intake-infrastructure`. Connect the existing viewer button
to human browser sign-in and the authenticated intake API. Source packages include
branch documentation; no customer needs AWS credentials or an AWS CLI install.

## Work packages

- [x] Share local session authorization and retry behavior across transports.
- [x] Implement browser authorization-code login with PKCE and state checking.
- [x] Upload checksum-bound packages and finalize through the gateway.
- [x] Explain sign-in at the existing send button.
- [x] Run client-to-gateway, real loopback and existing regression tests.
- [x] Build the viewer and review the complete stack.
- [x] Publish branches and documentation.
- [ ] Verify the hosted flow after deployment permissions are available.

## Current state

The customer client and authenticated intake implementation are available.
Deployment state, recipient details and recovery logs belong in private operator
records. Offline tests do not establish that a particular deployment is live.
All authentication material stays in memory. Only a five-minute access token is
used; no refresh token is retained. HTTP redirects cannot forward bearer tokens
or signed upload fields to another host. The callback binds only 127.0.0.1.

## Configuration after deployment

Distribute the deployment's `outputs.json` through the operator's chosen customer
channel. It contains deployment identifiers and endpoints, not credentials; do not
check a real deployment's outputs into this repository. See
[deployment configuration](cnc-deployment-configuration.md) for required fields. Configure the existing
viewer launch environment with:

```sh
export AIKEA_CNC_GATEWAY_CONFIG=/absolute/path/to/outputs.json
export AIKEA_CNC_SOURCE_REPO=/absolute/path/to/design-repository
export AIKEA_CNC_PROJECT_PATH=assemblies/design-name
```

Use the normal verified viewer launch command. The user clicks “Sign in and send
CNC request,” completes the invited-account sign-in in their browser, and returns
to the viewer for the receipt. The skill/model must never request their password,
copy tokens or give itself an AWS key. The source snapshot is frozen with the
viewer and must be reviewed before sending; repository docs are included.

This native flow requires the skill runtime and browser on the same user's
computer, with localhost:8766 available. A model running in a remote cloud
container cannot complete this callback on the user's behalf; a hosted browser
handoff is a separate future feature. A cancelled or expired sign-in can be
retried. Once both files upload, a retry only repeats server-side completion.

## Audit log

1. Patrick requested a customer/model upload path and branch documentation.
   The common session contract preserves existing trusted-host behavior while
   selecting hosted delivery when public gateway configuration is present.
2. Cognito sign-in is performed by the person in their browser. PKCE protects
   intercepted codes and state rejects unrelated callback requests. Passwords and
   AWS credentials never enter the viewer form or the model's conversation.
3. New branch Markdown under docs is included even before its first Git commit.
   All accepted source remains untrusted; it must not be executed on an operator's
   machine with credentials or network access.
4. Notification copy now carries the untrusted-source boundary. Rollout includes
   updating the existing notification worker before inviting external customers.
## Verification

Real localhost tests verify PKCE and rejection of forged OAuth state. Synthetic
client-to-gateway tests exercise actual multipart generation, checksum binding,
source validation, publication, expired tokens and retry after connection loss.
Existing trusted-host submission and HTTP authorization tests still pass. The
existing viewer bundle-size warning remains. New maintained source files are
under 150 lines; generated minified assets are build output, not authored modules.

Live identity provisioning, real S3 POST enforcement and inbox delivery
from this new endpoint are not implied by offline tests or the earlier trusted-
host synthetic delivery.

## Deployment

Generate scoped operator policies using the explicit target configuration described
in [intake infrastructure](cnc-intake-infrastructure.md). Checked-in policies are
examples, not policies ready for attachment to an operator identity. Apply only
after reviewing the generated policy and template for that deployment.
