# AIkea — fitted furniture design skills (alpha)

This repository contains the source-available AIkea skills, deterministic furniture
builders, tests, and editable interactive-viewer source. Generated client
projects and licensed manufacturer CAD remain local and outside source control.

**[Start in any chat](START_HERE.md)** ·
**[Download the skill](https://github.com/PatrickGrothOls/AIkea-skill/releases/download/v0.1.0-alpha.2/aikea-skill.zip)** ·
**[Download the chat guide](https://github.com/PatrickGrothOls/AIkea-skill/releases/download/v0.1.0-alpha.2/AIKEA_CHAT.md)**

No Codex or Claude Code is needed to begin. Copy this paragraph into a fresh chat:

> Help me design fitted furniture with AIkea. Read and follow https://raw.githubusercontent.com/PatrickGrothOls/AIkea-skill/main/START_HERE.md and load its linked guide. If you can download files and run code, set up its skill package in your own workspace; otherwise begin the guided conversation with the tools you have. Use only measurements and choices I supply for this new project, and ask one topic at a time. Start by asking which units I use: 1. Centimetres, 2. Millimetres, or 3. Inches. Never claim files were saved, software installed, or a design checked unless you actually did it. If you cannot read the guide, ask me to attach AIKEA_CHAT.md from https://github.com/PatrickGrothOls/AIkea-skill/releases/tag/v0.1.0-alpha.2.

The [start page](START_HERE.md) also explains the one-file upload fallback and
installing the ZIP as a persistent Claude skill. A conversation-only chat can
guide measurements; checked dimensions and CAD require a working Python/CadQuery
environment. Loading instructions does not grant a chat new tools.

## What the alpha can do

AIkea guides measured-space intake and material choices, generates cabinet and
base parts, adds supported doors, drawers, and recessed lighting, and shows the
composed result in an interactive 3D viewer. Construction comes from reusable
CadQuery builders and saved project specifications. Begin with one complete
cabinet and visually approve it before repeating the design.

This is an experimental design and review workflow. Exact material choices are
not yet propagated into generated part specifications, so those parts cannot
pass the fabrication-readiness gate. A complete manufacturing pack and a fresh
end-to-end fabrication proof remain unfinished. The checker rejects missing
evidence; a successful preview does not establish that a project is ready to cut.

Supported hardware profiles require exact manufacturer CAD downloaded into the
active project's local hardware library. Some suppliers require an account and
a manual download. AIkea guides that step; vendor CAD is not bundled with the
public skills. Current KA 4532 spacer support also leaves the longer fixing
screws and cabinet pilot specification unresolved.

## Try a first project

For Codex or Claude Code, install the Python environment below and open the
cloned repository as a working folder. Its `.agents/skills/` and `.claude/skills/`
links expose all nine skills. Start a fresh conversation with:

```text
$aikea
Help me design a fitted wardrobe. Use a new sibling project folder at
../my-first-wardrobe. Ask me for the measurements and choices you need,
one topic at a time, and guide me to the first complete cabinet review.
```

The sibling folder keeps client files outside this source repository. Supply
measurements from your own room. The skill's example and test files are
not measurements for your project. Keep the generated project private; its
dimensions, local hardware downloads, and approval records belong to you.

The current release has been exercised on macOS with Apple Silicon. Native
Windows is not supported by the viewer approval lock, which uses POSIX `fcntl`.
The complete automated suite also passes on Ubuntu 24.04. Interactive visual
review on Linux has not received the same local verification as macOS.

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
trademarks belong to their respective owners. AIkea's authored Cabineo machining
volumes preserve its custom brass-insert receiver without importing STEP files.
Their dimensions and regression proof are documented in
[Cabineo machining](aikea-build-units/references/cabineo-machining.md).

## Python setup

Install Python and [direnv](https://direnv.net/) before running these commands.
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
It also generates `THIRD_PARTY_LICENSES.md` from the bundled dependencies.
`SUPPLEMENTAL_LICENSES.md` retains notices omitted from dependency archives;
`THIRD_PARTY_NOTICES.txt` records source links and texture attributions.

## Reports and contributions

Use the repository's Issues page for reproducible bugs and supported-feature
requests. Include the commit or release version, operating system, failing
command, and a small synthetic example. Remove private room measurements,
download credentials, personal paths, and licensed CAD before attaching files.
