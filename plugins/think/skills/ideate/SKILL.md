---
name: ideate
description: >
  Divergent front-end for a problem/question: generate 5–15 genuinely diverse candidate ideas (each from a distinct lens), adversarially review them against a pinned merit rubric (composing `critic`), and return the top N (default 3, `N=1` on request) with the rationale each survived on + its main risk — then STOP, feeding the winners to think! / auror! / gauntlet! / smart!. Diverge → judge → select; it explores options, it never builds them.
  Activates ONLY on an explicit `/think:ideate <problem>` or `ideate! <problem>` invocation AND NOTHING ELSE.
---

# Ideate — divergent generation + adversarial selection

Explore the solution space *before* committing: **diverge → adversarially judge → select top-N**. The missing front-door — every other skill assumes the target is already chosen. Compose the judge (`critic`), never hand-roll it; **run** the loop and return the winners; then **STOP** — selection is not execution.

## Invocation & parameters
`/think:ideate <problem>` or `ideate! <problem>` — `<problem>` = a question · goal · decision. Optional trailing param:

| Param | Effect |
|---|---|
| *(none)* | top **N = 3**, field auto-sized 5–15 by complexity |
| `N=1` / `top 1` | return the single best idea |
| `N=<k>` | return the top k |

## Contract — holds every run
- **Diverge, don't vary.** Each candidate from a **distinct lens** (`references/lens-catalog.md`); make the lens explicit so near-duplicates are visible and pruned. Free-form "15 ideas" collapses to one idea × 15 (mode collapse) and the review becomes theater.
- **Pin the rubric first (the anchor).** Ideas have no external reference, so the **merit rubric IS the anchor** — author it *before* judging or the tournament is vibes (unpinned-anchor drift).
- **Compose `critic` as the judge; author no bespoke scorer.** The merit rubric is the pinned **standard** — yours to author (from the catalog + critic's *pin-the-standard-first* discipline); the adversarial **review** of each idea against it is **driven by `Skill(magic:critic)`** (review mode, refute-first — or its refute-first library inline when a subagent / large field). You add only the divergence + the comparative ranking; hand-rolling the review is the #1 emulation failure.
- **Comparative selection.** Refute-each-then-rank (≤8 ideas) or pairwise tournament (larger field) — never independent absolute 1–10 scores (they rank top-1 unreliably).
- **Depth-0, then STOP.** Return the top-N + rationale; do NOT continue into building/executing. As a subagent (can't spawn), generate + judge **inline**; never nest-spawn.

## Phase 0 — Frame + pin the rubric
Restate the problem in one line. Pin the **merit rubric** — the axes an idea is judged on (feasibility · fit-to-intent · impact · novelty · effort/risk), weighted to the problem (see `references/lens-catalog.md`; apply `critic`'s *pin-the-standard-first* discipline). This rubric is the **standard** the judging holds every idea to. Choose the divergence lenses, the field size (5–15, by complexity), and **N** (default 3).

## Phase 1 — Diverge
Generate one idea per lens/angle to the target count — a multi-modal sweep. At depth-0 you may fan out one generator per lens; inline otherwise. **Tag each idea with its lens.** Prune obvious near-duplicates so the field is genuinely varied; record how many were pruned.

## Phase 2 — Judge + select + hand off
**Judge via `critic`.** Invoke `Skill(magic:critic)` in **review mode**, holding each idea to the pinned rubric as its standard (refute-first — surface its fatal flaw / worst-fit axis); as a subagent or for a large field, apply critic's refute-first review discipline inline. **critic is the judge — author no scorer.** Then select **comparatively** — refute-each-then-rank (≤8) or pairwise tournament (larger) — ranking by what survives the refutation. Emit the **top N**, each with *why it survived* (rubric fit) and *its main risk*; then STOP with the handoff line.

```
Problem:  <one line>          Rubric: <axis · axis · axis>   (N = 3)
Field:    <k ideas, each tagged by its lens>   (pruned m near-duplicates)

Top 3
1. <idea> — survives: <rubric fit> · risk: <main weakness>
2. <idea> — survives: … · risk: …
3. <idea> — survives: … · risk: …
→ run it: think!/auror! <idea>  ·  build to a bar: gauntlet! <idea>  ·  sharpen first: smart! <idea>
```

## Boundary — vs `gauntlet` (the mirror twin)
Distinct on four axes: **ideas** not builds · **rubric** not external-reference · **diverge** not converge · **run** not print. `ideate` explores options (the front); `gauntlet` builds the chosen one to a blind-comparative bar (the back). No blind-vs-exemplar judging here — there is no exemplar; the rubric is the anchor.

## When NOT to use
Target already chosen → `think!` / `auror!` (build it) · `gauntlet!` (build to a bar) · `smart!` (sharpen it). · A single-answer question with no solution space to explore. · Judging that needs an external-reference blind A/B → that is `gauntlet!`, not this.
