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

## Phase 0 — Understand

1. **Parse.** Identify deliverable · constraints · domain knowledge · **capability signals** (named skills / `/commands` / macros / pipelines). Resolve each to the skills it invokes.
2. **Contract — `Done-when`.** List the acceptance criteria that define done: from the operator's stated conditions, else derived from the task. Each is a **checkable predicate** — executable where possible (a test passes · a command exits 0 · a route returns 200 · a grep matches), else tagged **judgment**. Phase 3 tests against these; without `Done-when` there is no gate.
3. **Unclear → ask ONE focused question.** Do not guess; do not proceed until answered.
4. **Restate + confirm:** deliverable, scope, constraints, `Done-when`, and the skills you will invoke. Wait for confirmation. Under `auror!`/`expelliarmus`: state it and proceed. Trivial task → one-line restate, proceed.

## Phase 1 — Plan

1. **Decompose** into 3–10 steps. Each: deliverable · check criterion · **`via:`** (the skill/command that performs it, or `inline`). A pipeline's skills are `via:` bindings in declared order; its gates are their own steps. Sequential unless a dependency is noted.
2. **Loop-shaped `via:`.** If a `via:` names a re-entrant loop skill (reconstruct → act → re-enter until its own stop condition), the step reads **"drive X to its stop condition via repeated invocation"**, never "invoke X"; the plan carries a **final step** that re-invokes X and records its stop-condition output verbatim. Invoking a loop once demotes it to a subroutine and drops every rule it enforces on later passes.
3. **Protocol file — one per run, stacked & resumable.** Track steps in a markdown protocol file. Default `<protocol-dir>` = the **session scratchpad / temp dir** (keep the project repo clean) — a **shared, session-scoped** dir that outlives any one run. Write it into a project working dir (`docs/working/<feature>/`, `notes/`, `planning/`) ONLY on operator request, or when the run's deliverable itself is a durable plan. Never a hardcoded path; state the resolved path in chat.
   - **Isolate + stack — the scratchpad is shared.** Nested or parallel runs share one dir (an outer `auror!` / `/goal` driving a nested `think!`; a `via:` step that re-enters think-deep; sibling subagents). Write your own **`think-<slug>-<n>.md`** (`<slug>`: lowercase the deliverable, drop stop-words, first ~4 significant tokens, hyphen-joined; `<n>`: the smallest integer that makes the name free in the dir) and stamp a header — **`Run:` this file · `Parent:` the run whose step launched you (else `none`) · `Status:` `active` | `awaiting-child` | `done` | `escalated`**. Launching a nested run: set your **own** `Status: awaiting-child`; when that child reaches a **terminal** state (`done` or `escalated`), flip back to `active` and continue or propagate. **Every run ends terminal** — `done` on converge (you may then delete your own file), `escalated` on STOP; **never leave a spent run `active`.** **READ any `think-*.md` header to relate runs; WRITE only the file whose `Run:` is yours** — never overwrite or adopt one you did not create.
   - **Resume from disk, never from memory (survives compaction).** On any re-entry — including after a context compaction — do **not** recompute-and-hope. Glob `think-*.md` in `<protocol-dir>`, read each `Run`/`Parent`/`Status`. **Exactly one `active` leaf ⇒ resume it** (regardless of header match). **Several `active` leaves ⇒ resume the one whose header matches this run**; zero-or-still-ambiguous ⇒ ASK which to resume; if you cannot ask (a subagent, no operator), resume the best task-match, else start a fresh run — never block, never fork blindly. **No `active` leaf but an `awaiting-child` parent whose child is terminal ⇒ flip that parent to `active` and resume it.**
  ```
  Path: <protocol-dir>/think-<slug>-<n>.md

  # Execution Protocol: <task>
  Run: think-<slug>-<n>.md · Parent: <file|none> · Status: active   # → awaiting-child while a child runs; → done|escalated at end
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
4. **Update the protocol:** tick the step, write its Results. **Checkbox + Status integrity** — no `[x]` while its Results read pending/blocked/not-started (untick on conflict); the header `Status` matches reality — set the terminal state at end, never leave a spent run `active`. Plan changed ⇒ say so in chat, never silently.
5. **Report** ≤3 sentences + remaining steps.

## Phase 3 — Acceptance gate (independent, depth-safe)

Verify the deliverable against every `Done-when`. **A ticked step never closes the run — only this gate does.** Independence = evidence, not an agent:

- **Executable criterion** → run the check; tool output is the verdict. Never grade from memory of having done the work.
- **Judgment criterion** → fresh-pass review, criterion by criterion, citing `file:line` / output.
- **Spawn = optional, depth-0 only.** A fresh reviewer subagent may strengthen judgment criteria ONLY when you are the top-level agent (invoked directly in the session, not spawned via the Agent/Task tool). If you are yourself a subagent: do NOT spawn (nested-spawn errors) and do NOT invoke a verification skill that itself spawns — verify inline. Inline evidence-based review is the always-safe default.

Per criterion → **PASS** / **FAIL** (+ evidence, gap). Confirm coherence: the step results form one deliverable, no gaps.

## Phase 4 — Converge or escalate

- **All PASS** → assemble and present the deliverable + a ≤3-sentence summary (done · key decisions · caveats); record the verdicts in the Gate log; **set your `Status: done`** (you may delete your own protocol file); close. Do not replay the step history.
- **Any FAIL · iterations < cap · progress since last pass** → **repair iteration**: re-enter Phase 1 scoped to the failed criteria only, seeded by the gap + the protocol (do not re-tread). Increment the Gate-log iteration. Default cap: 3.
- **Cap reached · OR the same criterion fails two iterations running** → **STOP + escalate** with the residual gap; **set your `Status: escalated`**. Never self-certify; never silently quit. Under `auror!`/`expelliarmus`, this escalation is the one wait autonomy cannot drop.

## Anti-patterns

- Emulating a named skill/macro/pipeline instead of invoking it — the #1 failure.
- Autonomy (`auror!`/`expelliarmus`) dropping a stage/gate — it removes waits, not stages.
- Skipping or rubber-stamping a check ("looks good") — name specific positives and issues.
- Grading a `Done-when` from memory instead of running its check.
- Reusing a shared protocol filename across nested/parallel runs, or forking a fresh one after a compaction instead of resuming the `active` leaf — both clobber or orphan a run.
- Leaving a run `active` after it closes or escalates — a stale `active` file breaks the leaf rule.
- Spawning a subagent from within a subagent, or requiring a spawn to verify.
- Closing without the gate — declaring done because the steps ran, not because the criteria passed.
- Silent plan rewrites · gold-plating past confirmed scope · apologizing for corrections.

## When NOT to use

Simple factual questions · quick tasks (<2 min) · creative writing where structure kills flow · when the operator asked for a quick/rough answer. If invoked on a trivial task, say so and answer directly without the full protocol.
