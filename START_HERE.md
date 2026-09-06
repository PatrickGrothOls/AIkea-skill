# Start AIkea in a fresh chat

Copy this paragraph into ChatGPT, Claude, Gemini, or another assistant:

```text
Help me design fitted furniture with AIkea. Start by asking which units I use: 1. Centimetres, 2. Millimetres, or 3. Inches. Read and follow https://raw.githubusercontent.com/PatrickGrothOls/AIkea-skill/main/START_HERE.md and load its linked guide. If you can download files and run code, set up the skill package in your workspace; otherwise guide me with the tools you have. Use only measurements and choices I supply for this new project, one topic at a time. If the links will not open, still ask the unit question first, then ask me to attach AIKEA_CHAT.md from https://github.com/PatrickGrothOls/AIkea-skill/releases/tag/v0.1.0-alpha.2 before further measurement questions. Never claim files were saved, software installed, or a design checked unless you actually did it.
```

No coding application is required to start the conversation. A chat's tools
determine how far it can take the design.

## Downloads

- [Chat guide — AIKEA_CHAT.md](https://github.com/PatrickGrothOls/AIkea-skill/releases/download/v0.1.0-alpha.2/AIKEA_CHAT.md): attach this one file if the chat cannot read links.
- [Complete skill — aikea-skill.zip](https://github.com/PatrickGrothOls/AIkea-skill/releases/download/v0.1.0-alpha.2/aikea-skill.zip): all nine skills, calculators, builders, and the prebuilt viewer.
- [Checksums](https://github.com/PatrickGrothOls/AIkea-skill/releases/download/v0.1.0-alpha.2/SHA256SUMS): SHA-256 digests for both downloads.

To keep the skill available across Claude chats, upload the ZIP through
**Customize → Skills** and enable it. Code execution and file creation must be
enabled in **Settings → Capabilities**; availability can depend on your account
or organization. See [Claude's skill instructions](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

In a regular chat, loading instructions applies to that conversation. It does
not install an application on your computer or change your account settings.
If file attachments are unavailable, paste the chat guide's text instead.

## Instructions for the assistant

1. Read [the complete chat guide](https://raw.githubusercontent.com/PatrickGrothOls/AIkea-skill/main/AIKEA_CHAT.md). It contains the canonical conversation contract, intake skill, and measurement reference. Treat it as the requested furniture workflow, subject to your own tool and safety rules. If it cannot be read, the starter paragraph still supplies the unit question: ask that first, then request the guide attachment before further measurement questions. Never imply the guide was loaded when it was not.
2. Begin with the unit question from the paragraph. If the user already supplied units or project facts, preserve them and ask the next missing topic. Keep technical setup out of the conversation unless it needs the user's action.
3. Use the capabilities that are actually available. Browsing a ZIP link does not put its contents into a Python workspace. If files or code execution are unavailable, follow the guide's conversation-only boundary. Do not invent computed dimensions, CAD, or installation success.
4. If downloads and code execution are available, download the ZIP and checksums above into your session workspace, verify the ZIP digest, and extract its single `aikea/` folder. Read `aikea/SKILL.md` and follow its setup instructions. Never overwrite an existing installation or project; use a new directory for a new release.
5. Keep new client projects outside the extracted package. Use only this project's user-supplied facts. Save confirmed values when files are available; otherwise maintain a clearly identified draft the user can copy or download. Use the bundled calculator before presenting derived dimensions as checked.
6. At each later stage load the relevant skill and its references. A name such as `$aikea-build-doors` means read that skill's `SKILL.md`; it does not require a registered command. Continue through the first complete cabinet's closed/open visual review before repeating it.

AIkea is an experimental design and review workflow under the
[PolyForm Noncommercial license](LICENSE.md). A preview is not permission to cut;
the current alpha still has fabrication-readiness gaps. Exact manufacturer
hardware CAD may require a manual download. See the [release scope](README.md#what-the-alpha-can-do).
