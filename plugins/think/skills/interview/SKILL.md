---
name: interview
description: >
  Gather front-end for expert knowledge: interview an expert with journalist-grade drilling, ground every assertion against available evidence, and emit a structured, skill-consumable raw-material document (core, claims, counter, evidence, data, insight, so-what) for a downstream writer / spec / think!! / etc — then STOP. It extracts source material; it never writes the downstream artifact. Composable as a prep/gather step: another skill may invoke it to extract material before its own work, and it accepts handed-in evidence.
  Activates ONLY on an explicit `/think:interview <topic>` or `interview!! <topic>` invocation AND NOTHING ELSE — NOT `ideate` (diverges options), NOT `smart` (shapes a goal), NOT `critic` (authors a bar).
---

# Interview — expert-knowledge extraction

Pull what an expert actually knows onto the page *before* anything is built or written: **ground → recon → drill → crystallize**. The missing gather front-door — a builder fed three thin theses stretches three thin theses. Drill past abstraction, confront every claim against real evidence (an assertion is not a fact), track state so you never drift, and **emit** the raw material — then **STOP**. Extraction is not writing.

## Invocation & parameters
`/think:interview <topic>` or `interview!! <topic>` — `<topic>` = the subject to extract. Optional inputs:

| Input | Effect |
|---|---|
| evidence pointers (files · paths · links · pasted notes) | folded into the Phase-0 grounding map |
| `show state` (mid-interview) | print the live state block, then continue |
| composed by another skill | invoked via the Skill tool with `{topic, evidence-pointers?, expert?}`; returns the doc to the caller |

## Contract — holds every run
- **Ground first — mandatory-attempt, graceful-degrade.** You MUST ingest whatever evidence is reachable (supplied files/paths/links/pasted material, or the readable repo/context) and build the grounding map that lets you confront the expert's claims. When genuinely no evidence exists, **say so** explicitly and degrade to a pure interview — grounding is attempted, **never faked**. External web research is optional / author-triggered.
- **Never accept the first answer.** One question at a time; every answer earns at least one drill. Drill with the intrinsic techniques (5-Whys · Scene · Devil's advocate · What-if-not — `references/technique-catalog.md`); switch technique rather than repeat; "don't know" is a signal to reformulate; repetition means the slot is exhausted.
- **Rewrite the live state block after every answer.** The anti-drift state (meta · immutable grounding map · mutating question plan · slot tracker · current core sentence · next-move decision) is rewritten after each answer *before* the next question — this is what stops drift after 5–6 exchanges. `show state` exposes it. Template in `references/output-format.md`.
- **Cover the slots; flag the gaps.** Track seven slots — **core · claim · counter · evidence · data · insight · so-what**. Fill the L2-required subset (core + ≥1 claim + ≥1 evidence + so-what) at minimum; leave the rest **unfilled** only with an explicit **flag** in the output.
- **Wind down honestly — L3 > L1 > L2.** Three sufficiency levels, in strict priority: **L3 expert signals** (fatigue · "enough" · repetition) override **L1 hard limits** (max questions · max clarifiers · max returns) override **L2 minimum slots**. Better to under-collect than grind the expert.
- **Emit and STOP — dual invocation.** Produce the raw-material doc and STOP: no auto-handoff, **not a writer**, no pipeline run. On the operator path the doc is the last thing you print; as a **calling skill**'s prep step, **return** the same structured **doc** to the caller for inline use. Self-contained — depend on no other plugin's skill.

## Phase 0 — Ground & map
Restate the topic in one line. Ingest all reachable evidence + any handed-in precedent into a **grounding map**: the current consensus, the camps, the open questions, the load-bearing data — and the points where the expert may diverge. No evidence reachable → **say so** and note the interview runs ungrounded. Seed the question plan (7–10 questions) and open the live state block.

## Phase 1 — Recon
Ask 3–4 questions to locate the expert's position relative to the grounding map. After each answer, update state; mark the 1–2 points where the expert diverges from consensus or where the answer is thinnest — that is where Phase 2 drills.

## Phase 2 — Drill
5–8 adaptive questions. Pick the technique that fits the weakness (`references/technique-catalog.md`): **5-Whys** for an unbacked assertion, **Scene** for an abstraction with no specifics, **Devil's advocate** to confront a claim with a counter drawn from the grounding map, **What-if-not** for a story with no stakes. Never accept the first answer; switch techniques; re-score the core sentence each turn. Stop when the required slots fill or an L3 signal fires.

## Phase 3 — Crystallize
Play back a compressed summary (thesis · central case · takeaway) and the **core test**: the **single sentence** that captures what actually matters. The expert confirms or corrects. Core not found → return to Phase 2 focused on the empty slots (bounded by L1). Then assemble the output doc (`references/output-format.md`) and **emit** it — flush-left, every unfilled slot flagged — then **STOP** (or return it to the calling skill).

## Boundary — vs the other front-ends
Distinct on one axis each: `interview` **extracts** an expert's knowledge; `ideate` **diverges** options; `smart` **shapes** a goal; `critic` **authors** an acceptance bar. This never writes the downstream artifact and never picks between options — it gathers grounded source material and hands it off.
