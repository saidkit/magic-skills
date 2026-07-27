# Changelog

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
