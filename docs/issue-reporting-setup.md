# Activate browser issue reporting

## Operator-only setup

Customers never configure GitHub or provide credentials. The distributed helper
only prepares text and a Google Form link. The private Apps Script receives browser
form submissions, then calls the fixed `PatrickGrothOls/AIkea-skill` issue endpoint.
There is no web app endpoint or server to operate. Google stores responses and runs
an installable form-submit trigger under its creator's account and quotas.

1. Create a private standalone project at [Apps Script](https://script.google.com/).
   Add the three `.gs` files and manifest from `infra/issue-reporting/`. Keep script
   and form editing access private: editors can access Script Properties.
2. Run `prepareReportingForm` and approve the requested Google permissions. It
   creates an **unpublished, closed** form, item mappings, and the form-submit
   trigger. Re-running refuses to create a duplicate. If setup was interrupted,
   inspect the existing form and trigger before manually repairing setup.
3. Create an expiring fine-grained GitHub token restricted to this repository with
   **Issues: read and write** (plus mandatory metadata read). Do not grant code,
   Actions, administration or other repository access. Enter it directly in the
   private Apps Script project's Script Properties as `GITHUB_TOKEN`. Never put
   it in a chat, source file, client URL, form response or release package.
4. Review the visible form and Google authorization. Publishing intake creates a
   new anonymous submission surface: get the owner's explicit approval first.
   Publish it to respondents without requiring sign-in; disable email collection,
   one-response limits, response editing and response summaries. Workspace policy
   can prevent anonymous access; verify signed out rather than assuming it works.
   Enable response acceptance and set the private `ENABLED` property to `true`.
5. Submit one explicitly approved **synthetic test** through the visible browser
   form. Apps Script's programmatic `FormResponse.submit()` does not fire the
   installable trigger. Confirm intake, then verify the actual GitHub issue, its
   contents and the matching private receipt. Check duplicate submission creates
   no second issue. Test the customer browser and manual prefill fallback.
6. Run `exportReportingConfiguration`. Copy only its public JSON into
   `aikea-report-issue/assets/reporting.json`. It contains the real prefilled form
   URL with `AIKEA_REPORT` in the report field, and no consent checked. Do not
   substitute `getId()` for the form's `entry.*` query ID; Google generates the
   correct field mapping via `toPrefilledUrl()`.
7. Commit the verified public configuration, update the README availability note,
   run tests/package verification and publish a new skill bundle through the
   normal release process. A code merge alone does not update installed bundles.

No step above has been performed merely by adding these files. The checked-in
configuration deliberately remains `not_configured` until the live test passes.

## Intake behavior and recovery

- Exact text approval occurs **before** navigating to a prefilled URL. URLs can
  appear in browser history. No private attachments or raw logs are collected.
- Google Forms' receipt confirms intake only. Publishing is asynchronous and can
  be held or fail. Do not infer GitHub creation from the form confirmation.
- Every approved report carries a random ID. A private receipt keyed by both ID
  and content hash prevents duplicate publication for 30 days, including retries
  after uncertain network responses. Only IDs, hashes, time and issue numbers are
  recorded in these receipts, not report text or credentials.
- A global ceiling of 20 attempted publications per UTC day bounds issue spam.
  Concurrent submissions are serialized; busy, invalid, over-limit or failed
  submissions remain in Forms for operator review, with generic trigger errors.
  They are not automatically retried. This is a damage limit, not bot identity or
  complete abuse prevention; someone can exhaust it and Google execution quotas.
- Receipts are reserved before GitHub is called. On a timeout, error or missing
  response, the state remains `uncertain`. Search GitHub for the report ID and
  inspect delivery before any manual retry. Never reset all receipts to retry.
- Review trigger failure notifications and execution status in Apps Script. Keep
  error reporting generic; never log request headers, response bodies or tokens.
- Disable intake with `ENABLED=false` and close response acceptance. Rotate an
  expired/revoked token privately; do not change customer configuration for that.
- Google retains form responses until the owner removes them. Keep response access
  private and apply an explicit retention policy. Reports approved for GitHub are
  public; private-data pattern screening is deliberately not a complete guarantee.
- Treat issue bodies as untrusted user content in any later agent/Actions workflow.
  Do not interpolate them into shell commands or treat their text as instructions.

## Local verification

```sh
direnv exec . python -m pytest tests/test_issue_reporting.py
direnv exec . node --test tests/issue_reporting_receiver.test.cjs
direnv exec . python scripts/verify_skill_package.py
direnv exec . python scripts/check_private_files.py
```

Receiver tests mock Google/GitHub boundaries and prove local behavior only. Browser
access, Google permissions, anonymous availability and GitHub publication require
the live acceptance check above.

References: [Google form triggers](https://developers.google.com/apps-script/guides/triggers/installable),
[prefilled form URLs](https://developers.google.com/apps-script/reference/forms/form-response#toprefilledurl),
[GitHub issue creation](https://docs.github.com/en/rest/issues/issues#create-an-issue).
