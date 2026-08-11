---
name: critic
description: >
  Authors a bounded acceptance contract for a quality target — subjective (blind-comparative against an exemplar) or objective (repair-loop to zero defects) — then gates it into review (default) · repair (`+fix`) · export (`as prompt`). Converts an open-ended "make it as good as X" into a terminating `Done-when` the acceptance loop converges on.
  Activates ONLY on a user's explicit `/magic:critic <target>` or `critic! <target>` invocation AND NOTHING ELSE.
---

# Critic — acceptance-contract author

Turn a fuzzy quality target ("as good as X", "world-class", "production-quality", "no bugs left") into a pinned, bounded `Done-when` the acceptance loop can converge on. **Author the contract; never run the loop** — `/magic:think-deep` (via `auror!` / `think!` / `/goal`) executes it. A `Done-when` is a well-specified criterion the loop already runs; never re-implement it or start a second loop.

## Invocation & parameters

`/magic:critic <target>` or `critic! <target>` — `<target>` = a path · dir · session id · description. One optional trailing **mode** parameter (default = **review**):

| Parameter | Mode | Effect |
|---|---|---|
| *(none)* | **review** | the default drive — report findings, **edits nothing** |
| `+fix` | **repair** | review, then fix — the only mode that edits the target |
| `as prompt` / `as full prompt` | **export** | render-only — the terse human prompt (full = enumerated, zero-context), then STOP |
| `park` | **hold** | author + hold the contract; no drive |

## Phase 0 — Classify the target

From the interview, route to the bar shape (worked entries in `references/critic-library.md`):
- **C — subjective / perceptual** (UI · copy · prose · logo · audio · video · deck): a **blind-comparative** bar against an external reference.
- **T — objective / spec** (software feature · API · refactor · data result): a **repair-loop or executed** bar — adversarial review to zero defects, or runs-green. No external reference; the standard is the spec / tests / source-of-truth.
- **C+T — composed** (dashboard · landing page · multi-step flow): the conjunction — author every sub-bar, stop only when all pass.

## Phase 1 — Pin the standard (the one input autonomy cannot skip)

- **C branch:** pin the **anchor** (named exemplar to match/beat) + **reference artifact** (image · brand kit · exemplar doc — capture its path/handle). No reference obtainable ⇒ **hard-block**: ask ONE focused question naming what is missing — never author a comparative gate without a reference, or the loop optimizes the wrong thing.
- **T branch:** pin the **internal standard** — the spec, test suite, or source-of-truth the review holds it against — plus the **severity threshold** (P0/P1 vs P0–P2) and whether it touches money/data/security (→ attacker stance). A repair loop's reference is the code itself, so **no hard-block**.

Under `auror!`/`expelliarmus` the *wait* relaxes, the *pin* does not — the standard (external anchor **or** internal spec/tests) is never droppable. Find the nearest library entry; adapt its standard from the interview.

## Phase 2 — Author the `Done-when`

Write terminating criteria — never a bare score (never converges), never a reward-hackable feature checklist:
- **C:** "judge <deliverable> BLIND against <reference> (both unlabeled), whole artifact, say which better meets the anchor; pass at **≥K of N** blind looks" — fix K/N before the run (the stop).
- **T:** "adversarial review until **0 open P0/P1 and nothing new** (attacker stance if it moves money/data/security); + tests green, no regressions" — or the executed form ("contract tests green · every documented shape returned") for a pure spec target. The stop is *defects reach zero and a fresh pass finds nothing new*.
- **Guardrails** (executable floor, from the library) — necessary-but-not-sufficient (tokens ∈ kit · tests green · budget · a11y).

Assemble the `Done-when`; Phase 3 renders and routes it.

## Phase 3 — Gate, then the exit (feeder, never a second loop)

**Render terse by default** — a floor pointer + the bar + the stop (`as full prompt` enumerates; see `references/prompt-forms.md`). Then hit the **gate**, and take the mode parameter's exit:
- **Standalone** — show the contract and **wait at the gate** for the mode (`review ⏎ · +fix · as prompt · park`). The pin already happened; the wait is the cheap checkpoint before an expensive run.
- **Under `auror!`/`expelliarmus`, or composed in a loop** — the *gate* auto-passes (never the pin), no footer: emit-and-STOP as a `via:`/loop step (the enclosing loop drives), else drive inline.

**Each exit's deliverable:** **review** hands the `Done-when` to `/magic:think-deep` — adversarial per target, verified, **writes a ranked `…-review.md` (file:line)**; reports findings, **edits nothing**, stops when a pass finds **nothing new**. · **`+fix`** repairs to **0 open P0/P1 and nothing new** — the only exit that edits. · **as prompt** emits the terse contract and STOPS (human export / loop feeder) — never run the loop, never re-implement the gate. Runs inline; **never spawns**.

## Critic library

`references/critic-library.md` — worked bars keyed by target; find the nearest, adapt its standard from the interview. **C** bars judge blind vs a reference; **T** bars are review-found or executed; compose **C+T** for cross-cutting targets. Pin the standard; set K/N (or the severity threshold) by stakes.

## When NOT to use

A target with **no meaningful standard** — nothing to compare against, no spec, no test, no defect class to close — there is no bar to author; say so. · A trivial one-shot with no acceptance risk — think-deep's plain `Done-when` suffices; critic is for targets where *"when is it done?"* is itself the hard question.
