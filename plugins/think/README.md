# Think — divergent front-doors for Claude Code

Front-door thinking skills that run *before* you commit to a target. Where the `magic` plugin keeps a long session honest about what it knows and already decided, `think` helps you **find the right thing to build in the first place** — generate real options and adversarially select the best.

| Skill            | Does                                                                              | Then |
| ---------------- | --------------------------------------------------------------------------------- | ---- |
| `/think:ideate`  | Generate 5–15 genuinely diverse candidate ideas, adversarially select the best against a pinned merit rubric | Returns the top-N, STOPS |

`ideate` **composes** the `magic` plugin's `critic` as its judge, and hands its winners to `think!` / `auror!` / `gauntlet!` (and `smart!` once it ships). It explores the solution space — it never builds. It is the divergent mirror of `gauntlet` (which converges: one target, built to a blind bar).

## Install

```bash
claude plugin marketplace add saidkit/magic-skills
claude plugin install think@magickit
```

Or in an active session: `/plugin marketplace add saidkit/magic-skills` → `/plugin install think@magickit` → `/reload-plugins`.

`ideate` composes `critic`, which ships in the `magic` plugin — install that too:

```bash
claude plugin install magic@magickit
```

## Trigger

`ideate! <problem>` or `/think:ideate <problem>` — explicit only; it never fires by accident.
