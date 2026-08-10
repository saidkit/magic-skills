---
name: gauntlet
description: >
  Assemble and PRINT a gauntlet-loop prompt (fan out a builder+critic fleet, /loop until a blind-comparative bar) for a subjective/quality target — anchor pinned first. Emits prompt text only; never runs it. 
  Triggered ONLY by the explicit command "/magic:gauntlet".
---

# Gauntlet — gauntlet-loop prompt assembler

## Contract — holds every run
- **Assemble + print only.** Emit the prompt and STOP — never orchestrate, `/loop`, or spawn.
- **Pin the bar first.** `Skill(magic:critic)` before assembling; no reference obtainable ⇒ hard-block.
- **Engine-agnostic.** Bake no orchestration keyword into the prompt — the operator picks how to run it.

## 1 — Pin the bar (via critic)
`Skill(magic:critic)` on the target → anchor · reference artifact · comparative `Done-when` (judge blind vs the reference, whole-artifact, stop at `≥K of N`). No reference ⇒ hard-block.

## 2 — Decompose into items
Split the target into the independently-buildable, independently-judgeable parts the fleet fans out over — e.g. a page → hero / pricing / footer; a 3D scene → rooms / props / lighting; a report → sections. Each item gets its own builder+critic loop.

## 3 — Fill the 3 slots
- **Task (what):** build <target> at the level of <anchor> — every part to that bar.
- **Build method (how):** fan out sub-agents, one per item; `/loop` each; a separate harsh critic checks each **blind** against <reference> (unlabeled A/B), whole-artifact; below the bar ⇒ keep going.
- **Bar (when to stop):** <critic's comparative `Done-when`> — each item passes when it wins `≥K of N` blind looks vs <reference>; don't stop until every item passes.

## 4 — Print
Emit the filled prompt as ONE fenced block, ready to paste/run. Stop — do not run it.

## Examples

### Canonical (the source technique) — a game
Input: `/magic:gauntlet — build a first-person shooter at the level of the most recent Call of Duty games, AAA quality (textures, physics, everything), in ThreeJS`

Phase 1 (critic) pins: anchor = the most recent Call of Duty games (AAA); reference = CoD gameplay footage/screenshots; bar = blind side-by-side vs the actual game, ≥4/5.
Phase 2 items = textures · physics · lighting · level geometry · weapons/animation · sound.
Printed prompt:

```
Task: Build a first-person shooter in ThreeJS at the level of the most recent Call
of Duty games — every part (textures, physics, lighting, level geometry, weapons/
animation, sound) at that AAA bar.

Build method: Fan out sub-agents, one per part; /loop each. A separate harsh critic
checks each part BLIND against footage of the actual Call of Duty game (unlabeled,
side-by-side), judging the whole part — not a feature checklist. If it doesn't look
AAA, keep going.

Bar: A part passes when, judged blind side-by-side against the actual Call of Duty
game, it is picked as matching-or-better in ≥4 of 5 looks. Don't stop until every
part passes.
```

### A UI
Input: `/magic:gauntlet — make our pricing-page hero as polished as ref/hero-exemplar.png, on-brand with ref/brand-kit.md`

Phase 1 (critic) pins: anchor = `ref/hero-exemplar.png`; reference = that screenshot + `ref/brand-kit.md`; bar = blind vs the exemplar, whole-artifact, ≥4/5.
Phase 2 items = headline block · CTA · supporting visual · layout/spacing.
Printed prompt:

```
Task: Build the pricing-page hero at the level of ref/hero-exemplar.png — every
part (headline, CTA, supporting visual, layout) to that bar, on-brand with
ref/brand-kit.md.

Build method: Fan out sub-agents, one per part (headline block, CTA, supporting
visual, layout/spacing); /loop each. A separate harsh critic checks each part
BLIND against ref/hero-exemplar.png (render vs reference, unlabeled, positions
re-randomized), judging the whole part — composition, hierarchy, type, color,
spacing, finish — not a feature checklist. Below the bar ⇒ keep iterating.

Bar: A part passes when it matches-or-beats ref/hero-exemplar.png in ≥4 of 5 blind
looks; also enforce brand-token conformance to ref/brand-kit.md (colors/type/
spacing ∈ kit). Don't stop until every part passes.
```

## When NOT to use
Objective/spec target · no reference obtainable.
