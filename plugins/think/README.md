# Think — front-door thinking skills for Claude Code

Front-door skills that run *before* you commit to how you'll build. Where the `magic` plugin keeps a long session honest about what it knows and already decided, `think` helps you **get the target right in the first place** — sharpen a fuzzy goal, or generate and select among real options.

| Skill            | Does                                                                                          | Then |
| ---------------- | --------------------------------------------------------------------------------------------- | ---- |
| `/think:smart`   | Sharpen a vague goal into a **measurable + convergent** statement a run can finish — the kit's **IFR builder** | Emits the sharpened goal, STOPS |
| `/think:ideate`  | Generate 5–15 genuinely diverse candidate ideas, adversarially select the best against a pinned merit rubric   | Returns the top-N, STOPS |

Both are **feeders** — they shape the work and STOP. `smart` points a sharpened goal at `think!` / `auror!` (or `critic!` for a quality bar); `ideate` **composes** `critic` as its judge and hands its winners to `smart!` / `think!` / `auror!` / `gauntlet!`. Neither touches an engine — each emits plain text. `smart` pins a goal's **Ideal Final Result** before the loop runs; `ideate` explores the option space (the divergent mirror of `gauntlet`).

## Install

```bash
claude plugin marketplace add saidkit/magic-skills
claude plugin install think@magickit
```

Or in an active session: `/plugin marketplace add saidkit/magic-skills` → `/plugin install think@magickit` → `/reload-plugins`.

Both skills lean on `critic`, which ships in the `magic` plugin — install that too:

```bash
claude plugin install magic@magickit
```

## Triggers

- `smart! <goal>` or `/think:smart <goal>` — sharpen a fuzzy goal into a finishable one.
- `ideate! <problem>` or `/think:ideate <problem>` — explore + adversarially select ideas.

Explicit only; neither fires by accident.
