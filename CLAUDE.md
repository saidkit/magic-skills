# magic-skills — repo conventions

This repo is a Claude Code **plugin marketplace of one**. It ships prompts, not code.

## Layout invariants

- `.claude-plugin/marketplace.json` — marketplace `magickit`. Its `name` must stay distinct from every other marketplace the author publishes (`saidkit`, for said-skills): Claude Code registers **one marketplace per name**, and a duplicate name silently replaces the earlier registration for the user.
- `plugins/magic/` — the plugin. `skills/` sits at the **plugin root**, never inside `.claude-plugin/`.
- Skill directory names are the invocation names. `skills/revelio/SKILL.md` → `/magic:revelio`. Renaming a directory is a breaking change for anyone's `CLAUDE.md` macros.
- `docs/operator-macros.md` — the paste-in `CLAUDE.md` block. A plugin cannot write to a user's `CLAUDE.md`, so any macro the skills reference in their bodies must be defined here or the skill ships inert.

## Editing skills

- Frontmatter `name:` must equal the directory name.
- `description:` is what routes the skill — it is read at dispatch time, so it must name both the explicit command (`/magic:revelio`) and the macro form (`revelio!`).
- Skill bodies must stay project-agnostic: no hardcoded paths, no assumed doc layout, no stack assumptions. Where a project convention is needed, describe the shape and let the skill discover the project's actual equivalent.

## Before committing

```bash
claude plugin validate .
claude plugin validate ./plugins/magic --strict
```

Bump `version` in **both** `.claude-plugin/marketplace.json` and `plugins/magic/.claude-plugin/plugin.json` together — the validator warns when they diverge, and `plugin.json` wins at runtime. Add a `CHANGELOG.md` entry in the same commit.
