# Getting started with AIkea Skill

Copy this prompt into a new desktop Work or Claude chat:

```text
Set up AIkea Skill and help me design my furniture. Go to https://github.com/PatrickGrothOls/AIkea-skill and follow the getting-started instructions. Handle the setup and ask me for any necessary approvals.
```

Your assistant downloads the complete skill and installs its Python, CAD and
headless Blender dependencies. You may need to approve downloads, sign-in or
folder access. No coding application or manual terminal setup is required by
the installer. The chat must provide file downloads and command execution.

## Download

- [AIkea Skill installer](https://github.com/PatrickGrothOls/AIkea-skill/releases/download/v0.1.0-desktop.1/aikea-skill.zip)
- [SHA-256 checksum](https://github.com/PatrickGrothOls/AIkea-skill/releases/download/v0.1.0-desktop.1/SHA256SUMS)
- [Installation and completion requirements](docs/desktop-installation.md)

Version: `v0.1.0-desktop.1`. The archive contains all 11 skills and the editable source,
including the installer, construction tools and bundled viewer. Manufacturer CAD
and customer designs are not included.

## Instructions for the assistant

1. Download the ZIP above using your available file tools. Verify its SHA-256
   before extracting: `5cb2b09b68e95bfcc40d5f24ae8ef4a5c3d7a62ac4019dfebfacebb34e056ff9`.
2. Extract its single `aikea/` folder into a fresh directory. Read the extracted
   `SKILL.md` and `BOOTSTRAP.md`. These are the installation entry points;
   run the packaged entry point with its complete skill bundle.
3. Run the extracted `setup.sh` yourself as documented. Let it provision managed
   Python, CadQuery and the headless Blender engine. Inspect its stage logs and
   resolve recoverable errors. Request an ordinary approval when needed and
   continue once it arrives. Never ask for passwords in chat.
4. Require the real CAD solid, STEP round trip, GLB export, Blender bake and
   geometry checks to pass. `RUNTIME_VERIFIED` means these runtime checks passed;
   it does not mean the complete setup is ready.
5. Follow the packaged viewer instructions and deliver the actual model in a
   user-accessible interactive viewer. Verify rotation and zoom. In a hosted
   workspace, an internal localhost address is not accessible to the user;
   use a supported artifact/download route. A static image is not sufficient.
6. Record where the package, runtime and projects live and how to reopen them.
   Then read `skills/aikea/SKILL.md` and ask the first missing intake question,
   one topic at a time. Use only measurements supplied for this project.
7. Report `READY` only after integrity, CAD, Blender, interactive delivery and
   intake all succeed. If a required capability is unavailable, preserve progress
   and report the exact blocked stage and smallest required user action. Do not
   silently substitute a conversation-only workflow and call it installed.

## Compatibility

The installer supports macOS ARM64 and Linux x86_64. Desktop applications may
execute commands in a hosted Linux workspace; do not assume installation happens
on the user's computer. Allow approximately 4 GiB free plus project space.

This is a prerelease. Isolated macOS runtime checks passed; the runtime also ran
in a Claude hosted workspace. Complete interactive delivery from the hosted
workspace and ChatGPT Work acceptance remain unverified.

A working installation is not fabrication approval. Follow the skill's material,
hardware, machining and assembly checks before cutting any furniture.
