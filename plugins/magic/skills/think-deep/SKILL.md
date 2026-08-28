---
name: think-deep
description: >
  Structured task orchestrator — decompose into steps, self-check each, then verify the whole against explicit acceptance criteria and loop until they pass. 
  Triggered ONLY by the explicit command "/magic:think-deep" invocation AND NOTHING ELSE.

---

# Think-Deep — structured task orchestrator

Decompose a complex task, execute each step with a mandatory self-check, then verify the whole deliverable against explicit acceptance criteria and loop until it passes. Progress shows after every step.

**Prime directive — compose, don't emulate.** If the task names or implies a skill, `/command`, operator macro, or pipeline, INVOKE it — never reproduce its work by hand.
Expand a macro to the skill(s) it maps to (per `CLAUDE.md`); invoke a named multi-skill pipeline stage-by-stage in its declared order, never flattened into hand-rolled steps.
Emulating a named capability is the primary failure this skill prevents.

**Language.** Respond in the language of the invoking message — all phases, checks, the protocol file, and the deliverable.

**Marker.** While a run is live, **lead every turn with `[think] <id>`** — phase-scoped: `· step N/total` (Phase 2) · `· gate` (Phase 3) · `· iter K` (a Phase-4 repair iteration — overrides `· step`) · `· done`/`· escalated` (close). Nested: flip to the active leaf's id.

## Phase 0 — Understand

1. **Parse.** Identify deliverable · constraints · domain knowledge · **capability signals** (named skills / `/commands` / macros / pipelines). Resolve each to the skills it invokes.
2. **Contract — `Done-when`.** List the acceptance criteria that define done: from the operator's stated conditions, else derived from the task. Each is a **checkable predicate** — executable where possible (a test passes · a command exits 0 · a route returns 200 · a grep matches), else tagged **judgment**. Phase 3 tests against these; without `Done-when` there is no gate.
3. **Unclear → ask ONE focused question.** Do not guess; do not proceed until answered.
4. **Restate + confirm:** deliverable, scope, constraints, `Done-when`, and the skills you will invoke. Wait for confirmation. Under `auror!`/`expelliarmus`: state it and proceed. Trivial task → one-line restate, proceed.

## Phase 1 — Plan

1. **Decompose** into 3–10 steps. Each: deliverable · check criterion · **`via:`** (the skill/command that performs it, or `inline`). A pipeline's skills are `via:` bindings in declared order; its gates are their own steps. Sequential unless a dependency is noted.
2. **Loop-shaped `via:`.** If a `via:` names a re-entrant loop skill (reconstruct → act → re-enter until its own stop condition), the step reads **"drive X to its stop condition via repeated invocation"**, never "invoke X"; the plan carries a **final step** that re-invokes X and records its stop-condition output verbatim. Invoking a loop once demotes it to a subroutine and drops every rule it enforces on later passes.
3. **Protocol file — a carried run-id + a disk fallback.** Track steps in a markdown protocol file in the **session scratchpad / temp dir** (keep the project repo clean). Write it into a project working dir (`docs/working/<feature>/`, `notes/`, `planning/`) ONLY on operator request, or when the run's deliverable itself is a durable plan. Never a hardcoded path; state the resolved path in chat.
   - **Carry your run-id (fast path).** Your **id** names your file `think-<id>.md`; **announce `▶ think-deep <id>` on the launch turn** (which also leads with the `[think] <id>` Marker), and resume by opening `think-<id>.md` directly (no scan). **Id derivation + minting follow the canonical rule in `references/run-id.md`** — the single source shared across the `magic:think-*` family. Nested runs each carry their own id; when a child returns, resume your own.
   - **Disk fallback (survives a full compaction).** Each file stamps `Parent: <parent-id|none>` and flips `Closed:` to `done`/`escalated` at its terminal outcome. **If you are mid-run but cannot open your carried id's file** (a full compaction dropped it), reconstruct from disk instead of re-minting: glob `think-*.md`, read `Parent`/`Closed`; the **live leaf** is the un-`Closed` run that no other un-`Closed` run names as `Parent` — resume it. **Several un-closed leaves, or none matching the task ⇒ ASK which to resume; if you cannot ask (a subagent, no operator), resume the best task-match, else start fresh — never fork blindly.**
   - **Write only your own.** Read any `think-*.md` to relate runs; write only `think-<id>.md`, never a file you did not create. On converge you may delete your own file.
  ```
  Path: <protocol-dir>/think-<id>.md

  # Execution Protocol: <task>
  Parent: <parent-id|none> · Closed: no          # Closed → done|escalated at end
  ## Done-when
  - [ ] <criterion> — <check: cmd / grep / judgment>
  ## Steps
  - [ ] **1** <step> → via: <skill|inline> → deliverable: <what> · check: <criterion>
  ## Results
  (filled during execution)
  ## Gate log
  (per-iteration verdicts)
  ```
4. **Output the step list to chat.** Self-check: a named pipeline/skill absent from the `via:` bindings ⇒ rebind before executing.

## Phase 2 — Execute

Per step, in order:

1. **Do the work.**
2. **Self-check** against the step's check criterion and any `Done-when` it touches:
   > **Self-check [N]** — **Good:** <specifics> · **Issues:** <numbered> · **Verdict:** PASS / FIX
   Test: completeness · correctness · consistency with prior steps · traceability (each claim → a source) · bloat. Nothing wrong ⇒ look harder; name one improvable thing.
3. **FIX before advancing.** No forward move on a FIX verdict; re-check after fixing.
4. **Update the protocol:** tick the step, write its Results. **Checkbox + Closed integrity** — no `[x]` while its Results read pending/blocked/not-started (untick on conflict); set `Closed: done`/`escalated` at the terminal outcome, never leave an ended run un-`Closed`. Plan changed ⇒ say so in chat, never silently.
5. **Report** ≤3 sentences + remaining steps.

## Phase 3 — Acceptance gate (independent, depth-safe)

Verify the deliverable against every `Done-when`. **A ticked step never closes the run — only this gate does.** Independence = evidence, not an agent:

- **Executable criterion** → run the check; tool output is the verdict. Never grade from memory of having done the work.
- **Judgment criterion** → fresh-pass review, criterion by criterion, citing `file:line` / output.
- **Spawn = optional, depth-0 only.** A fresh reviewer subagent may strengthen judgment criteria ONLY when you are the top-level agent (invoked directly in the session, not spawned via the Agent/Task tool). If you are yourself a subagent: do NOT spawn (nested-spawn errors) and do NOT invoke a verification skill that itself spawns — verify inline. Inline evidence-based review is the always-safe default.

Per criterion → **PASS** / **FAIL** (+ evidence, gap). Confirm coherence: the step results form one deliverable, no gaps.

## Phase 4 — Converge or escalate

- **All PASS** → assemble and present the deliverable + a ≤3-sentence summary (done · key decisions · caveats); record the verdicts in the Gate log; **set `Closed: done`** (you may delete your own protocol file); close. Do not replay the step history.
- **Any FAIL · iterations < cap · progress since last pass** → **repair iteration**: re-enter Phase 1 scoped to the failed criteria only, seeded by the gap + the protocol (do not re-tread). Increment the Gate-log iteration. Default cap: 3.
- **Cap reached · OR the same criterion fails two iterations running** → **STOP + escalate** with the residual gap; **set `Closed: escalated`**. Never self-certify; never silently quit. Under `auror!`/`expelliarmus`, this escalation is the one wait autonomy cannot drop.

## Anti-patterns

- Emulating a named skill/macro/pipeline instead of invoking it — the #1 failure.
- Autonomy (`auror!`/`expelliarmus`) dropping a stage/gate — it removes waits, not stages.
- Skipping or rubber-stamping a check ("looks good") — name specific positives and issues.
- Grading a `Done-when` from memory instead of running its check.
- Scanning or re-minting your protocol when your carried id already names it — open `think-<id>.md` directly.
- Leaving an ended run un-`Closed` — a stale open file is a false leaf for the disk fallback.
- Spawning a subagent from within a subagent, or requiring a spawn to verify.
- Closing without the gate — declaring done because the steps ran, not because the criteria passed.
- Silent plan rewrites · gold-plating past confirmed scope · apologizing for corrections.

## When NOT to use

Simple factual questions · quick tasks (<2 min) · creative writing where structure kills flow · when the operator asked for a quick/rough answer. If invoked on a trivial task, say so and answer directly without the full protocol.
