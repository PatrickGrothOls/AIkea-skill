# Desktop installation

The current installer is delivered in the versioned ZIP linked from
[Getting started](../START_HERE.md). Its complete source is included in that
archive. Installer source is also maintained in `portable/`; the release ZIP
places it alongside the complete skill bundle required for installation.

## Installation

The assistant verifies the published ZIP checksum, extracts it and reads
`SKILL.md` followed by `BOOTSTRAP.md`. It runs:

```sh
bash /absolute/path/aikea/setup.sh /absolute/path/workspace/aikea-runtime
```

The installer verifies the pinned uv download, provisions isolated Python,
installs CAD dependencies and a separate headless Blender engine, then runs
real CAD and presentation probes. Dependencies stay in the selected runtime
folder; it does not change system Python or shell profiles.

The setup report preserves stage logs, interpreter paths and generated artifacts.
A repeated run reuses downloaded dependencies while retaining each attempt's
logs. Keep one heavy bake and one 3D viewer active at a time.

## Completion

- The package integrity check passes.
- CAD creates a solid, round-trips STEP and exports GLB.
- Blender completes the bake and geometry checks.
- The user can open the interactive model, rotate it and zoom.
- The assistant records file locations and asks the first furniture-intake question.

Runtime checks alone produce `RUNTIME_VERIFIED`. The assistant may report `READY`
only after interactive delivery and intake also succeed. A hosted localhost
server is not a user-accessible viewer. Preserve successful runtime setup if
viewer delivery is blocked, and identify the remaining action precisely.

## Current verification

The installer passed an isolated macOS ARM64 installation and repeat run. Its
runtime stages also completed in a Claude hosted Linux workspace. Public-prompt
viewer delivery, reopening, persistent skill registration and ChatGPT Work
acceptance have not been established for this release.
