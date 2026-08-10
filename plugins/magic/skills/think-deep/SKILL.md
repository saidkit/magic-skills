---
name: think-deep
description: >
  Structured task orchestrator — decompose into steps, self-check each, then verify the whole against explicit acceptance criteria and loop until they pass. 
  Triggered ONLY by the explicit command "/magic:think-deep". Do NOT trigger on general requests, problem- solving, analysis, or any other phrasing. Only the exact command "/magic:think-deep" activates this skill.
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
3. **Bind the step tracker — once, here.** Compose with the environment's native tracker when present; emulate it with a file only when it is genuinely absent (the prime directive, applied to tracking). Take the first tier that resolves and **state the binding in one line** (e.g. *"task tracking: native"* / *"task tracking: file protocol"*):
   - **Hint** — an operator or `CLAUDE.md` line (`task-tracker: native|file`) → use verbatim.
   - **Native** — a native task tracker (`TaskCreate`/`TaskUpdate`, or `TodoWrite`) **named anywhere in your tool manifest — the eager list OR a deferred / lazy-loaded listing.** Being listed **is** positive confirmation; **present-but-deferred is NOT a reason to fall back** — you MUST load its schema (e.g. `ToolSearch`) and bind native. Register each step as a task (`via:`/check in metadata, deps where supported); write **no `## Steps` markdown**. Refocus = the tracker's own next-item reminder.
   - **File** — the markdown protocol below. Use it **only when a native tracker is absent from the manifest entirely** (neither eager nor deferred), or the hint says `file`. **Deferred-but-loadable ⇒ native, not file** — "I'd have to load it first" and "another log already tracks this" are not reasons to fall back. The safe-default caveat is the *absent* case only: a false-absent costs polish, a false-present breaks the run.
4. **Verification note — always think-deep's own, either backend.** `Done-when` + the `Gate log` have no native-tracker slot; keep them in a scratchpad note (`think-deep-gate.md`) — never a tracker state, never the repo. Under the file backend this note *is* the protocol file's non-`Steps` sections.
5. **Protocol file (file backend).** Default `<protocol-dir>` = the **session scratchpad / temp dir** — the protocol is a transient single-run scaffold (it dies with the run; keep the project repo clean). Write it into a project working dir (`docs/working/<feature>/`, `notes/`, `planning/`) ONLY on operator request, or when the run's deliverable itself is a durable plan. Never a hardcoded path; state the resolved path in chat.
  ```
  Path: <protocol-dir>/think-deep-protocol.md

  # Execution Protocol: <task>
  ## Done-when
  - [ ] <criterion> — <check: cmd / grep / judgment>
  ## Steps
  - [ ] **1** <step> → via: <skill|inline> → deliverable: <what> · check: <criterion>
  ## Results
  (filled during execution)
  ## Gate log
  (per-iteration verdicts)
  ```
6. **Output the step list to chat.** Self-check: a named pipeline/skill absent from the `via:` bindings ⇒ rebind before executing.

## Phase 2 — Execute

Per step, in order:

1. **Do the work.**
2. **Self-check** against the step's check criterion and any `Done-when` it touches:
   > **Self-check [N]** — **Good:** <specifics> · **Issues:** <numbered> · **Verdict:** PASS / FIX
   Test: completeness · correctness · consistency with prior steps · traceability (each claim → a source) · bloat. Nothing wrong ⇒ look harder; name one improvable thing.
3. **FIX before advancing.** No forward move on a FIX verdict; re-check after fixing.
4. **Record in the bound tracker.** Mark the step done and attach its Results. *File backend:* tick the step, write Results — **Checkbox integrity**: no `[x]` while its Results read pending/blocked/not-started; on conflict, untick and say so. *Native backend:* set the task done with a result note. Plan changed ⇒ say so in chat, never silently.
5. **Report** ≤3 sentences + the next step (file: print remaining steps; native: the tracker's own reminder).

## Phase 3 — Acceptance gate (independent, depth-safe)

Verify the deliverable against every `Done-when`. **A tracker step marked `completed` never closes the run — only this gate does** (a tracker "done" is self-asserted; the gate is the oracle). Independence = evidence, not an agent:

- **Executable criterion** → run the check; tool output is the verdict. Never grade from memory of having done the work.
- **Judgment criterion** → fresh-pass review, criterion by criterion, citing `file:line` / output.
- **Spawn = optional, depth-0 only.** A fresh reviewer subagent may strengthen judgment criteria ONLY when you are the top-level agent (invoked directly in the session, not spawned via the Agent/Task tool). If you are yourself a subagent: do NOT spawn (nested-spawn errors) and do NOT invoke a verification skill that itself spawns — verify inline. Inline evidence-based review is the always-safe default.

Per criterion → **PASS** / **FAIL** (+ evidence, gap). Confirm coherence: the step results form one deliverable, no gaps.

## Phase 4 — Converge or escalate

- **All PASS** → assemble and present the deliverable + a ≤3-sentence summary (done · key decisions · caveats); record the verdicts in the Gate log; close. Do not replay the step history.
- **Any FAIL · iterations < cap · progress since last pass** → **repair iteration**: re-enter Phase 1 scoped to the failed criteria only, seeded by the gap + the protocol (do not re-tread). Increment the Gate-log iteration. Default cap: 3.
- **Cap reached · OR the same criterion fails two iterations running** → **STOP + escalate** with the residual gap. Never self-certify; never silently quit. Under `auror!`/`expelliarmus`, this escalation is the one wait autonomy cannot drop.

## Anti-patterns

- Emulating a named skill/macro/pipeline instead of invoking it — the #1 failure.
- Autonomy (`auror!`/`expelliarmus`) dropping a stage/gate — it removes waits, not stages.
- Skipping or rubber-stamping a check ("looks good") — name specific positives and issues.
- Grading a `Done-when` from memory instead of running its check.
- Spawning a subagent from within a subagent, or requiring a spawn to verify.
- Closing without the gate — declaring done because the steps ran, not because the criteria passed.
- Silent plan rewrites · gold-plating past confirmed scope · apologizing for corrections.

## When NOT to use

Simple factual questions · quick tasks (<2 min) · creative writing where structure kills flow · when the operator asked for a quick/rough answer. If invoked on a trivial task, say so and answer directly without the full protocol.
