# Independent stability review, round 2

Verdict: **FAIL** — one confirmed source completeness defect (S1, P2). The observed upload lifecycle, retry behavior, validation, and existing viewer compatibility tests otherwise pass. This verdict does not claim live AWS validation.

## Contract and checkout

Read `/tmp/aikea-review-contract-r2.md` before code exploration. Reviewed integrated changes from `5db04d7` through `dec32663814818a134cad6af9357d34c7d698fc5` in `<user-home>/.codex/worktrees/cnc-release-review/AIkea-skill`.

Before and after review, `git rev-parse HEAD` returned exactly `dec32663814818a134cad6af9357d34c7d698fc5`; `git status --short --branch` showed only `## docs/cnc-public-availability`, with no changes. No repository edits, dependency installs, shared venv changes, cloud operations, uploads, emails, invitations, or customer-source execution were performed. Prior reports and narrative audit logs were not read.

## S1 — P2: newly added shared source is silently absent from an accepted source snapshot

- Requirements: **R2** (editable repository code for local regeneration), **R4** (complete frozen source submission).
- Introduced by this integrated unit; `quote_source_repository.py` is new relative to the base.
- Primary location: `aikea-review-unit/scripts/quote_source_repository.py:25-29`.
- Downstream path: `QuoteDeliverySession.from_environment` -> `QuoteSourceRepository.build` -> either submission transport -> accepted package/ready marker. Hosted validation at `infra/cnc-intake/package_validation.py:53-65` validates only the files the incomplete manifest declares, so it cannot detect this omission.
- Reachable prerequisite: a chosen Git repository has a committed HEAD and selected design directory. A working design imports a new, untracked shared Python helper outside that selected directory and outside `docs/`. This satisfies the documented repository setup at `aikea-review-unit/references/cnc-quotes.md:22-28`; no staging or clean-working-tree requirement is specified. Working-copy/uncommitted design source is explicitly supported.
- Defect: candidate names include only tracked files, selected-project files, and Markdown docs. New allowed shared source elsewhere in the chosen repository is never considered. A modified tracked builder is included with its new import, while the imported file is silently omitted. This does not require an ignored file, forbidden extension, symlink, generated export, or external dependency.
- Impact: Patrick receives a submitted/ready archive whose provided design cannot be regenerated because part of its local editable source is missing. Both transports share the faulty snapshot builder. An unchanged retry reproduces the incomplete package.

### Offline evidence

Using the existing synthetic Git fixture, changed `assemblies/wardrobe/builder.py` to `from shared_dimensions import WIDTH` and created untracked root-level `shared_dimensions.py` containing `WIDTH = 700`. No source was executed. Actual snapshot output:

```text
Packaged builder: from shared_dimensions import WIDTH
Required shared module exists locally: True
Required shared module included: False
```

Then submitted that exact package through `HostedQuoteSession` and the existing synthetic `GatewayTransport`, which runs the real gateway, reservation, package validation, and acceptance classes with fake storage/network. Output:

```text
Synthetic gateway receipt: {"notification": "pending", "request_id": "53d0e2fc-8bc0-5f56-aa78-799417628348", "services_sent": ["machining"], "status": "submitted"}
Accepted builder: from shared_dimensions import WIDTH
Accepted package has required shared source: False
```

Reproducer, run from the reviewed tree with `direnv exec . python`:

```python
from pathlib import Path
from tempfile import TemporaryDirectory
import sys, io
from zipfile import ZipFile
sys.path[:0] = ['tests', 'aikea-review-unit/scripts', 'infra/cnc-intake']
from test_quote_source_repository import TestQuoteSourceRepository
from test_hosted_quote_session import TestHostedQuoteSession
from hosted_quote_session import HostedQuoteSession

with TemporaryDirectory(prefix='aikea-stability-source-') as directory:
    root = Path(directory)
    source = TestQuoteSourceRepository()
    repository = source.repository(root)
    source.write(root, 'assemblies/wardrobe/builder.py',
                 'from shared_dimensions import WIDTH\n')
    source.write(root, 'shared_dimensions.py', 'WIDTH = 700\n')
    package = repository.build()
    fixture = TestHostedQuoteSession()
    fixture.setup_method()
    session = HostedQuoteSession(package, 'b' * 64, fixture.config,
                                 fixture.transport, fixture.login)
    receipt = session.submit(fixture.body, session.token)
    assert receipt['status'] == 'submitted'
    accepted = fixture.transport.s3.objects[
        'accepted', 'aikea/cnc-requests/' + receipt['request_id'] +
        '/source-repository.zip']
    with ZipFile(io.BytesIO(accepted)) as archive:
        assert archive.read('repository/assemblies/wardrobe/builder.py') == (
            b'from shared_dimensions import WIDTH\n')
        assert 'repository/shared_dimensions.py' not in archive.namelist()
```

Smallest justified correction: avoid silently claiming a complete snapshot while omitting allowed new shared source. Include such selected-repository source through the same exclusions/symlink/size/privacy checks, or fail preflight with a specific instruction to stage the omitted shared source before submission. Do not execute imports to detect dependencies. Add one regression using a design importing a new root/shared helper and verify that submission either contains it or is explicitly blocked before upload; retain other-design and secret/export exclusions.

## Coverage and results

- **PASS** — focused Python flow suite: `test_hosted_quote_session.py`, `test_quote_delivery.py`, `test_quote_source_repository.py`, `test_quote_preferences.py`, `test_cnc_intake.py`, `test_cnc_notification.py`, `test_cnc_package_validation.py`, `test_cnc_intake_infrastructure.py`, `test_cnc_browser_login.py`, `test_quote_object_store.py`. Initial run: 66 passed and one localhost bind blocked by sandbox. The affected browser test and `test_quote_http.py` were rerun with permitted localhost access: **6 passed**, including all browser tests and four HTTP tests. The sandbox bind failure is not a code defect.
- **PASS** — portable package checks: `tests/test_portable_desktop_package.py`, **6 passed**. Inspected `PortablePackage.members/build` and deployment runtime ZIP construction for inclusion of the new runtime modules and availability instructions. License and bundled third-party notices remain in the portable distribution path.
- **PASS** — existing caller compatibility: `tests/test_unit_review_decision_api.py` and `tests/test_unit_review_artifact_binding.py`, **6 passed** with synthetic local HTTP access. CadQuery emitted six existing `FutureWarning` messages for its `save` API.
- **PASS** — bounded preview checks: `direnv exec . node --test viewer/src/ReviewSnapshot.test.js`, **5 passed**.
- **FAIL** — additional source-completeness fixture above; ordinary tests do not cover a new shared helper outside the chosen project/docs.

Reviewed the full quote form and snapshot path; local host/origin/token route composition; frozen submission identity and locking; trusted-host conditional writes and checksum retry; native PKCE client and transport boundaries; authenticated gateway reservation/acceptance/storage lifecycle; quota and expiry behavior; service-owned ready publication; notification manifest checks and retry marker; infrastructure routing/permissions/deployment packaging; and new public availability/portable instructions. No additional concrete stability finding was confirmed.

## Limits, deferred work, and optional hardening

- **NOT_RUN** — live Cognito, S3 POST, Lambda/API Gateway, SNS/email delivery, IAM/deployment, fresh external installer download, real desktop browser interaction, and full CAD regression. They are outside this offline assignment. Full regression CI is coordinator owned.
- **INCONCLUSIVE** — live end-to-end hosted operation. The contract explicitly defers IAM repair/deployment and live authentication/upload proof; this alone is not a release defect. Public instructions accurately retain this limitation and describe the same-computer localhost callback constraint.
- No claim of exhaustive untouched CAD correctness, browser visual fidelity, or production notification delivery.
- Notification delivery is at least once: a crash after SNS accepts a publish but before `notified.json` can duplicate an email, as the source explicitly documents. No exactly-once requirement exists in the contract; no blocking finding is raised for that behavior.
- No speculative hardening requests are included.
