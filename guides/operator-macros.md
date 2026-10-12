# Operator macros

The `magic` plugin ships eleven skills. The **macro block that drives them** — the autonomy verbs and the inline shorthands — lives in **[`guides/CLAUDE.md`](./CLAUDE.md)** beside this file. That is the single source; this page keeps **no copy of the macros**, it only explains what the block is and how to install it.

A Claude Code plugin cannot add text to your `CLAUDE.md`, and the macros are the orchestration layer: they define the autonomy verbs (`proceed!!`, `resume!!`, `run!!`) that the skills refer to when they say "do not continue unless paired with `resume!!`".

Without the block the skills still work — you invoke them as `/magic:refresh`, `/magic:audit`, `/magic:session`, `/magic:think-deep`, `/magic:critic`, `/magic:gauntlet`, `/magic:ruled`, `/magic:worklog`. With it, they work the way they were designed to.

## Install

Paste the contents of **[`guides/CLAUDE.md`](./CLAUDE.md)** (beside this file) into **`~/.claude/CLAUDE.md`** (applies to every project) or a project's **`./CLAUDE.md`** (that project only).

## Notes

- **`proceed!!` is load-bearing.** `resume!!` is defined in terms of it, and `/magic:audit` names it in its stop condition. Keep it even if you never type it directly.
- **`precedent!!` targets `/said:retrieval`.** Precedent/decision-record search moved to the SAID plugin (`said:retrieval`); the `precedent!!` macro is kept in the block but needs the `said` plugin installed.
- **`!!` is the operator-macro marker.** Every operator macro ends in `!!` — the double bang is what tells the agent you mean the macro, not the English word. One form per macro: no bare-word or single-`!` variants.
- **Macros do not carry across invocations.** This is deliberate — every macro is scoped to the message that invoked it, so an autonomy grant can never silently persist into later work.
