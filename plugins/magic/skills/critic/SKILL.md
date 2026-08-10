---
name: critic
description: >
  Author a blind-comparative acceptance contract for a subjective/quality target — pin an external anchor, pick the critic form, emit a bounded `Done-when` for the acceptance loop to run.
  Triggered ONLY by the explicit command "/magic:critic". Do NOT trigger on general requests, reviews, or the word "critique". Only the exact command "/magic:critic" activates this skill.
---

# Critic — comparative acceptance-contract author

Turn a subjective/quality target ("as good as X", "world-class", "on-brand") into a pinned, blind-comparative `Done-when` the acceptance loop can converge on. **Author the contract; never run the loop** — `/magic:think-deep` (via `auror!` / `think!` / `/goal`) executes it. A comparative gate is a well-specified **judgment** criterion the loop already runs; never re-implement it.

## Phase 1 — Pin the anchor (the one input autonomy cannot skip)

Elicit for the target:
- **Anchor** — the named exemplar the result must match or beat.
- **Reference artifact** — the concrete thing to compare against: image · brand kit · exemplar doc · spec/test-suite. Capture its path/handle.
- **Bar** — find the nearest target in `references/critic-library.md`; adapt its standard from the interview.

No reference obtainable ⇒ **hard-block**: ask ONE focused question naming what is missing. Under `auror!`/`expelliarmus` the *wait* relaxes, the *pin* does not — never author a comparative gate without a reference (else the loop optimizes the wrong thing).

## Phase 2 — Author the `Done-when`

From the library entry, write the criteria:
- **Comparative, blind** — "judge <deliverable> BLIND against <reference> (both unlabeled), whole artifact, say which better meets the anchor." Never a feature checklist (reward-hackable); never an absolute score.
- **Bounded stop** — "pass at ≥K of N blind looks" (fix K/N before the run). This is what terminates the loop.
- **Guardrails** (executable, from the library) — the necessary-but-not-sufficient checks (e.g. token conformance · tests green).

Emit the assembled `Done-when` block verbatim.

## Phase 3 — Hand off (feeder, not driver)

- **Inside an enclosing loop** (invoked as a `via:` step, or under `auror!`/`/goal`): emit the `Done-when` and STOP — the enclosing loop drives it. Never start a second loop.
- **Standalone** (`/magic:critic` alone): after the operator confirms the contract, optionally invoke `/magic:think-deep` with it to run end-to-end. Runs inline; never spawns; never re-implements the gate.

## Critic library

`references/critic-library.md` — worked acceptance bars keyed by target; find the nearest, adapt its standard from the interview. Comparative bars (**C**) are critic's; targets tagged **T** (software · execution) route to think-deep. Pin the standard; K/N by stakes; compose for cross-cutting targets.

## When NOT to use

Objective/spec targets — think-deep's plain `Done-when` already gates them. · No external reference exists and none can be named — there is no comparative gate to author; say so.
