# MagicKit — operator macros for Claude Code

Five small skills that keep a long Claude Code session honest about **what it knows**, **what it already decided**, and **what it still owes you**. Stack-agnostic, no project files, no configuration. Home: **https://saidkit.dev**

Long sessions rot in predictable ways: constraints from turn 12 stop being applied by turn 60, the model proposes a default the project already rejected in an ADR, and the plan drifts from what was actually agreed. These skills are the interrupts for that.

| Skill               | Does                                                                          | Then |
| ------------------- | ------------------------------------------------------------------------------ | ---- |
| `/magic:revelio`    | Context refresh — surfaces what went stale or buried, plus 3–5 next actions    | STOP |
| `/magic:pensieve`   | Full scope/status audit end-to-end — status ledger, blockers, remaining path    | STOP |
| `/magic:lumos`      | Precedent search across CLAUDE.md, memory, ADRs, working dirs, probe records    | Reports |
| `/magic:session`    | Writes a handoff doc so a fresh session can pick the work up cold               | Confirms first |
| `/magic:think-deep` | Plans a complex task into steps, self-checks after each, keeps a live protocol  | Confirms first |

`revelio` and `pensieve` **stop on purpose**. They are diagnostics, not drivers — you read the output and decide. Pair them with the `locomotor!` macro when you want them to keep going.

## Install

```bash
claude plugin marketplace add saidkit/magic-skills
claude plugin install magic@magickit
```

Or in an active session: `/plugin marketplace add saidkit/magic-skills` → `/plugin install magic@magickit` → `/reload-plugins`.

## Then: add the macros

The plugin is half the kit. The other half is a block of **operator macros** you paste into your `CLAUDE.md` — they give you `revelio!` / `pensieve!` / `lumos!` / `session!` as inline shorthand, and define the autonomy verbs (`expelliarmus`, `locomotor!`) that the skills refer to.

**→ [docs/operator-macros.md](docs/operator-macros.md)** — copy the block, paste into `~/.claude/CLAUDE.md`.

Skipping this is fine; you just invoke the skills by their full `/magic:<name>` form and lose the `locomotor!` chaining.

## Typical use

```
# mid-session, the thread has drifted
revelio!                  → refresh, 3–5 next actions, stop
locomotor!                → refresh, then work the list autonomously

# before answering "what should the default be?"
lumos!                    → what the project already decided, with citations

# planning a long task, or after an interruption
pensieve!                 → full ledger: done / in flight / blocked / remaining

# out of context budget
session!                  → handoff doc for a fresh session

# a task big enough that step 4 will forget what step 1 decided
think!                    → plan, confirm, then step-by-step with self-checks
auror!                    → same, but runs the plan through without waiting
```

## What's in this repo

```
magic-skills/                            (marketplace-of-one)
├── .claude-plugin/marketplace.json      marketplace: magickit
├── plugins/magic/                       the plugin
│   ├── .claude-plugin/plugin.json
│   ├── skills/                          revelio · pensieve · lumos · session · think-deep
│   └── README.md
├── docs/operator-macros.md              the paste-in CLAUDE.md block
├── LICENSE                              MIT
└── README.md
```

## Related

[**SAID**](https://github.com/saidkit/said-skills) — the Scope → Architect → Implement → Debrief feature workflow. MagicKit is independent of it, but `lumos` and `session` were built against SAID's artifact layout (`docs/working/<feature>/`, ADRs, task logs) and are sharper on a SAID project.

## Contributing

Validate before opening a PR:

```bash
claude plugin validate .
claude plugin validate ./plugins/magic --strict
```

## License

MIT — see [LICENSE](LICENSE).
