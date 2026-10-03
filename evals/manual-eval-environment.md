# Manual AIkea eval environment

Use one empty temporary folder and one fresh model conversation for each eval case. The model may see the installed AIkea skill and the user messages for that case. It must not see the eval set, expected answers, development documentation, or files from another run.

## 1. Create an empty project folder

```bash
AIKEA_EVAL_DIR="$(mktemp -d /private/tmp/aikea-overall-wardrobe-eval.XXXXXX)"
cd "$AIKEA_EVAL_DIR"
```

Keep this folder for every turn in the same conversation. Create a new folder before starting another case or model.

## 2. Start a fresh Codex conversation

Use the Codex executable configured on your PATH:

```bash
codex exec \
  --skip-git-repo-check \
  --disable memories \
  '$aikea I want to build a built-in wardrobe for a bedroom wall. I have not taken any measurements or chosen the cabinet settings yet. Help me start.'
```

Check `codex exec --help` for the installed version before an automated run.
Keep the normal permission checks enabled.

Send the next turn from the same temporary folder:

```bash
codex exec resume \
  --last \
  --skip-git-repo-check \
  --disable memories \
  'NEXT USER MESSAGE'
```

Because the folder is unique to one case, `--last` selects that case's most recent conversation. A saved session ID may be supplied instead when several conversations have been run from the same folder.

## 3. Start a fresh Claude conversation

Use the long `--print` option rather than its `-p` alias:

```bash
claude \
  --bare \
  --print \
  --output-format json \
  --permission-mode acceptEdits \
  --name "AIkea overall wardrobe eval" \
  '/aikea I want to build a built-in wardrobe for a bedroom wall. I have not taken any measurements or chosen the cabinet settings yet. Help me start.'
```

Copy the `session_id` from the JSON response, then continue that conversation:

```bash
claude \
  --resume SESSION_ID \
  --bare \
  --print \
  --output-format json \
  --permission-mode acceptEdits \
  'NEXT USER MESSAGE'
```

## 4. Score the case

After every turn:

1. Save the model's response outside the temporary project folder.
2. Compare it with that turn's answer key in the eval set being run.
3. Fail the case if any forbidden behavior occurs.
4. When a case includes final project values, compare the generated `aikea.yaml`
   and calculated dimensions with the expected values. Next-question cases stop
   after scoring the response.
5. Record the model, session ID, pass or fail result, and short failure notes.

Do not correct the model during a case. A changed prompt is a new eval case and requires a new empty folder and conversation.

`--disable memories` prevents Codex from loading saved knowledge from previous projects. Claude's `--bare` mode removes project instructions, plugins, hooks, and automatic memory while retaining skill discovery; it requires API-key or configured helper authentication. These isolation flags matter because an empty folder alone does not prevent unrelated saved context from reaching the model.
