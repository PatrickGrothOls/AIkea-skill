# AIkea skill source

This repository contains the source-available AIkea skills, deterministic furniture
builders, tests, and editable interactive-viewer source. Generated client
projects and licensed manufacturer CAD remain local and outside source control.

Open the cloned repository as a Codex or Claude working folder. Its
`.agents/skills/` and `.claude/skills/` links expose the complete AIkea skill
set, beginning with `$aikea`.

## License and permitted use

AIkea is licensed under the [PolyForm Noncommercial License 1.0.0](LICENSE.md).
Personal furniture, private experiments, study, and hobby projects are permitted.

Commercial use is not granted. This includes using AIkea for paid furniture
design, manufacture, installation, or sale. Contact the repository owner for a
separate commercial license. The license text controls if this summary differs
from it.

Because commercial use is restricted, AIkea is source-available rather than
Open Source Initiative open-source software.

AIkea is an independent project. It is not affiliated with or endorsed by IKEA,
Lamello, Hettich, or other referenced manufacturers. Product names and
trademarks belong to their respective owners. Bundled Cabineo STEP files are
machining cutter inputs rather than complete manufacturer product CAD; their
provenance and hashes are documented in
`aikea-build-units/assets/cabineo/README.md`.

## Python setup

Use Python 3.10.16 and create the repository-local environment once:

```sh
python3.10 -m venv .venv
direnv allow .
direnv exec . python -m pip install -r requirements.txt
```

Run the complete Python suite with:

```sh
direnv exec . python -m pytest -q
```

The review commands discover the same interpreter through
`AIKEA_CADQUERY_PYTHON`, which `.envrc` sets to `.venv/bin/python`.

For a generated project, the final readiness command is:

```sh
direnv exec . python aikea-review-unit/scripts/check_fabrication_readiness.py \
  /path/to/project/aikea.yaml
```

It reports every missing physical, manufacturing-pack, validation, or visual
approval requirement and returns success only for `fabrication-ready`.

## Viewer source

The installed skill contains prebuilt static viewer files and does not require
Node.js. Contributors use the repository-only `viewer/` project, pinned to Node
24.4.1 and npm 11.4.2:

```sh
direnv exec . npm --prefix viewer ci
direnv exec . npm --prefix viewer test
direnv exec . npm --prefix viewer run build
```

The production build writes the compiled viewer directly into
`aikea-review-unit/assets/viewer/` for skill packaging.
