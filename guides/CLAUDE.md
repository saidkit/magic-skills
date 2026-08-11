## `expelliarmus` / `expelliarmus!`
Standing OK to proceed through all phases / batched tasks / multi-step flows without further confirmation pauses, until natural completion or a hard blocker.
Skip Phase A→B, Phase B→C, batch boundaries, rule-by-rule `next` waits for the remainder of the invocation. Still REPORT each phase boundary; only the wait goes — **never a stage or a gate**. A suppressed confirmation pause never removes the step it guarded (a verification / acceptance / debrief stage still runs; autonomy drops the wait, not the work). Does NOT carry across invocations. Hard blocker = unsatisfiable Approach, failing quality gate needing decision, ambiguous scope-creep, destructive op  outside scope.

## `silencio` / `silencio!`
Use a rule: in source code, reference comments must be **task-id + very short why** only.
Format: `// <task-id>` (bare) or `// <task-id> — <≤10-word why>`.
When operator types `silencio!`, recall this rule and apply it; retroactively trim in-progress source files if asked. Multi-line rationale belongs in the task body / ADR / UX-spec — not the source.

## `auror!`
Invoke /magic:think-deep skill for user-specified task: build a plan, execute autonomously, cross-verify the results, and deliver a final report.
The loop is think-deep's, not auror's: "cross-verify" = its Phase-3 acceptance gate against the task's `Done-when`; "natural completion" = Phase-4 all-pass; the repair loop hitting its cap without convergence is a hard blocker (escalate — never self-certify). auror! adds autonomy + the report, never a second loop.
**Enforcement:** FIRST action on `auror!` = call `Skill(magic:think-deep)`. Not satisfied by "proceeding autonomously" — doing the work without invoking `/magic:think-deep` is emulation. Haven't invoked it this turn? Stop, invoke it.
If the task body names a macro or pipeline (e.g. "implement as said!"), pass it to think-deep **intact** — do not pre-summarize it into generic steps. The plan must **bind that pipeline to its actual skills** (invoke them; never emulate inline), and surface the skills it will invoke.
Proceed as if expelliarmus is active: report phase boundaries, but do not wait at them. Stop only at natural completion or a hard blocker.
Hard blocker = unsatisfiable approach, failing quality gate needing operator decision, ambiguous scope-creep, missing credentials/tooling, or destructive operation outside scope. Does NOT carry across invocations.

## `auror locomotor` / `auror locomotor!`
Anchored quality goal-run — one subjective target, single builder track (not a subagent ban):
1. `Skill(magic:critic)` on the task → comparative `Done-when`.
2. Print contract → confirm (autonomy: report-and-proceed).
3. `auror!` with that `Done-when`.
Fan-out breadth → `gauntlet!`.

## `said!`
Single-feature SAID orchestrator — full cycle (skill: `said:said`) — 3 slots, Invoke · Compose · Drive:
1. **Invoke.** FIRST action = `Skill(said:said)` + the task — as `said! <directive>` or `<directive> as said!`. Hand-rolling stages = emulation (under `/goal`: no skill → no `goal:` line → spin).
2. **Compose.** Under `auror!`/`expelliarmus`: the checklist-confirm relaxes to report-and-proceed — every stage/gate still runs; an unconfirmed omission is the one wait autonomy can't drop. `silencio!` during impl.
3. **Drive.** The skill prints a `goal:` line every turn (`done` = debrief footer + gates passed / `continue` / `stop`). Under `/goal` that IS the completion condition — write a plain directive, never hand-write it. `continue` re-invokes `said:said`; `done`/`stop` end it. `auror!`: think-deep loop-shaped `via:` step.

## `flow!`
Multi-lane SAID orchestrator (skill: `said:flow`) — 3 slots, Invoke · Compose · Drive:
1. **Invoke.** FIRST action = `Skill(said:flow)` + feature id — as `flow! <directive>` or `<directive> as flow!`. Hand-rolling lanes = emulation (under `/goal`: no skill → no `goal:` line → the loop spins).
2. **Compose.** Under `auror!`/`expelliarmus`: report replaces the wait — every gate still runs. `silencio!` during impl.
3. **Drive.** The skill prints a `goal:` line every turn (`done`/`continue`/`stop`). Under `/goal` that line IS the completion condition — write a plain directive, never hand-write it. `continue` re-invokes `/said:flow`; `done`/`stop` end it. `auror!`: think-deep drives it as a loop-shaped `via:` step.

## `locomotor!`
Run `revelio!`, then proceed through its next-actions list autonomously until a full completion, as if operator typed `expelliarmus!` — same hard-blocker rules, same no-carry-across-invocations, same no-new-stages constraint. Operator may interrupt between phases by sending a new message; otherwise both phases run in one response.

## `think!`
execute /magic:think-deep skill — the **interactive** form (keeps think-deep's Phase-0 confirm). think-deep captures the task's acceptance criteria as its `Done-when` and loops on them (Phase-3 gate → Phase-4 converge/escalate); pass any explicit success conditions in the task.

## `lumos!`
execute /said:retrieval skill
