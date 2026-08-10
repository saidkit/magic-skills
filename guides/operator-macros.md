# Operator macros

The `magic` plugin ships six skills. The **macro block that drives them** — the autonomy verbs and the inline shorthands — lives in **[`guides/CLAUDE.md`](./CLAUDE.md)** beside this file. That is the single source; this page keeps **no copy of the macros**, it only explains what the block is and how to install it.

A Claude Code plugin cannot add text to your `CLAUDE.md`, and the macros are the orchestration layer: they define the autonomy verbs (`expelliarmus`, `locomotor!`, `auror!`) that the skills refer to when they say "do not continue unless paired with `locomotor`".

Without the block the skills still work — you invoke them as `/magic:revelio`, `/magic:pensieve`, `/magic:session`, `/magic:think-deep`, `/magic:critic`, `/magic:gauntlet`. With it, they work the way they were designed to.

## Install

Paste the contents of **[`guides/CLAUDE.md`](./CLAUDE.md)** (beside this file) into **`~/.claude/CLAUDE.md`** (applies to every project) or a project's **`./CLAUDE.md`** (that project only).

## Notes

- **`expelliarmus` is load-bearing.** `locomotor!` and `pensieve locomotor!` are defined in terms of it, and `/magic:pensieve` names it in its stop condition. Keep it even if you never type it directly.
- **`lumos!` targets `/said:retrieval`.** Precedent/decision-record search moved to the SAID plugin (`said:retrieval`); the `lumos!` macro is kept in the block but needs the `said` plugin installed.
- **Keep the `!` suffix meaningful.** Across this macro family the bare word and the `!` form do the same thing; the `!` is a readability cue that the operator means the macro, not the English word.
- **Macros do not carry across invocations.** This is deliberate — every macro is scoped to the message that invoked it, so an autonomy grant can never silently persist into later work.
