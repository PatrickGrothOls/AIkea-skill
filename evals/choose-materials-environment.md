# Material-advice eval environment

Run every case in a new project folder and a new conversation. The model may see
the copied AIkea skills, the selected project fixture, the declared evidence
files, attachments, and the case's user message. It must not see
`choose-materials.yaml`, expected files, or another case.

## Prepare one case

Read the case's `setup` block in `choose-materials.yaml`. Then run:

```sh
AIKEA_MATERIAL_SOURCE="/path/to/AIkea-skill"
AIKEA_MATERIAL_CASE="$(mktemp -d /private/tmp/aikea-material-eval.XXXXXX)"
cp -R "$AIKEA_MATERIAL_SOURCE/evals/PROJECT_FIXTURE/." "$AIKEA_MATERIAL_CASE/"
mkdir -p "$AIKEA_MATERIAL_CASE/.agents/skills" "$AIKEA_MATERIAL_CASE/.claude/skills"
for AIKEA_SKILL_SOURCE in "$AIKEA_MATERIAL_SOURCE"/aikea*; do
  if [ -f "$AIKEA_SKILL_SOURCE/SKILL.md" ]; then
    AIKEA_SKILL_NAME="$(basename "$AIKEA_SKILL_SOURCE")"
    cp -R "$AIKEA_SKILL_SOURCE" "$AIKEA_MATERIAL_CASE/.agents/skills/$AIKEA_SKILL_NAME"
    cp -R "$AIKEA_SKILL_SOURCE" "$AIKEA_MATERIAL_CASE/.claude/skills/$AIKEA_SKILL_NAME"
  fi
done
```

Replace `PROJECT_FIXTURE` with the case's exact `project_fixture` value. Copy
each declared `evidence_files[].source` to its `destination` inside the case folder.
Do not copy an `expected_aikea_yaml` fixture into the case folder.

## Run the case

From `AIKEA_MATERIAL_CASE`, start a fresh Codex conversation with the case's
exact `next_user_message` after the skill invocation:

```sh
/Applications/ChatGPT.app/Contents/Resources/codex exec \
  --skip-git-repo-check \
  --disable memories \
  --approve-for-me \
  '$aikea-choose-materials NEXT_USER_MESSAGE'
```

When `attachments` is present, add one `--image` argument per declared source
path before the prompt. The source path is relative to `evals/` in the source
repository. Claude runs use the same copied project and exact message; attach the
declared image through its client interface.

## Score the case

Score every required and forbidden response and inference item. If
`expected_aikea_yaml` is `unchanged`, compare the final file byte-for-byte with
the copied starting file. Otherwise compare the parsed final YAML exactly with
the declared expected fixture. Inspect any other required saved record
semantically. Record the model, session ID, case name, pass or fail, and concise
failure evidence. Never correct the model mid-case.
