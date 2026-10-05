# Watch furniture come together

Start one local viewer before building, keep the process running, and open its
printed URL. The host needs the installed CadQuery environment and access to a
local browser. A remote AI service cannot show its localhost on the client's
computer; use the existing hosted review path there and disclose that limitation.

```sh
direnv exec . python <package>/aikea-review-unit/scripts/watch_furniture_build.py <project> --assembly <root_id>
```

The watcher waits for saved construction inputs to settle, then rebuilds the root.
It watches `aikea.yaml`, assembly Python files, `features.json` and drawer layout
policy. It does not run on every keystroke or watch external vendor CAD changes.
If those change, restart the watcher. `--no-open` prints the URL without launching
a browser; `--port` can choose a fixed local port.

Each completed machined panel from the current `PanelAssemblyBuilder` is published
immediately. The preview reuses unchanged meshes, fades new/replaced parts in and
shimmers only across the assembly currently building. It checks the complete tree
after construction, including final feature modifications and purchased hardware.
The camera fits growing geometry until the user first interacts; after that their
camera is retained. **Fit furniture** frames the current result again. Reduced
motion disables both fade and shimmer.

A failed build retains the latest visible geometry and shows a failure. During a
rebuild it can contain previous parts awaiting replacement; the status says so.
Checks passing means ready for design review, never fabrication approval. Formal
review remains bound to its own immutable checked files. Stop with Ctrl+C; the
browser reports disconnection and stops the animation. The temporary part cache
is removed when the process exits normally. No model is uploaded.

## Authored nested builders

Generated wardrobe roots already supply their declared child frames. For custom
nesting, wrap the actual child build so part events carry the correct placement:

```python
from live_build_progress import LiveBuildChild

with LiveBuildChild(child_spec):
    child = BuiltChildAssembly(child_spec, child_builder.build())
```

For a custom part builder that does not use `PanelAssemblyBuilder`, emit
`LiveBuildProgress.started(assembly_spec)` before work and
`LiveBuildProgress.part(assembly_spec, built_part)` after each final solid.
These are optional observation hooks; they do not approve or alter geometry.
Do not publish blanks as if their machining were finished.

Older projects retain their local shared contracts. Reconcile their
`assemblies/panel_assembly.py` with the current template deliberately; never
overwrite authored files blindly. Builders without hooks or known parent frames
still update at the complete-tree checkpoint, but cannot promise per-part progress.
Feature-generated hardware and modified host panels currently appear at that
checkpoint. Do not simulate that missing progress with a timed animation.
