---
name: gauntlet
description: >
  Assemble and PRINT a gauntlet-loop prompt (fan out a builder+critic fleet, /loop until a blind-comparative bar) for a subjective/quality target — anchor pinned first. Emits prompt text only; never runs it. 
  Triggered ONLY by the explicit command "/magic:gauntlet" or "gauntlet!" invocation AND NOTHING ELSE.
---

# Gauntlet — gauntlet-loop prompt assembler

## Contract — holds every run
- **Assemble + print only.** Emit the prompt and STOP — never orchestrate, `/loop`, or spawn.
- **Pin the anchor first.** `Skill(magic:critic)` before writing; no reference obtainable ⇒ hard-block.
- **Output the canonical form.** The three flowing paragraphs below with `<target>` · `<anchor>` · items · modality swapped in — NOT a terse spec, NOT a K/N rubric, NOT an orchestration keyword.

## 1 — Pin the anchor (via critic)
`Skill(magic:critic)` on the target → the named **anchor** to match/beat · the **reference** to compare against · the **modality** (looks / sounds / feels). No reference ⇒ hard-block.

## 2 — Decompose into items
Split the target into the independently-buildable parts the fleet fans out over — a game → textures · physics · lighting · geometry · movement · sound; a page → hero · pricing · footer; a scene → rooms · props · lighting.

## 3 — Write the prompt (the canonical gauntlet-loop form)
Fill the three paragraphs; keep the wording, swap in `<target>` · `<anchor>` · the items · the modality (**looks** / **sounds** / **feels**):

1. *I want you to build `<target>` at the level of `<anchor>`. It should be utterly perfect, `<visually beautiful / on-brand / …>`, with every single thing done at the highest quality—from `<item>` to `<item>` to anything you could think of.*
2. *Fan out sub-agents and have sub-agents tackle each one individually so that the `<target>` is utterly perfect. You should /loop on each item and have a separate sub-agent check it `<visually / by listening / by playing it>` against `<anchor>`. That separate sub-agent should be a really harsh critic, and if it doesn't match, it should keep going.*
3. *Don't stop until each sub-agent is utterly wowed with the quality when compared with `<the actual anchor>`. It should literally compare them side by side blind and say which one `<looks / sounds / feels>` better. `<tech constraint, e.g. Do this in ThreeJS.>` /loop until it's utterly perfect. Fan out sub-agents.*

## 4 — Print
Emit the filled three paragraphs as ONE fenced block. Stop — do not run it.

## Example — the canonical prompt (game)
`/magic:gauntlet — build a first-person shooter at the level of the most recent Call of Duty games, in ThreeJS` →

```
I want you to build a first-person shooter at the level of the most recent Call of Duty games. It should be utterly perfect, visually beautiful, with every single thing done at AAA quality—from textures to physics to anything you could think of.

Fan out sub-agents and have sub-agents tackle each one individually so that the game is utterly perfect. You should /loop on each item and have a separate sub-agent check it visually to ensure it looks triple A. That separate sub-agent should be a really harsh critic, and if it doesn't look triple A, it should keep going.

Don't stop until each sub-agent is utterly wowed with the quality when compared with the actual Call of Duty game. It should literally compare them side by side blind and say which one looks better. Do this in ThreeJS. /loop until it's utterly perfect. Fan out sub-agents.
```

## Example — a UI (modality: looks)
`/magic:gauntlet — make our pricing-page hero as polished as ref/hero.png` →

```
I want you to build a pricing-page hero at the level of ref/hero.png. It should be utterly perfect, visually beautiful and on-brand, with every single part done at the highest quality—from the headline to the CTA to the layout to anything you could think of.

Fan out sub-agents and have sub-agents tackle each part individually so that the hero is utterly perfect. You should /loop on each item and have a separate sub-agent check it visually against ref/hero.png. That separate sub-agent should be a really harsh critic, and if it doesn't match ref/hero.png, it should keep going.

Don't stop until each sub-agent is utterly wowed with the quality when compared with ref/hero.png. It should literally compare them side by side blind and say which one looks better. /loop until it's utterly perfect. Fan out sub-agents.
```

## When NOT to use
Objective/spec target · no reference obtainable (nothing to compare against side by side).
