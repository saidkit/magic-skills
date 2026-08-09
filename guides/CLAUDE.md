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
One standalone task run as a **goal**: the requested scope + quality gates are the completion condition. Run `auror!` with them stated as think-deep's `Done-when`.
think-deep's **Phase-4** drives it — turning each QA/review finding into the next repair cycle (re-plan -> fix -> re-verify) until every gate passes (converge) or a hard blocker is hit (escalate — never self-certify, never silently quit). `auror locomotor!` supplies the completion condition and scopes it to one task; it adds no second loop.
Single task only — never combine with `said!` or `flow!`. The prompt-level equivalent of a `/goal` run. Does NOT carry across invocations.

## `said!`
Execute the full SAID cycle for user-specified task: triage (if needed), add or update the task, implement, run required verification, run full e2e UAT including Playwright MCP when UI behavior is involved, and debrief. **First action: resolve the ordered stage sequence from the SAID map and emit it as an explicit checklist for this task** (do not restate the chain from memory — read it), then reconfirm by user.
Each stage **runs its `said:` plugin skill** — walk the SAID phase chain (Scope → Architect → Implement → gates → Debrief) per the plugin's **own map**: the said README + each skill's description are the authoritative order, gates, and branch points (skills self-select by phase — e.g. `scope-refine` vs `scope-grill` at Scope; read the map for the rest). Do NOT re-encode the chain here — read it. **Invoke the skills, never emulate the work inline**; skip/adapt only the UX gate on non-web tasks.
**Run every stage by default; the cycle is not complete until the debrief close-footer exists** — the single closure signal, which debrief writes only after its Phase-3.5 gate-check clears (gates passed, or a skip you explicitly confirmed and it recorded). Declaring the work done without that footer is a false close, not a finished cycle. **Omission is never silent:** skip or defer a stage only on explicit operator confirmation, recorded — never present a mandatory stage as an optional offer ("if you want…"). When nested under an autonomy macro (`auror!` / `expelliarmus`), "reconfirm by user" relaxes to report-and-proceed and stages run without pauses — but an **omission is the one wait autonomy cannot drop: a hard blocker that forces the confirmation** (autonomy drops the wait, not the stage). During implementation use silencio! principle.

## `flow!`
Multi-lane SAID orchestrator (skill: `said:flow`) — 5 slots, Route · Invoke · Boundary · Compose · Drive:
1. **Route.** ≥2 SAID lanes (a mount ≠ a lane) → `flow!`. Single-lane → `said!` (→ `/said:impl` once architected). Never nest; never pre-decide the split.
2. **Invoke.** FIRST action = `Skill(said:flow)` + feature id. Hand-rolling lanes = emulation — stop, invoke.
3. **Boundary.** Skill owns everything invoke→yield (sequencing · crossings · fork/rotate · gates · UAT). Read there; never restate or override.
4. **Compose.** Launch: pure lane-work → `/goal flow!`; + non-lane work → `/goal auror! flow!`; NEVER `auror locomotor! flow!` (→ INIT-28), never `said! + flow!`. `/goal`'s evaluator reads the transcript → the condition MUST name the sentinel `feature closed: yes` (template below); unattended = + auto mode. Under `auror!`/`expelliarmus`: report replaces the wait — **every gate still runs**. `silencio!` during impl.
5. **Drive to stop.** No `/goal`: re-invoke `/said:flow <id>` until `feature closed: yes` — one pass ≠ the loop. Under `/goal`: that printed block is the evaluator's oracle and `/goal` re-invokes. Under `auror!`: think-deep drives it as a loop-shaped `via:` step each pass. Ticking one `/said:flow` done = the INIT-28 demotion.

`/goal` condition template (name the sentinel, or the evaluator can stop early; prepend `auror!` for the mixed-work form):
```
/goal <FEAT-ID> — <one-line feature>. Drive it across every lane via flow! (/said:flow).
Done ONLY when /said:flow prints `feature closed: yes` (all lanes Closed AND feature e2e/UAT ∈
{passed, skipped(recorded), n/a}). If it prints `feature closed: no`, continue. Escalate on
no-progress two passes running or after N turns.
```

## `revelio` / `revelio!`
execute /magic:revelio skill

## `locomotor!`
Run `revelio!`, then proceed through its next-actions list autonomously until a full completion, as if operator typed `expelliarmus!` — same hard-blocker rules, same no-carry-across-invocations, same no-new-stages constraint. Operator may interrupt between phases by sending a new message; otherwise both phases run in one response.

## `pensieve!`
execute /magic:pensieve skill

## `lumos!`
execute /said:retrieval skill

## `muggle!`
Briefly explain in plain human language where we are, what is happening, or the subject the operator asked about. Prioritize the essential meaning, current state, and practical implication. Avoid implementation detail, jargon, exhaustive history, and formal status-report structure unless needed for clarity.

## `pensieve locomotor!`
Run `pensieve!`, then proceed through the remaining path autonomously as if `expelliarmus!` was active, stopping only at natural completion or a hard blocker.

## `session!`
execute /magic:session skill

## `think!`
execute /magic:think-deep skill — the **interactive** form (keeps think-deep's Phase-0 confirm). think-deep captures the task's acceptance criteria as its `Done-when` and loops on them (Phase-3 gate → Phase-4 converge/escalate); pass any explicit success conditions in the task.
