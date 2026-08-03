# Changelog

## 0.2.0 — 2026-08-03

`magic:think-deep` gains two rules, both from a live post-mortem in which a plan silently
dropped a verification stage and then reported the work complete.

**Added — loop-shaped `via:` bindings (Phase 1).** When a `via:` names a skill whose contract
is a re-entrant loop, the step must read *"drive X to its stop condition via repeated
invocation"*, not *"invoke X"*, and the plan must carry a final step that re-invokes it and
records its stop-condition output verbatim. Invoking a loop once demotes it to a subroutine:
every rule it would have enforced on later passes becomes unreachable, the plan's own steps
become the only enforcement, and a step that quietly fails to run leaves none.

**Added — checkbox integrity (Phase 2 self-check).** A step may not be marked `[x]` while its
Results entry reads pending / blocked / not started. The observed failure was exactly this —
all steps ticked, Results reading *"pending steps 5–6"*, and nothing detecting the
contradiction for two sessions.

**`docs/operator-macros.md`** — two `flow!` changes. It now instructs **driving `said:flow` to
its stop condition** rather than invoking it once. And its opening line no longer names one
project's directories (`FE / BE / shared engine`) — those were *mounts*, not lanes. It states
the test instead: **spans two or more task logs; a lane is not a repo or a mount**, and one
feature may touch several mounts and stay single-lane. The enforcement clause also now names
`Skill(said:flow)` rather than the retired pre-plugin skill id. Pairs with `said` 0.2.0.

## 0.1.0 — 2026-07-27

Initial release. Five skills migrated from personal `~/.claude/skills/` into the `magic` plugin under the `magickit` marketplace.

- `magic:revelio` — context refresh (was `magic-revelio`)
- `magic:pensieve` — scope / status audit (was `magic-pensieve`)
- `magic:lumos` — precedent / decision-record search (was `magic-lumos`)
- `magic:session` — new-session handoff (was `magic-session`)
- `magic:think-deep` — structured task orchestrator (was `think-deep`)

Migration notes:

- Skills are now namespaced by the plugin: `/magic-revelio` → `/magic:revelio`, `/think-deep` → `/magic:think-deep`, and so on. Update any `CLAUDE.md` macros that referenced the old names.
- `docs/operator-macros.md` ships the `CLAUDE.md` macro block (`revelio!`, `pensieve!`, `lumos!`, `session!`, `think!`, `auror!`, `expelliarmus`, `locomotor!`) that the skills were designed against — previously personal-config-only, now part of the distribution.
- `think-deep` wrote its execution protocol to a hardcoded `/home/claude/think-deep-protocol.md`. That path only exists in a Linux sandbox; the ported skill resolves a `<protocol-dir>` at runtime (project working dir, else session scratch) and reports the resolved path in chat.
