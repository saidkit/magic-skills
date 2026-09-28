---
name: prompt
description: |
  Generate a new prompt from the project's curated prompt library — in the operator's own terse voice — or `add` a good prompt back to that library. Reads the house corpus (the `MAGIC.prompts` key in CLAUDE.md → default `docs/prompts.md`), picks the most-relevant saved examples, and emits the prompt only. Activates ONLY on "/magic:prompt <…>" or "prompt!! <…>" — a generate `<ask>`, or the `add` capture verb — AND NOTHING ELSE. NOT for a build-to-a-bar prompt (that's gauntlet!!), a prompt-as-acceptance-contract (critic!!), or shaping a fuzzy goal (smart!!).
---

Read the project's prompt library, find the closest good examples, and write a new prompt in the operator's own voice — or `add` a good prompt to the library. Two verbs; report and STOP.

## Contract
- **Corpus.** Resolve the library path from the `MAGIC.prompts` key in the nearest `CLAUDE.md`; default `docs/prompts.md` when unset. Plain, terse markdown, one shot per `##` block (`## <case> — <when>` + the prompt body) — a human-maintained bridge; never rewrite it into a machine format.
- **Compose nothing heavy.** No critic loop, no embeddings / no index, no external service — read the small, curated corpus and judge relevance directly.
- **Report and STOP.** Emit the prompt (or the capture confirm) and stop; never run the generated prompt or continue into the work.
- **`add` is operand-guarded.** `add` is the capture verb ONLY as the operative token (bare, or `add` + an explicit "capture this" reference). A free-form ask that merely starts with "add …" — e.g. `prompt!! add a dark-mode toggle` — is a GENERATE request.

## `prompt!! <ask>` — generate
Resolve the corpus, read it, and pick the **most-relevant** shot(s) for the ask (judge relevance yourself — no index). Emit **a prompt only** — no preamble, no explanation, no wrapper — **terse** and **in the operator's voice**, mimicking the matched shots' phrasing and shape rather than a generic template. No close match → still a terse in-voice prompt from the nearest shots, never a verbose essay. Then STOP.

## `prompt!! add` — curate
File a good prompt into the library as a reusable case. Ask **at most two** questions to place it — the case label and when to reach for it — skipping either when clear from context. Then **append** one **least-verbose** shot (`## <case> — <when, ≤1 line>` + the prompt body) and nothing more. **Append-only** — never edit or reorder existing shots. If the resolved corpus file doesn't exist yet, **seed** it from `references/prompts.template.md` first, then append.

## References
- `references/prompts.template.md` — the shipped corpus template (shot shape + examples); seeds a fresh `docs/prompts.md`.
