---
name: smart
description: >
  Front-door goal-shaper: turn a vague goal into a think-deep-ready statement carrying the two properties a run needs — Measurable (a success signal a gate can evaluate) and Convergent (a reachable stop, not "as good as possible") — with light Specific/Relevant (anti-drift) + Achievable (feasibility) checks, then hand off to think! / auror! (and critic! for a quality bar). It shapes the GOAL (aka IFR); it never authors the Done-when or the bar. Emit and STOP.
  Activates ONLY on an explicit `/think:smart <goal>` or `smart! <goal>` invocation AND NOTHING ELSE.
---

# Smart — front-door goal-shaper (the kit's IFR builder)

Sharpen a fuzzy goal *before* the loop runs — goal quality is the upstream lever on run quality; a soft goal yields a soft gate that drifts or spins. `smart` pins the goal's **Ideal Final Result**: a specific objective, a **measurable** success signal, and a **convergent** stop — the checkable end-state `think!` / `auror!` then aim at. It **names** the measure and **defers** the executable check to think-deep and the quality bar to critic.

## Invocation
`/think:smart <goal>` or `smart! <goal>` — `<goal>` = a fuzzy objective. Default: shape + emit, then **STOP**. `smart! <goal> then think!` / `then auror!` = after emit, offer to drive the sharpened goal inline (opt-in).

## Contract — holds every run
- **The two-point core (non-negotiable).** Never emit a goal missing a **Measurable** signal (a gate can evaluate it) or a **Convergent** stop (a reachable termination, not "perfect"); missing either → **surface the gap**, don't paper over it. These two decide whether a run succeeds or spins.
- **Anti-drift: flag, don't rewrite.** Make the target **Specific** (one decomposable objective) and check it stays **Relevant** (aimed at the real outcome) — surface a mismatch, **never silently rewrite intent**.
- **Feasibility flag.** Flag an un-**Achievable** / over-scoped goal (one that would hit the repair cap and escalate) rather than emit it as-is.
- **Time-bound = convergence, never a clock.** "Bounded / converges / won't loop forever" — **no literal deadlines** or timers (`think-deep` has no clock).
- **Author no check, no bar.** `smart` names the measure and defers operationalization — it **never writes the executable `Done-when`** (think-deep's) or the acceptance/quality bar (critic's). Feeder: emit and **STOP**, runs inline, **never spawns**. **Standalone** — emits plain text; no other-plugin dependency to run.

## Phase 0 — Diagnose the gaps
Read the goal; name which properties are missing — **Measurable? Convergent?** (the core) · Specific? Relevant? · Achievable? Already sharp on all → one-line confirm + emit. Otherwise **rewrite when the intent is clear; interview only the missing contract points** (don't re-ask what's already there).

## Phase 1 — Shape to the two-point contract
Pin **one specific objective**; an **in / out-of-scope** line; the **success signal(s)** — measurable, named in principle (the gate's raw material); and a **reachable stop** ("done when the signal holds", not "perfect"). Add a light Achievable/Relevant watch-out if any.

## Phase 2 — Emit + hand off
Emit the sharpened-goal block as **flush-left markdown** — one `###` heading per field (Goal (sharpened) · Objective · In scope · Out of scope · Success signal · Stops when · Watch-outs · Usage), each value on its own line(s), tags **inline** as a lead-in (`Measurable (the gate's raw material) [✓]:`), multi-point fields as flush-left `-` bullets. **Never** align columns, pad, right-float a tag, or hang-indent — fixed-width layout deforms on console word-wrap and can't be copied without reflow. Exact shape + rules: `references/output-format.md`. Then **STOP** (standalone MAY offer to chain into `think!` on confirm).

## When NOT to use
Goal already sharp (measurable + bounded) → just `think!` / `auror!`. · Subjective-quality target with an exemplar → `critic!` / `auror locomotor!` pins the bar. · You want options, not a sharpened goal → `ideate!`.
