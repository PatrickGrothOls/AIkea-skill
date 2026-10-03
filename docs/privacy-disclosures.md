# Privacy disclosure cleanup

## Scope

Remove private evidence from the current tracked tree, sanitize public operations
notes, require explicit CNC deployment configuration and add a lightweight privacy
check. Branch `codex/privacy-disclosures` starts from `origin/main` at `cc082ee`.
Patrick authorized a new branch and PR; no merge, AWS deployment or history rewrite.

## Work packages

- [x] Audit tracked evidence and deployment identifiers without reporting credentials.
- [x] Untrack evidence while preserving and checking local files.
- [x] Sanitize public docs and replace production configuration across code/policies/tests.
- [x] Add ignore rules and an automated index-based privacy check.
- [x] Test invalid configuration, account guards, IAM restrictions and privacy checks.
- [x] Review final diff and scan the staged tree without exposing matched values.
- [x] Commit with GitHub noreply identity, push and open PR.

## Current state

Implementation and final indexed review are complete.
[PR #26](https://github.com/PatrickGrothOls/AIkea-skill/pull/26) is open and unmerged.
Local verification is complete; GitHub CI status is reported separately on the PR.
The 40 formerly tracked evidence files remain byte-for-byte unchanged in both
local copies, verified against their pre-cleanup SHA-256 snapshots. No evidence
files remain in this branch's index. The private room run log is retained locally
under ignored `local-evidence/privacy-cleanup/`; its public page now keeps only
reusable technical lessons.

Validation: 130 focused tests and 4 subtests pass (CNC intake, notifications,
configuration, hosted/trusted upload, loopback authorization, source packaging,
portable package and privacy scanner). All 11 packaged skills and links verify.
Both deployers and both IAM generators prepare safe examples offline. A normalized
comparison against the base commit confirms all four IAM policy documents retain
the same actions, resource restrictions and conditions, with only target values
and the recipient statement label changed. Missing/invalid config, example apply
and account mismatch refuse deployment. No AWS command or deployment was run.

Compatibility: existing operators must supply private target configuration;
hosted client outputs now require AccountId and Region. Example policies are not
ready to attach to a live identity. All touched maintained Python files are under
150 lines. The scanner is heuristic and scans the index, not historical commits.
Back up `local-evidence/` in every other clone **before pulling this cleanup**:
Git can delete previously tracked copies when applying their removal.
This work removes disclosures from the current files only. Prior commits, existing
clones/forks, PR diffs and external caches are not erased by these commits.

## Audit log

1. Patrick requested this bounded privacy cleanup, explicit deployment configuration,
   preserved IAM/account restrictions, tests and a PR with no deployment or rewrite.
2. The audit found production identifiers in the hosted upload client as well as
   deployment code. Both are in scope so no hidden destination remains in the source.
   Trusted configuration must retain exact login and S3 destination restrictions.

3. As explicitly requested, deployment targets and the recipient remain private
   operator inputs; example configs support offline preparation but cannot apply.
   Existing exact IAM and hosted-upload destination restrictions are retained.
4. The requested public-document cleanup includes private host/temp paths and the
   room-specific operational ledger. Its original content is preserved locally;
   reusable construction and review lessons remain available publicly.
5. Regression verification initially hit sandbox restrictions on local sockets.
   Rerunning the same suite with loopback access passed; no AWS access was involved.

6. Final indexed privacy scan reports zero findings. A separate full indexed-byte
   search confirms the known production account, bucket, deployment identity and
   personal recipient are absent. Final diff/whitespace review passed. Evidence
   removal changes only Git tracking; preserved local copies were hash-checked.

7. Published the cleanup branch and opened PR #26. Author and committer use the
   requested GitHub noreply identity. No merge, history rewrite or AWS deployment.

## Remaining disclosure boundaries

Public authorship, repository URLs, third-party license attribution and other
existing furniture examples/technical design notes remain. This is not a complete
redaction of every named design case study or a historical secret audit. The known
personal recipient and production deployment identifiers are removed from current
source/docs/policies/tests. Older commits, already published releases, PR diffs,
existing clones/forks and caches can still contain removed disclosures. They have
not been rewritten or republished by this change.
