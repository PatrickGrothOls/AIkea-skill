# Portable AIkea start

## Scope

Let a fresh everyday chat load AIkea from one pasted paragraph and begin the
measurement conversation. Provide a single downloadable skill bundle for file
and execution capable chats, including Claude's custom-skill upload format.
Keep all furniture instructions and builders in the existing nine skills.

## Workpackages and tasks

### WP1 - Entry and capability handling

- [x] Inspect the current entry skill and public release boundaries.
- [x] Check current ordinary-chat file and execution capabilities.
- [x] Add one public starter paragraph and a readable bootstrap entry.
- [x] Make absent browsing, file access, and runtime capabilities explicit.
- [x] Provide a self-contained Markdown intake guide for upload fallback.

### WP2 - Download and setup

- [x] Package all nine skills, the viewer, runtime requirements, and licenses.
- [x] Provide a single-root skill ZIP with a discoverable entrypoint.
- [x] Keep setup inside the bundle's environment and preserve existing projects.
- [x] Generate deterministic downloads and checksums from tracked source files.

### WP3 - Verification and delivery

- [x] Verify the extracted bundle and actual entry commands.
- [ ] Test a fresh chat using only the starter and published instructions.
- [x] Check that a chat without execution never claims CAD installation or validation.
- [ ] Update the public download entry and release assets after verification.
- [ ] Record the tested platforms and remaining limits honestly.

## Current state

Work starts from clean public main in an isolated worktree. The existing public
alpha and private development history remain separate. Ordinary ChatGPT supports
Markdown uploads, but its data-analysis Python cannot fetch external packages.
Claude supports custom skill ZIP uploads when its skill and execution features
are enabled. A text paragraph cannot grant tools that the chat does not have.

The portable entry, generated guide, and 4 MB single-root ZIP are implemented.
Two integration tests prove reproducible archives/checksums, exclusion of
untracked client data, nine included skills, viewer license notices, and real
entry commands after extraction. A clean package-local Python 3.10 installation
passes the import/version/solid check on Apple Silicon. Python 3.11 local setup
and Linux 3.11/3.12 CI are being checked before release.

An independent fresh assistant, given only the guide and no execution tools,
asked for units, then the shape, then fitted edges. It rejected a request to
pretend installation and fabrication checks had happened. This is a behavioral
test, not a ChatGPT or Claude web product test. The available ChatGPT browser
session is signed out; native chat upload and Claude skill installation have
not been verified in their account UIs.

Full calculated CAD and saved approvals still require the actual runtime and
project files. A loaded guide, an unpacked skill, and a working CAD environment
are reported separately. Publication and live download checks remain pending.

## Rebuild the downloads

Run `direnv exec . python scripts/build_portable_package.py` from the repository
root. Commit the regenerated `AIKEA_CHAT.md` alongside any changed canonical
intake sources. The ignored `dist/` folder contains `aikea-skill.zip`,
`AIKEA_CHAT.md`, and `SHA256SUMS`; upload these together for the release named in
`START_HERE.md` and the builder's stage links. The builder includes only tracked
files under the nine canonical skill folders and explicit portable entry files.
CI rejects a stale guide and exercises the extracted package.

## Audit log

1. 2026-09-06 - The user requested easy download and a single paragraph that lets
   a no-context chat install AIkea and start, particularly without coding agents.
2. 2026-09-06 - Capability detection avoids claiming universal software
   installation from text alone. Missing execution does not prevent beginning
   measurement intake, but it still prevents claiming checked CAD results.
3. 2026-09-06 - Existing source instructions remain authoritative. The upload
   guide and downloadable bundle will be generated from them to avoid a second
   independently maintained furniture workflow.
4. 2026-09-06 - The portable wrapper keeps all nine skill folders adjacent under
   `skills/`, preserving their existing relative imports and routes. Client
   projects and virtual environments are excluded from release generation.
5. 2026-09-06 - Runtime setup uses the package's own environment and verifies
   pinned dependencies plus a real solid. Python 3.11/3.12 are admitted because
   the pinned upstream packages provide compatible wheels; CI checks their
   setup and entry commands while Python 3.10 remains the complete-suite baseline.
6. 2026-09-06 - Conversation-only forward testing preserved the one-topic intake
   flow and the distinction between a draft and checked fabrication evidence.

## Platform evidence

- [ChatGPT data analysis](https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt/)
- [Claude custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
- [Using skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude)
