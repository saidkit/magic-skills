# Operator macros — the paste-in half

The `magic` plugin ships the four skills. This file ships the **macros that drive them**.

A Claude Code plugin cannot add text to your `CLAUDE.md`, and the macros are the ergonomic layer: they let you type `revelio!` mid-sentence instead of `/magic:revelio`, and they define the autonomy verbs (`expelliarmus`, `locomotor!`) that the skills refer to when they say "do not continue unless paired with `locomotor`".

Without this block the skills still work — you invoke them as `/magic:revelio`, `/magic:pensieve`, `/magic:lumos`, `/magic:session`. With it, they work the way they were designed to.

## Install

Paste the block below into **`~/.claude/CLAUDE.md`** (applies to every project) or a project's **`./CLAUDE.md`** (that project only).

## The block

```markdown

## `expelliarmus` / `expelliarmus!`
Standing OK to proceed through all phases / batched tasks / multi-step flows without further confirmation pauses, until natural completion or a hard blocker.
Skip Phase A→B, Phase B→C, batch boundaries, rule-by-rule `next` waits for the remainder of the invocation. Still REPORT each phase boundary; only the wait goes — **never a stage or a gate**. A suppressed confirmation pause never removes the step it guarded (a verification / acceptance / debrief stage still runs; autonomy drops the wait, not the work). Does NOT carry across invocations. Hard blocker = unsatisfiable Approach, failing quality gate needing decision, ambiguous scope-creep, destructive op  outside scope.

## `silencio` / `silencio!`
Use a rule: in source code, reference comments must be **task-id + very short why** only.
Format: `// <task-id>` (bare) or `// <task-id> — <≤10-word why>`.
When operator types `silencio!`, recall this rule and apply it; retroactively trim in-progress source files if asked. Multi-line rationale belongs in the task body / ADR / UX-spec — not the source.

## `auror!`
Invoke /magic:think-deep skill for user-specified task: build a plan, execute autonomously, cross-verify the results, and deliver a final report.
**Enforcement:** FIRST action on `auror!` = call `Skill(magic:think-deep)`. Not satisfied by "proceeding autonomously" — doing the work without invoking `/magic:think-deep` is emulation. Haven't invoked it this turn? Stop, invoke it.
If the task body names a macro or pipeline (e.g. "implement as said!"), pass it to think-deep **intact** — do not pre-summarize it into generic steps. The plan must **bind that pipeline to its actual skills** (invoke them; never emulate inline), and surface the skills it will invoke.
Proceed as if expelliarmus is active: report phase boundaries, but do not wait at them. Stop only at natural completion or a hard blocker.
Hard blocker = unsatisfiable approach, failing quality gate needing operator decision, ambiguous scope-creep, missing credentials/tooling, or destructive operation outside scope. Does NOT carry across invocations.

## `auror locomotor!`
Run `auror! reconfirm the goal; then plan, fix, QA/review, repeat till done; when done - do a short task debrief, review the original plan and show divergences`

## `said!`
Execute the full SAID cycle for user-specified task: triage (if needed), add or update the task, implement, run required verification, run full e2e UAT including Playwright MCP when UI behavior is involved, and debrief. Formulate the full execution path (stages and skills involved at each stage ) and reconfirm by user.
Each stage **runs its `said:` plugin skill** — walk the SAID phase chain (Scope → Architect → Implement → gates → Debrief) per the plugin's **own map**: the said README + each skill's description are the authoritative order, gates, and branch points (skills self-select by phase — e.g. `scope-refine` vs `scope-grill` at Scope; read the map for the rest). Do NOT re-encode the chain here — read it. **Invoke the skills, never emulate the work inline**; skip/adapt only the UX gate on non-web tasks. When nested under an autonomy macro (`auror!` / `expelliarmus`), "reconfirm by user" relaxes to report-and-proceed — but every stage and gate still runs (autonomy drops the wait, not the stage). During implementation use silencio! principle.

## `flow!`
Multi-lane feature — spans **two or more task logs**. A lane owns its own spec, task log, working dir and ADRs; a lane is **not** a repo or a mount — one feature may touch several mounts and stay single-lane. Single-lane → `said!`. Never nest the two.
**Enforcement:** FIRST action = `Skill(said:flow)` + feature id. Sequencing lanes without invoking it = emulation. Not invoked this turn? Stop, invoke.
Skill owns: lane sequencing · crossing classification · handover scoping · fork-vs-rotate · gates · stop conditions. Read there. Never restate or override here.
Never pre-decide the lane split. Never instruct it to hold tasks pending a reply.
`silencio!` during implementation. e2e UAT + Playwright MCP: feature-level, after all lanes close.
Under `auror!` / `expelliarmus`: report replaces wait; every stage and gate still runs.
**Drive the skill to its stop condition** — re-invoke until it emits `feature closed: yes`. A single invocation is a subroutine call, not the loop, and every rule the loop would enforce on later passes is lost.

## `revelio` / `revelio!`
execute /magic:revelio skill

## `locomotor!`
Run `revelio!`, then proceed through its next-actions list autonomously until a full completion, as if operator typed `expelliarmus!` — same hard-blocker rules, same no-carry-across-invocations, same no-new-stages constraint. Operator may interrupt between phases by sending a new message; otherwise both phases run in one response.

## `pensieve!`
execute /magic:pensieve skill

## `lumos!`
execute /magic:lumos skill

## `pensieve locomotor!`
Run `pensieve!`, then proceed through the remaining path autonomously as if `expelliarmus!` was active, stopping only at natural completion or a hard blocker.

## `session!`
execute /magic:session skill

## `think!`
execute /magic:think-deep skill
```

## Notes

- **`expelliarmus` is load-bearing.** `locomotor!` and `pensieve locomotor!` are defined in terms of it, and `/magic:pensieve` names it in its stop condition. Keep it even if you never type it directly.
- **Keep the `!` suffix meaningful.** Across this macro family the bare word and the `!` form do the same thing; the `!` is a readability cue that the operator means the macro, not the English word.
- **Macros do not carry across invocations.** This is deliberate — every macro is scoped to the message that invoked it, so an autonomy grant can never silently persist into later work.
