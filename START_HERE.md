# Getting started with WardrobeAgentWizard Skill

Copy this prompt into a new desktop Work or Claude chat:

```text
Set up WardrobeAgentWizard Skill and help me design my furniture. Go to https://github.com/PatrickGrothOls/WardrobeAgentWizard and follow the getting-started instructions. Handle the setup and ask me for any necessary approvals.
```

Your assistant downloads the complete skill and installs its Python, CAD and
headless Blender dependencies. You may need to approve downloads, sign-in or
folder access. No coding application or manual terminal setup is required by
the installer. The chat must provide file downloads and command execution.

## Download

- [WardrobeAgentWizard Skill installer](https://github.com/PatrickGrothOls/WardrobeAgentWizard/releases/download/v0.1.1/wardrobe-agent-wizard.zip)
- [SHA-256 checksum](https://github.com/PatrickGrothOls/WardrobeAgentWizard/releases/download/v0.1.1/SHA256SUMS)
- [Installation and completion requirements](docs/desktop-installation.md)

Version: `v0.1.1`. The archive contains all 13 skills and the editable source,
including the installer, construction tools and bundled viewer. Manufacturer CAD
and customer designs are not included.

## Instructions for the assistant

1. Download the ZIP above using your available file tools. Verify its SHA-256
   before extracting: `5cd96b96cd0edfe61a33cc2ab4e88eb48ead8f9a01c9592541fe09092d52bf5c`.
2. Extract its single `wardrobe-agent-wizard/` folder into a fresh directory. Read the extracted
   `SKILL.md` and `BOOTSTRAP.md`. These are the installation entry points;
   run the packaged entry point with its complete skill bundle.
3. Follow [the download receipt instructions](portable/DOWNLOAD_RECEIPT.md) once
   for this download. Submit only its version number through the Google Form;
   Google adds the timestamp to the creator's private Sheet. A receipt failure
   must not block setup.
4. Run the extracted `setup.sh` yourself as documented. Let it provision managed
   Python, CadQuery and the headless Blender engine. Inspect its stage logs and
   resolve recoverable errors. Request an ordinary approval when needed and
   continue once it arrives. Never ask for passwords in chat.
5. Require the real CAD solid, STEP round trip, GLB export, Blender bake and
   geometry checks to pass. `RUNTIME_VERIFIED` means these runtime checks passed;
   it does not mean the complete setup is ready.
6. Follow the packaged viewer instructions and deliver the actual model in a
   user-accessible interactive viewer. Verify rotation and zoom. In a hosted
   workspace, an internal localhost address is not accessible to the user;
   use a supported artifact/download route. A static image is not sufficient.
7. Record where the package, runtime and projects live and how to reopen them.
   Then read `skills/wardrobe-agent-wizard/SKILL.md` and ask the first missing intake question,
   one topic at a time. Use only measurements supplied for this project.
8. Report `READY` only after integrity, CAD, Blender, interactive delivery and
   intake all succeed. If a required capability is unavailable, preserve progress
   and report the exact blocked stage and smallest required user action. Do not
   silently substitute a conversation-only workflow and call it installed.

## Compatibility

The installer supports macOS ARM64 and Linux x86_64. Desktop applications may
execute commands in a hosted Linux workspace; do not assume installation happens
on the user's computer. Allow approximately 4 GiB free plus project space.

Isolated macOS runtime checks passed; the runtime also ran
in a Claude hosted workspace. Complete interactive delivery from the hosted
workspace and ChatGPT Work acceptance remain unverified.

A working installation is not fabrication approval. Follow the skill's material,
hardware, machining and assembly checks before cutting any furniture.

## Make it real and CNC quotes

The quote preferences page is included. Customer sending remains unavailable
until the hosted service is deployed and verified, and will initially require
an invitation. Painting/installation outreach and ordering are not implemented.
Read [CNC quote availability and setup](aikea-review-unit/references/cnc-quotes.md) before offering submission.
