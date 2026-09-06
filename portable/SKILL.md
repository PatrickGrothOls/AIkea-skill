---
name: aikea
description: Guide a fresh fitted-furniture or wardrobe project from measurements to the first cabinet review using the bundled AIkea skills. Use in ordinary chats or coding assistants, adapting to available file and code tools.
---

# AIkea portable entry

Read `AIKEA_CHAT.md` completely before the first furniture response. It contains
the shared conversation contract, capability boundaries, and initial intake.
Begin with its first unfinished question; setup must not delay collecting units.

The nine canonical skills live next to each other inside `skills/`. Resolve
`$aikea-<stage>` by reading `skills/aikea-<stage>/SKILL.md`, then its referenced
files. Do not assume the host supports dollar commands or persistent skills.
Within a canonical skill, relative paths remain relative to that skill folder.

## Runtime setup when code execution is available

Loading this package is not proof that CadQuery is available. From this folder,
run `python setup_aikea.py` to check the current Python, imports, and a real solid.
If it succeeds, use that interpreter for the bundled scripts and set
`AIKEA_CADQUERY_PYTHON` to its absolute path for review subprocesses.

If the check fails and the host permits package installation, use an available
Python 3.10, 3.11, or 3.12 to run `python setup_aikea.py --install` (substitute
the actual interpreter command). This creates only this package's
`.venv`, installs the pinned requirements there, and checks it. Use the printed
interpreter path for later commands. It never needs a global pip install, sudo,
direnv, Codex, or Claude Code. Do not bypass host restrictions, enable network
access, or alter account settings to make setup work. If the required runtime
cannot run here, continue guided intake and explain the limit when calculation
or CAD is needed.

Python 3.10 is the complete-suite baseline. Newer supported interpreters must
still pass the runtime check; a successful setup check does not validate a
furniture project. Native Windows cannot run the current review approval lock.

Store each client project in a separate folder outside this package. Before
calculating a complete, material-approved specification, the command is:

```sh
<verified-python> skills/aikea/scripts/calculate_overall_wardrobe.py <project>/aikea.yaml
```

Use the other canonical skills' commands for their stages, substituting the
actual skill and project directories. Never overwrite an existing project with
the template. Keep the first complete cabinet's visual approval gate and all
hardware, collision, and fabrication checks active.

## Scope and license

Personal and noncommercial use is covered by the bundled `LICENSE.md`.
Commercial use requires separate permission. The alpha supports design and
review; missing material propagation and manufacturing-pack evidence still
block fabrication readiness. Manufacturer hardware CAD is not included.
