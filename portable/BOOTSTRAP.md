# Set up AIkea and begin the furniture flow

This is a candidate for desktop Work/Cowork testing, not a claim of compatibility
with every chat product. Use actual available tools. Installation may execute
locally or in the app's hosted workspace; record where it really happens.

## Install

After checking the downloaded ZIP against the SHA-256 supplied on the
getting-started page, extract it into a new directory. Read this file, then run:

```sh
bash /absolute/path/aikea/setup.sh /absolute/path/chosen-workspace/aikea-runtime
```

The assistant runs the command. Do not ask the user to open a terminal or install
dependencies. macOS ARM64 and Linux x86_64 are preparation targets for this
candidate; actual desktop acceptance remains to be tested. Bash, HTTPS curl,
tar and a SHA-256 utility must be available. The script downloads pinned uv from
its official release, verifies its baked-in digest, and provisions managed Python.
It then installs pinned CAD dependencies and a separate headless Blender engine.
All dependency files stay under the chosen runtime directory. No shell profile,
system Python, security setting or global software installation is changed.

Read the printed log paths while setup runs. It verifies a real CAD solid and
STEP round trip, exports GLB, runs the real Blender bake and checks preserved
geometry. `attempts/<id>/setup-report.json` retains the exact stage evidence and
absolute interpreter/artifact paths. Repeating the same command reuses the
runtime/cache and runs fresh probes in a new attempt; it preserves prior logs.
Allow approximately 4 GiB free for preparation, plus room for customer projects.

## Finish the desktop delivery check

RUNTIME_VERIFIED means CAD/Blender probes passed, not that the customer can see
the result. Read `skills/aikea-review-unit/SKILL.md` and its presentation guidance.
Use the report's labelled inspection/presentation assets for the synthetic test.
Serve the bundled viewer when its local URL is reachable by the user's browser.
In a hosted environment, use a supported user-accessible artifact/download route.
An internal localhost URL is not a deliverable. If this package's viewer cannot
be delivered in the current app, preserve runtime success but report viewer
delivery as BLOCKED. Do not call a static image an interactive viewer.

Verify that the actual model and assets load and that rotation and zoom work;
retain a screenshot or explicit user confirmation if you cannot observe them.
Record where the package, runtime and project will live and how to reopen them.
Do not claim cross-session persistence or account skill registration without
testing it. Keep one heavy bake and one 3D tab active at a time.

Then load `skills/aikea/SKILL.md`, create a separate fresh project when needed and
ask the first missing intake question, one topic at a time. Report READY only
after package integrity, CAD, Blender, accessible interactive viewer and intake
have all succeeded. Installation is distinct from the later furniture build.

## Continue through recoverable problems

Do not stop after planning, downloading or hitting the first error. Inspect the
failed stage's log, resolve its cause using supported tools, then rerun setup.
For a corrupt uv download, remove only the named installer-owned `tools/uv.tar.gz`
and retry; never delete unrelated files or customer projects. Retry transient
network errors with bounded backoff; do not repeat an unchanged failure forever.

If approval is required, report WAITING_FOR_APPROVAL, explain what it permits,
present the ordinary consent flow and resume after it arrives. Do not collect
passwords in chat, bypass restrictions or promise unsupported background work.
Preserve progress when the task is interrupted. With genuinely unavailable tools,
report BLOCKED with the exact stage, observed error, supported fixes attempted
and smallest required user action. Never disguise a reduced workflow as READY.
