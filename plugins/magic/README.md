# `magic` — operator macros

Four stack-agnostic skills for controlling context, scope, orchestration and handoff mid-session. Part of [MagicKit](https://github.com/saidkit/magic-skills).

## Skills

### `/magic:revelio` — context refresh

Surfaces what has gone stale or buried mid-conversation and is load-bearing for the next step: recent activity, current work state, operator constraints stated in earlier turns, and 3–5 prioritized next actions. Deliberately skips what is already in recent turns — re-emitting that is noise, not refresh. **Stops.**

### `/magic:pensieve` — scope / status audit

Reconstructs the whole active scope end-to-end and emits a status ledger: every planned step plus every step that became necessary during execution, each marked Done / In progress / Blocked / Not started / Superseded with evidence and a next action, followed by current blockers and the remaining path. Unlike `revelio`, it does **not** skip recent turns. **Stops.**

### `/magic:session` — new-session handoff

Writes `working/<feature>/session-<n>.md` so a fresh session picks the work up cold. Confirms feature id and session number with the operator before writing. Carries what a cold session cannot reconstruct — decisions and their reasons, operator constraints, done vs. in flight vs. blocked — with citations rather than restated prose.

### `/magic:think-deep` — structured task orchestrator

Decomposes a complex task into 3–10 steps, each carrying a deliverable, a check criterion, and a **`via:`** binding naming the skill that performs it. Confirms the restatement with the operator, writes a live execution protocol file, then executes step by step — with a mandatory self-check after each that must name specific positives *and* specific criticism before moving on.

Its prime directive is **compose, don't emulate**: when a step is covered by a named skill, macro or pipeline, the step invokes it rather than hand-rolling equivalent work. A plan whose `via:` bindings omit a pipeline the task named is treated as a wrong plan and rebound before execution.

Pairs with the `think!` macro (plain invocation) and `auror!` (invoke, then run the plan through autonomously and deliver a final report).

## Design notes

**`revelio` and `pensieve` stop by contract.** They are diagnostics. The operator reads the output and decides. To chain straight into execution, use the `locomotor!` / `pensieve locomotor!` macros from [operator-macros.md](../../guides/operator-macros.md).

**Nothing carries across invocations.** No skill here makes subsequent turns "automatically refreshed" or "automatically precedent-checked". Each invocation is a fresh sweep scoped to the message that triggered it.

**No project files, no config.** These skills read whatever layout a project already has and adapt — `docs/adr/` vs `decision-log/` vs `architecture/decisions/`, `docs/working/` vs `notes/` vs `planning/`.
