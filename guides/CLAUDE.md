## `proceed!!`
Standing OK to proceed through all phases / batched tasks / multi-step flows without further confirmation pauses, until natural completion or a hard blocker.
Skip Phase A→B, Phase B→C, batch boundaries, rule-by-rule `next` waits for the remainder of the invocation. Still REPORT each phase boundary; only the wait goes — **never a stage, a gate, or an operator-question boundary**. A suppressed confirmation pause never removes the step it guarded (a verification / acceptance / debrief stage still runs; autonomy drops the wait, not the work). Does NOT carry across invocations. Hard blocker = unsatisfiable Approach, failing quality gate needing decision, ambiguous scope-creep, destructive op  outside scope.
A blanket grant covers **how-to-build choices only — never an operator question**, which is announced once, then held (the same whether you watch or walk away); to pre-decide a reserved class, **name it** in the directive — no grant persists. An operator question is **not an "ambiguous answer"** a grant may default: a blanket grant does not reach it, however the grant is worded — only naming the specific reserved class pre-decides it.

## `task-comments!!`
Use a rule: in source code, reference comments must be **task-id + very short why** only.
Format: `// <task-id>` (bare) or `// <task-id> — <≤10-word why>`.
When operator types `task-comments!!`, recall this rule and apply it; retroactively trim in-progress source files if asked. Multi-line rationale belongs in the task body / ADR / UX-spec — not the source.

## `run!!`
Invoke /magic:think-deep skill for user-specified task: build a plan, execute autonomously, cross-verify the results, and deliver a final report.
The loop is think-deep's, not run!!'s: "cross-verify" = its Phase-3 acceptance gate against the task's `Done-when`; "natural completion" = Phase-4 all-pass; the repair loop hitting its cap without convergence is a hard blocker (escalate — never self-certify). run!! adds autonomy + the report, never a second loop.
**Enforcement:** FIRST action on `run!!` = call `Skill(magic:think-deep)`. Not satisfied by "proceeding autonomously" — doing the work without invoking `/magic:think-deep` is emulation. Haven't invoked it this turn? Stop, invoke it.
If the task body names a macro or pipeline (e.g. "implement as said!!"), pass it to think-deep **intact** — do not pre-summarize it into generic steps. The plan must **bind that pipeline to its actual skills** (invoke them; never emulate inline), and surface the skills it will invoke.
Proceed as if proceed!! is active: report phase boundaries, but do not wait at them. Stop only at natural completion or a hard blocker.
Hard blocker = unsatisfiable approach, failing quality gate needing operator decision, ambiguous scope-creep, missing credentials/tooling, or destructive operation outside scope. Does NOT carry across invocations.
If the driven pipeline stops with `CONTEXT-CHECKPOINT`, that is its planned stop, not a failure: `/clear`, then `think!! continue <path>` (the protocol path the session-start re-anchor prints) -- never a new `run!!`.
Before a long pause, `think!! export` the run so its protocol survives the scratchpad rotation.

## `drive!!`
Anchored quality goal-run — one subjective target, single builder track (not a subagent ban):
1. `Skill(magic:critic)` on the task → comparative `Done-when`.
2. Print contract → confirm (autonomy: report-and-proceed).
3. `run!!` builds to that `Done-when`.
4. **Acceptance = an independent `critic!!` review (reviewer ≠ builder), NOT the builder's own gate** — run!!'s converge/escalate runs on that review's findings, closing only when the independent review adds **nothing new**, else escalating. A self-graded "all pass, no iteration" can never close it.
The critic's pass cap (at most 3 passes by one reviewer per target) ends that review through the escalate branch, never a 4th pass.

## `said!!`
Single-feature SAID orchestrator — full cycle (skill: `said:said`) — 3 slots, Invoke · Compose · Drive:
1. **Invoke.** FIRST action = `Skill(said:said)` + the task — as `said!! <directive>` or `<directive> as said!!`. Hand-rolling stages = emulation (under `/goal`: no skill → no `goal:` line → spin).
2. **Compose.** Under `run!!`/`proceed!!`: the checklist-confirm relaxes to report-and-proceed — every stage/gate still runs; an unconfirmed omission is a wait autonomy can't drop (as is an operator question, per `proceed!!`). `task-comments!!` during impl.
3. **Drive.** The skill prints a `goal:` line every turn (`done` = debrief footer + gates passed / `continue` / `stop`). Under `/goal` that IS the completion condition — write a plain directive, never hand-write it. `continue` re-invokes `said:said`; `done`/`stop` end it. `run!!`: think-deep loop-shaped `via:` step.
A `goal: stop -- CONTEXT-CHECKPOINT` is a planned stop, not a failure and not an operator question: `/clear`, then re-issue the same directive (the skill resumes by inspection).

## `flow!!`
Multi-lane SAID orchestrator (skill: `said:flow`) — 3 slots, Invoke · Compose · Drive:
1. **Invoke.** FIRST action = `Skill(said:flow)` + feature id — as `flow!! <directive>` or `<directive> as flow!!`. Hand-rolling lanes = emulation (under `/goal`: no skill → no `goal:` line → the loop spins).
2. **Compose.** Under `run!!`/`proceed!!`: report replaces the wait — every gate still runs. `task-comments!!` during impl.
3. **Drive.** The skill prints a `goal:` line every turn (`done`/`continue`/`stop`). Under `/goal` that line IS the completion condition — write a plain directive, never hand-write it. `continue` re-invokes `/said:flow`; `done`/`stop` end it. `run!!`: think-deep drives it as a loop-shaped `via:` step.
A `goal: stop -- CONTEXT-CHECKPOINT` is a planned stop, not a failure and not an operator question: `/clear`, then re-issue the same directive (the skill resumes by inspection).

## `resume!!`
Run `refresh!!`, then proceed through its next-actions list autonomously until a full completion, as if operator typed `proceed!!` — same hard-blocker rules, same no-carry-across-invocations, same no-new-stages constraint. Operator may interrupt between phases by sending a new message; otherwise both phases run in one response.

## `think!!`
**Front-dispatch.** Route to `Skill(magic:think)` (the run manager over think-deep's `think-<id>.md` files) ONLY when the first token is a manager verb {list, status, clear, resume, export, continue} **and its tail is empty or a lone operand** (`all` · an id · a path) — NOT free-form prose. So `think!! clear all` / `think!! resume PROJ-01` / `think!! continue /path/think-x.md` → manager; a verb followed by a task phrase — `think!! clear up the spec`, `think!! continue the refactor`, `think!! list the top risks` → `Skill(magic:think-deep)`: execute the task (interactive form; captures its acceptance criteria as the `Done-when`, loops Phase-3 gate → Phase-4). The manager owns its routing table.

## `ruled!!`
Record an operator ruling (skill: `magic:ruled`). FIRST action = `Skill(magic:ruled)` + the text; by hand = emulation.
Compose: a sweep writes only lines the operator confirmed; an assistant choice under a grant is never a ruling.

## `precedent!!`
execute /said:retrieval skill
